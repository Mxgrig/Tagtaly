# Image API Integration Setup

This guide explains how to integrate real images from NYTimes API and Pexels API into the dashboard.

## Overview

The `index.html` now includes real API integration to fetch:
1. **NYTimes API**: Top news articles with high-quality images
2. **Pexels API**: High-quality stock photography relevant to trending topics

## Step 1: Get NYTimes API Key

1. Go to [NYTimes Developer Portal](https://developer.nytimes.com/)
2. Sign up or log in with your NYTimes account
3. Create a new app:
   - Click "Create a new App"
   - Select "Article Search API"
   - Accept terms and create
4. Copy your API key
5. Update `index.html` line 1372:
   ```javascript
   const NYTIMES_API_KEY = 'your-key-here'; // Replace 'demo' with actual key
   ```

**Note**: NYTimes API has rate limits:
- Free tier: 10 requests per second, 4,000 per day
- Images are extracted from article multimedia field

## Step 2: Get Pexels API Key

1. Go to [Pexels API](https://www.pexels.com/api/)
2. Sign up with email or OAuth
3. Create an application:
   - Fill in basic info
   - Agree to terms
   - Generate authorization token
4. Copy your API key
5. Update `index.html` line 1373:
   ```javascript
   const PEXELS_API_KEY = 'your-key-here'; // Replace 'demo' with actual key
   ```

**Note**: Pexels API is generous:
- Free tier: 200 requests per hour
- Returns high-quality, royalty-free stock photos
- No attribution required but included in code

## Step 3: Security Best Practices

**⚠️ WARNING**: Storing API keys in client-side JavaScript is a security risk!

### Option A: Backend Proxy (Recommended for Production)

Create a Python backend endpoint to proxy API calls:

```python
# api_proxy.py
from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

NYTIMES_API_KEY = os.getenv('NYTIMES_API_KEY')
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')

@app.route('/api/images/nytimes')
def get_nytimes_image():
    # Proxy request to NYTimes API
    url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
    params = {
        'q': 'UK news',
        'sort': 'newest',
        'api-key': NYTIMES_API_KEY
    }
    response = requests.get(url, params=params)
    return jsonify(response.json())

@app.route('/api/images/pexels')
def get_pexels_image():
    # Proxy request to Pexels API
    url = 'https://api.pexels.com/v1/search'
    params = {
        'query': 'news photography',
        'per_page': 1
    }
    headers = {'Authorization': PEXELS_API_KEY}
    response = requests.get(url, params=params, headers=headers)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(port=5000)
```

Then update `index.html` to call local endpoints:
```javascript
// Instead of direct API calls:
const nytResponse = await fetch('/api/images/nytimes');
const pexelsResponse = await fetch('/api/images/pexels');
```

### Option B: Environment Variables

For development, store keys in `.env`:
```bash
NYTIMES_API_KEY=your-key-here
PEXELS_API_KEY=your-key-here
```

Build process would inject these at compile time.

### Option C: Keep in index.html (Current - Development Only)

Current implementation works for development/testing but should be replaced before production deployment.

## Step 4: Testing

1. Add your API keys to `index.html`
2. Open browser DevTools (F12)
3. Check Console tab
4. Reload page
5. Look for logs:
   - `✅ Loaded NYTimes image` - Banner image loaded from NYTimes
   - `✅ Loaded Pexels image` - Article image loaded from Pexels
   - `✅ Using Unsplash fallback` - API failed, using backup image

## Step 5: Troubleshooting

### CORS Errors
- Error: `No 'Access-Control-Allow-Origin' header`
- Solution: Use backend proxy approach (Option A above)

### Rate Limit Exceeded
- Error: `401 Unauthorized` or `429 Too Many Requests`
- Solution: Upgrade API plan or implement request caching

### No Images Found
- Issue: API returns empty results
- Solution: Check console logs for specific error messages
- Try different search query in code

### Images Not Displaying
- Clear browser cache (Ctrl+Shift+R)
- Check if image URLs are valid in browser
- Verify image element IDs match (`nytimes-banner`, `pexels-image`)

## Performance Optimization

### Caching
Add to `index.html` to cache image URLs:
```javascript
// Store in localStorage to avoid repeated API calls
const cacheKey = `featured_images_${new Date().toDateString()}`;
const cached = localStorage.getItem(cacheKey);
if (cached) {
    // Use cached images
}
```

### Progressive Enhancement
Images load after DOMContentLoaded, allowing page to render while APIs load.

## API Response Format

### NYTimes Response
```json
{
  "response": {
    "docs": [{
      "headline": {"main": "Article Title"},
      "multimedia": [{
        "type": "image",
        "subtype": "xlarge",
        "url": "path/to/image.jpg"
      }]
    }]
  }
}
```

### Pexels Response
```json
{
  "photos": [{
    "src": {
      "landscape": "https://...image.jpg"
    },
    "photographer": "John Doe",
    "alt": "Description"
  }]
}
```

## Cost Considerations

- **NYTimes**: Free tier includes 4,000 requests/day
- **Pexels**: Free tier includes 200 requests/hour
- Both APIs are free for production use

## Next Steps

1. Get API keys from both services
2. Update `index.html` with your keys
3. Test in development
4. For production: implement backend proxy (Option A)
5. Monitor API usage and consider caching strategies
