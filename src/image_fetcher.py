"""
Fetch images from NYTimes and Pexels APIs using environment variables.
Generates images.json for dashboard consumption (no hardcoding).
"""

import os
import json
import requests
from datetime import datetime


class ImageFetcher:
    """Fetch news images from secure API sources"""

    def __init__(self):
        self.nytimes_key = os.getenv('NYTIMES_API_KEY')
        self.pexels_key = os.getenv('PEXELS_API_KEY')
        self.output_dir = "social_dashboard/assets/data"
        os.makedirs(self.output_dir, exist_ok=True)

    def fetch_nytimes_articles(self, query="UK news", limit=5):
        """
        Fetch latest articles with images from NYTimes API
        
        Args:
            query: Search query (e.g., "UK news", "US politics")
            limit: Number of articles to fetch
            
        Returns:
            List of article dicts with image URLs
        """
        if not self.nytimes_key:
            print("   ⚠️  NYTIMES_API_KEY not set, skipping NYTimes images")
            return []

        try:
            url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
            params = {
                "q": query,
                "sort": "newest",
                "api-key": self.nytimes_key,
                "page": 0
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            articles = []
            for doc in data.get('response', {}).get('docs', [])[:limit]:
                # Extract image URL from multimedia array
                image_url = None
                for media in doc.get('multimedia', []):
                    if media.get('type') == 'image':
                        image_url = f"https://www.nytimes.com/{media.get('url', '')}"
                        break

                if image_url:
                    articles.append({
                        'source': 'NYTimes',
                        'headline': doc.get('headline', {}).get('main', 'News Article'),
                        'url': doc.get('web_url', ''),
                        'image': image_url,
                        'published': doc.get('pub_date', ''),
                    })

            return articles

        except Exception as e:
            print(f"   ⚠️  NYTimes API error: {str(e)}")
            return []

    def fetch_pexels_images(self, query="news", limit=10):
        """
        Fetch images from Pexels API for fallback/supplementary images
        
        Args:
            query: Search query (e.g., "news", "politics", "business")
            limit: Number of images to fetch
            
        Returns:
            List of image dicts
        """
        if not self.pexels_key:
            print("   ⚠️  PEXELS_API_KEY not set, skipping Pexels images")
            return []

        try:
            url = "https://api.pexels.com/v1/search"
            headers = {'Authorization': self.pexels_key}
            params = {
                'query': query,
                'per_page': limit,
                'page': 1
            }

            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            images = []
            for photo in data.get('photos', [])[:limit]:
                images.append({
                    'source': 'Pexels',
                    'title': photo.get('alt', 'Image'),
                    'url': photo['src'].get('large', ''),
                    'photographer': photo.get('photographer', 'Unknown'),
                    'photographer_url': photo.get('photographer_url', ''),
                })

            return images

        except Exception as e:
            print(f"   ⚠️  Pexels API error: {str(e)}")
            return []

    def get_banner_image(self):
        """
        Get primary banner image from NYTimes (with Pexels fallback)
        
        Returns:
            Dict with image URL and attribution
        """
        # Try NYTimes first
        nytimes_articles = self.fetch_nytimes_articles("news", limit=1)
        if nytimes_articles:
            article = nytimes_articles[0]
            return {
                'url': article['image'],
                'source': 'NYTimes',
                'title': article['headline'],
                'attribution': f"📷 {article['headline']} - NYTimes",
                'article_url': article['url']
            }

        # Fallback to Pexels
        pexels_images = self.fetch_pexels_images("news breaking", limit=1)
        if pexels_images:
            image = pexels_images[0]
            return {
                'url': image['url'],
                'source': 'Pexels',
                'title': image['title'],
                'attribution': f"📷 Image by {image['photographer']} - Pexels",
                'photographer_url': image['photographer_url']
            }

        # Ultimate fallback (no API keys available)
        return {
            'url': 'https://via.placeholder.com/1200x400?text=Tagtaly+News',
            'source': 'Placeholder',
            'title': 'News Dashboard',
            'attribution': '📷 Placeholder image'
        }

    def get_topic_images(self, topics):
        """
        Get relevant images for each topic
        
        Args:
            topics: List of topic names
            
        Returns:
            Dict mapping topics to image URLs
        """
        topic_images = {}
        pexels_images = self.fetch_pexels_images("business news economy", limit=20)

        for topic in topics[:10]:  # Limit to 10 topics
            # Try to find matching image from Pexels
            matching = next(
                (img for img in pexels_images 
                 if topic.lower() in img['title'].lower()),
                None
            )

            if matching:
                topic_images[topic] = {
                    'url': matching['url'],
                    'source': 'Pexels',
                    'photographer': matching['photographer']
                }
            else:
                # Use first available or placeholder
                if pexels_images:
                    img = pexels_images[0]
                    topic_images[topic] = {
                        'url': img['url'],
                        'source': 'Pexels',
                        'photographer': img['photographer']
                    }

        return topic_images

    def generate_images_json(self, topics=None):
        """
        Generate complete images.json file for dashboard
        
        Args:
            topics: List of topic names for images
            
        Returns:
            Path to generated JSON file
        """
        if topics is None:
            topics = ['Tech', 'Politics', 'Business', 'Health', 'Entertainment']

        print("\n🖼️  FETCHING IMAGES FOR DASHBOARD...")

        images_data = {
            'generated_at': datetime.now().isoformat(),
            'banner': self.get_banner_image(),
            'topics': self.get_topic_images(topics),
            'api_status': {
                'nytimes': 'configured' if self.nytimes_key else 'missing',
                'pexels': 'configured' if self.pexels_key else 'missing'
            }
        }

        # Save to JSON file
        output_file = os.path.join(self.output_dir, 'images.json')
        with open(output_file, 'w') as f:
            json.dump(images_data, f, indent=2)

        print(f"   ✅ Saved: {output_file}")
        print(f"   📰 Banner: {images_data['banner']['source']}")
        print(f"   🖼️  Topic images: {len(images_data['topics'])} topics")

        return output_file


if __name__ == "__main__":
    fetcher = ImageFetcher()
    topics = ['Tech', 'Politics', 'Business', 'Health', 'Entertainment', 'Science', 'Sports']
    fetcher.generate_images_json(topics)
