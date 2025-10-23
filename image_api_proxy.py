#!/usr/bin/env python3
"""
Image API Proxy Server
Securely proxies requests to NYTimes and Pexels APIs
Stores API keys server-side (not exposed to client)
"""

import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import urllib.request
import urllib.error

# API Keys (get from environment variables for security)
NYTIMES_API_KEY = os.getenv('NYTIMES_API_KEY', 'demo')
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY', 'demo')

class APIProxyHandler(BaseHTTPRequestHandler):
    """Handle HTTP requests and proxy to external APIs"""

    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)

        # Enable CORS
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.end_headers()

        try:
            if path == '/api/images/nytimes':
                response = self._fetch_nytimes_image()
                self.wfile.write(json.dumps(response).encode())

            elif path == '/api/images/pexels':
                response = self._fetch_pexels_image()
                self.wfile.write(json.dumps(response).encode())

            elif path == '/api/health':
                self.wfile.write(json.dumps({
                    'status': 'ok',
                    'nytimes_configured': NYTIMES_API_KEY != 'demo',
                    'pexels_configured': PEXELS_API_KEY != 'demo'
                }).encode())

            else:
                self.wfile.write(json.dumps({
                    'error': 'Endpoint not found'
                }).encode())

        except Exception as e:
            self.wfile.write(json.dumps({
                'error': str(e)
            }).encode())

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

    def _fetch_nytimes_image(self):
        """Fetch image from NYTimes Article Search API"""
        if NYTIMES_API_KEY == 'demo':
            return {'error': 'NYTimes API key not configured'}

        try:
            search_query = 'UK news'
            url = (
                f'https://api.nytimes.com/svc/search/v2/articlesearch.json'
                f'?q={search_query}&sort=newest&api-key={NYTIMES_API_KEY}'
            )

            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read())

                # Find first article with image
                if 'response' in data and 'docs' in data['response']:
                    for article in data['response']['docs']:
                        if 'multimedia' in article and article['multimedia']:
                            for media in article['multimedia']:
                                if media.get('type') == 'image' and media.get('subtype') == 'xlarge':
                                    return {
                                        'url': f"https://static01.nyt.com/{media['url']}",
                                        'alt': article.get('headline', {}).get('main', 'NYTimes news'),
                                        'source': 'NYTimes'
                                    }

                return {'error': 'No images found in NYTimes articles'}

        except urllib.error.HTTPError as e:
            return {'error': f'NYTimes API error: {e.code}'}
        except Exception as e:
            return {'error': f'NYTimes fetch failed: {str(e)}'}

    def _fetch_pexels_image(self):
        """Fetch image from Pexels API"""
        if PEXELS_API_KEY == 'demo':
            return {'error': 'Pexels API key not configured'}

        try:
            url = 'https://api.pexels.com/v1/search?query=news%20photography&per_page=1'

            req = urllib.request.Request(url)
            req.add_header('Authorization', PEXELS_API_KEY)

            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read())

                if 'photos' in data and data['photos']:
                    photo = data['photos'][0]
                    return {
                        'url': photo['src']['landscape'],
                        'alt': photo.get('alt', 'Stock photo'),
                        'photographer': photo.get('photographer', 'Unknown'),
                        'source': 'Pexels'
                    }

                return {'error': 'No images found on Pexels'}

        except urllib.error.HTTPError as e:
            return {'error': f'Pexels API error: {e.code}'}
        except Exception as e:
            return {'error': f'Pexels fetch failed: {str(e)}'}


def run_server(host='localhost', port=8001):
    """Run the API proxy server"""
    server_address = (host, port)
    httpd = HTTPServer(server_address, APIProxyHandler)

    print(f'🚀 Image API Proxy running at http://{host}:{port}')
    print(f'📝 NYTimes API configured: {NYTIMES_API_KEY != "demo"}')
    print(f'📝 Pexels API configured: {PEXELS_API_KEY != "demo"}')
    print(f'🔗 Health check: http://{host}:{port}/api/health')
    print()
    print('Available endpoints:')
    print(f'  GET http://{host}:{port}/api/images/nytimes')
    print(f'  GET http://{host}:{port}/api/images/pexels')
    print()
    print('Press Ctrl+C to stop')

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n✅ Server stopped')
        httpd.server_close()


if __name__ == '__main__':
    run_server()
