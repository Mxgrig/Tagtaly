# Tagtaly RSS Worker

Cloudflare Worker that receives WebSub (PubSubHubbub) pushes from RSS hubs,
stores fresh articles, and streams them to the dashboard in real time.

## Overview

Routes:

| Method | Path        | Description |
| ------ | ----------- | ----------- |
| GET    | `/webhook`  | WebSub verification handshake (`hub.challenge`). |
| POST   | `/webhook`  | Receives feed payloads, normalizes entries, stores the latest 100 articles, and broadcasts them to connected clients. |
| GET    | `/feed`     | Returns cached articles as JSON. Used by the dashboard for initial load / fallback polling. |
| GET    | `/live`     | Server‑Sent Events stream that pushes new stories as they arrive. |

Storage / state:

- `RSS_KV` (Workers KV) keeps the latest 100 normalized entries.
- `FeedHub` (Durable Object) fans out real-time Server-Sent Events to connected browsers.

## Setup

1. **Install Wrangler**

   ```bash
   npm install -g wrangler
   ```

2. **Configure bindings**

   In `wrangler.toml` replace:

   - `ALLOWED_ORIGIN` with the origin that will host your dashboard (e.g. `https://mxgrig.github.io` or your Cloudflare Pages domain).
   - `RSS_KV.id` with an actual KV namespace ID created via `wrangler kv namespace create rss-feed`.

   Example:

   ```bash
   wrangler kv namespace create rss-feed
   ```

   Copy the resulting ID into the `id` field.

3. **Publish**

   ```bash
   cd cloudflare/rss-worker
   wrangler deploy
   ```

   Wrangler outputs the Worker URL (e.g. `https://tagtaly-rss-worker.example.workers.dev`).

4. **Subscribe feeds (WebSub)**

   Many publishers expose a `<link rel="hub">` element in their RSS/Atom feeds.
   For each feed:

   - Discover the hub URL.
   - POST to the hub:

     ```bash
     curl -X POST HUB_URL \
       -d "hub.mode=subscribe" \
       -d "hub.callback=https://tagtaly-rss-worker.example.workers.dev/webhook" \
       -d "hub.topic=FEED_URL" \
       -d "hub.verify=sync" \
       -d "hub.lease_seconds=864000"
     ```

   The Worker automatically handles the verification callback (`hub.challenge`).

   For feeds without WebSub support, add a Cloudflare Cron Trigger to poll the feed and `POST` it to `/webhook`.

## Local development

```bash
wrangler dev --remote
```

Use `--remote` so DOMParser / Durable Object APIs are available.

## Dashboard integration

- Initial load fetches `GET /feed`.
- Real-time updates connect to `GET /live` (SSE).
- Both endpoints respect `ALLOWED_ORIGIN` for CORS; update it if you serve the dashboard from a different domain.

See `docs/assets/js/live-feed.js` for the client integration.
