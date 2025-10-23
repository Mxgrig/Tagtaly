# API Keys Reference Guide

## Quick Links

### NYTimes API
- **Sign Up**: https://developer.nytimes.com/
- **Rate Limit**: 4,000 requests/day (FREE)
- **API Endpoint**: `https://api.nytimes.com/svc/search/v2/articlesearch.json`
- **Documentation**: https://developer.nytimes.com/docs/article-search-product/1/overview
- **Where to Add**: index.html line 1372

### Pexels API
- **Sign Up**: https://www.pexels.com/api/
- **Rate Limit**: 200 requests/hour (FREE)
- **API Endpoint**: `https://api.pexels.com/v1/search`
- **Documentation**: https://www.pexels.com/api/documentation/
- **Where to Add**: index.html line 1373

## Step-by-Step Setup

### For NYTimes

1. Go to: https://developer.nytimes.com/
2. Sign up with email
3. Log in to developer account
4. Click "Create a new App"
5. Select "Article Search API"
6. Fill in app name (e.g., "Tagtaly Dashboard")
7. Accept terms
8. Copy your API Key (looks like: `xxxxxxxxxxxxx1a2b3c4d5e6f`)
9. Open `index.html` and find line 1372:
   ```javascript
   const NYTIMES_API_KEY = 'demo';
   ```
10. Replace with:
    ```javascript
    const NYTIMES_API_KEY = 'xxxxxxxxxxxxx1a2b3c4d5e6f';
    ```

### For Pexels

1. Go to: https://www.pexels.com/api/
2. Sign up (email or OAuth)
3. Check "I agree to terms" and submit
4. Copy your API Key (looks like: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)
5. Open `index.html` and find line 1373:
   ```javascript
   const PEXELS_API_KEY = 'demo';
   ```
6. Replace with:
   ```javascript
   const PEXELS_API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx';
   ```

## Testing Your Keys

### In Browser Console

```javascript
// Test NYTimes API
const nytUrl = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?q=UK%20news&sort=newest&api-key=YOUR_KEY';
fetch(nytUrl)
  .then(r => r.json())
  .then(d => console.log('NYTimes OK:', d.response?.docs?.length, 'articles'))
  .catch(e => console.error('NYTimes Error:', e.message));

// Test Pexels API
const pexUrl = 'https://api.pexels.com/v1/search?query=news&per_page=1';
fetch(pexUrl, {headers: {'Authorization': 'YOUR_KEY'}})
  .then(r => r.json())
  .then(d => console.log('Pexels OK:', d.photos?.length, 'photos'))
  .catch(e => console.error('Pexels Error:', e.message));
```

## For Production (Environment Variables)

### Method 1: Using .env file

1. Create `.env` file in project root:
   ```
   NYTIMES_API_KEY=your-key-here
   PEXELS_API_KEY=your-key-here
   ```

2. Run proxy server:
   ```bash
   python3 image_api_proxy.py
   ```

3. Proxy server automatically reads from .env

### Method 2: Using System Environment Variables

```bash
export NYTIMES_API_KEY='your-key-here'
export PEXELS_API_KEY='your-key-here'
python3 image_api_proxy.py
```

### Method 3: Using Docker

```bash
docker run \
  -e NYTIMES_API_KEY='your-key-here' \
  -e PEXELS_API_KEY='your-key-here' \
  -p 8001:8001 \
  tagtaly-proxy
```

## Rate Limits & Usage

| API | Limit | Reset |
|-----|-------|-------|
| NYTimes | 4,000/day | Midnight EST |
| Pexels | 200/hour | Rolling hour |

For Tagtaly dashboard:
- Images load once per page view
- Typical usage: ~10-20 requests/day
- **Well within free tier** ✓

## Troubleshooting

### "Invalid API key" Error
- Double-check you copied entire key
- Verify no extra spaces or characters
- Try logging into respective API dashboard

### CORS Errors
- This happens with direct browser API calls
- **Solution**: Use backend proxy (`image_api_proxy.py`)
- Proxy server handles CORS automatically

### 401 Unauthorized
- API key is invalid or not set
- Or API key for wrong service (don't mix them up!)
- Check you're using the correct key for each API

### No Images Found
- Normal! Happens if search returns no results
- System falls back to Unsplash images
- Try different search query if needed

### Rate Limit Hit
- NYTimes: 4,000/day limit reached
- Pexels: 200/hour limit reached
- Wait for reset or upgrade API plan
- Consider caching images locally

## API Response Examples

### NYTimes Success Response

```json
{
  "response": {
    "docs": [{
      "headline": {"main": "Article Title"},
      "multimedia": [{
        "type": "image",
        "subtype": "xlarge",
        "url": "images/2025/10/22/image.jpg"
      }]
    }]
  }
}
```

### Pexels Success Response

```json
{
  "photos": [{
    "id": 123456,
    "width": 4000,
    "height": 2667,
    "src": {
      "landscape": "https://images.pexels.com/photos/123456/...",
      "large": "https://..."
    },
    "photographer": "Jane Doe",
    "alt": "Descriptive text"
  }]
}
```

## Security Notes

### Development (Current)
- Keys stored in index.html
- Fine for testing/development
- **Don't commit to public repo!**

### Production (Recommended)
- Keys stored in `.env` file
- Never commit `.env` file
- Use environment variables only
- Use backend proxy to hide keys
- See `image_api_proxy.py` for implementation

## Need Help?

- See: IMAGE_API_SETUP.md (detailed guide)
- See: QUICKSTART_IMAGES.md (quick 5-min setup)
- Check: VERIFICATION_CHECKLIST.md (verify everything works)
- Read: index.html lines 1369-1516 (code implementation)

## Support Resources

### NYTimes Developer
- Docs: https://developer.nytimes.com/docs/article-search-product
- Forum: https://github.com/nytimes/developer-portal/discussions
- Status: https://status.nytimes.com/

### Pexels Developer
- Docs: https://www.pexels.com/api/documentation/
- GitHub: https://github.com/pexels/pexels-api
- Email: api@pexels.com

---

**Last Updated**: October 22, 2025
**Status**: Complete and Ready
