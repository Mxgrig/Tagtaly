export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    if (url.pathname === '/webhook') {
      if (request.method === 'GET') {
        const challenge = url.searchParams.get('hub.challenge');
        if (!challenge) {
          return new Response('Missing hub.challenge', { status: 400 });
        }
        return new Response(challenge, {
          headers: {
            'content-type': 'text/plain',
          },
        });
      }

      if (request.method === 'POST') {
        const raw = await request.text();
        const entries = parseFeed(raw, url.searchParams.get('topic'));

        if (entries.length) {
          await persistEntries(env, entries);

          ctx.waitUntil(
            env.FEED_HUB.fetch('https://feed-hub.internal/broadcast', {
              method: 'POST',
              headers: { 'content-type': 'application/json' },
              body: JSON.stringify({ entries }),
            }),
          );
        }

        return new Response('ok', { status: 202 });
      }

      return new Response('Method not allowed', { status: 405 });
    }

    if (url.pathname === '/feed' && request.method === 'GET') {
      const cached = await env.RSS_KV.get('latest');
      return new Response(cached ?? '[]', {
        headers: {
          'content-type': 'application/json',
          'access-control-allow-origin': env.ALLOWED_ORIGIN ?? '*',
          'cache-control': 'no-store',
        },
      });
    }

    if (url.pathname === '/live') {
      return env.FEED_HUB.fetch(request);
    }

    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: {
          'access-control-allow-origin': env.ALLOWED_ORIGIN ?? '*',
          'access-control-allow-methods': 'GET,POST,OPTIONS',
          'access-control-allow-headers': 'content-type',
        },
      });
    }

    return new Response('Not found', { status: 404 });
  },
};

export class FeedHub {
  constructor(state, env) {
    this.state = state;
    this.env = env;
    this.sessions = new Map();
    this.encoder = new TextEncoder();
  }

  async fetch(request) {
    const url = new URL(request.url);

    if (request.method === 'POST' && url.pathname === '/broadcast') {
      const payload = await request.json();
      const entries = payload.entries ?? [];
      await this.broadcast(entries);
      return new Response('ok');
    }

    if (
      request.method === 'GET' &&
      request.headers.get('accept')?.includes('text/event-stream')
    ) {
      const { readable, writable } = new TransformStream();
      const writer = writable.getWriter();
      const connectionId = crypto.randomUUID();

      this.sessions.set(connectionId, writer);

      const headers = {
        'content-type': 'text/event-stream',
        'cache-control': 'no-cache',
        'connection': 'keep-alive',
        'access-control-allow-origin': this.env.ALLOWED_ORIGIN ?? '*',
      };

      const initMessage = this.encoder.encode(
        `event: open\ndata: ${JSON.stringify({ connectionId })}\n\n`,
      );

      await writer.write(initMessage);

      request.signal?.addEventListener('abort', () => {
        const session = this.sessions.get(connectionId);
        if (session) {
          try {
            session.close();
          } catch (error) {
            // Ignore close failures
          }
          this.sessions.delete(connectionId);
        }
      });

      return new Response(readable, { headers });
    }

    return new Response('Not found', { status: 404 });
  }

  async broadcast(entries) {
    if (!entries.length || this.sessions.size === 0) {
      return;
    }

    const payload = this.encoder.encode(
      `data: ${JSON.stringify(entries)}\n\n`,
    );

    const toRemove = [];

    for (const [id, writer] of this.sessions.entries()) {
      try {
        await writer.write(payload);
      } catch (error) {
        toRemove.push(id);
      }
    }

    for (const id of toRemove) {
      const writer = this.sessions.get(id);
      try {
        writer?.close?.();
      } catch (error) {
        // Ignore release errors
      }
      this.sessions.delete(id);
    }
  }
}

async function persistEntries(env, newEntries) {
  const raw = await env.RSS_KV.get('latest');
  const existing = raw ? JSON.parse(raw) : [];

  const combined = [...newEntries, ...existing];
  const seen = new Set();
  const deduped = [];

  for (const entry of combined) {
    const key = entry.id || entry.guid || entry.link;
    if (!key || seen.has(key)) {
      continue;
    }
    seen.add(key);
    deduped.push(entry);
  }

  deduped.sort((a, b) => {
    const timeA = Date.parse(a.published || a.updated || a.receivedAt || 0);
    const timeB = Date.parse(b.published || b.updated || b.receivedAt || 0);
    return timeB - timeA;
  });

  const limited = deduped.slice(0, 100);

  await env.RSS_KV.put('latest', JSON.stringify(limited));
}

function parseFeed(xml, topicHint) {
  try {
    const parser = new DOMParser();
    const doc = parser.parseFromString(xml, 'text/xml');

    const channelTitle =
      doc.querySelector('channel > title')?.textContent?.trim() ||
      doc.querySelector('feed > title')?.textContent?.trim() ||
      topicHint ||
      'Unknown Source';

    const nodes = [
      ...doc.querySelectorAll('item'),
      ...doc.querySelectorAll('entry'),
    ];

    const entries = nodes.map((node) => {
      const title =
        node.querySelector('title')?.textContent?.trim() || 'Untitled';
      const link =
        node.querySelector('link[rel="alternate"]')?.getAttribute('href') ||
        node.querySelector('link')?.textContent?.trim() ||
        node.querySelector('link')?.getAttribute('href') ||
        '';
      const guid =
        node.querySelector('guid')?.textContent?.trim() ||
        node.querySelector('id')?.textContent?.trim() ||
        link;
      const summary =
        node.querySelector('summary')?.textContent?.trim() ||
        node.querySelector('description')?.textContent?.trim() ||
        '';
      const published =
        node.querySelector('published')?.textContent?.trim() ||
        node.querySelector('updated')?.textContent?.trim() ||
        node.querySelector('pubDate')?.textContent?.trim() ||
        new Date().toISOString();

      return {
        id: guid,
        title,
        link,
        summary,
        source: channelTitle,
        published,
        receivedAt: new Date().toISOString(),
      };
    });

    return entries;
  } catch (error) {
    console.error('Failed to parse feed payload', error);
    return [];
  }
}
