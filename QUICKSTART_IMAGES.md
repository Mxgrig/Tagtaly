# Quick Start: Real Image Integration

## What Changed?

The dashboard now fetches **real images** from two sources instead of placeholders:

1. **NYTimes API** → Banner image from top news stories
2. **Pexels API** → Article image from stock photography

## Current Status

✅ **Code is ready** - `index.html` has API integration
⏳ **Need API keys** - To make it work with real images

## Quick Setup (5 minutes)

### Option 1: Get Real API Keys (Recommended)

1. **NYTimes API Key**:
   - Visit: https://developer.nytimes.com/
   - Sign up → Create App → Select "Article Search API"
   - Copy your API key
   - Open `index.html` and find line ~1372
   - Replace `'demo'` with your key

2. **Pexels API Key**:
   - Visit: https://www.pexels.com/api/
   - Sign up → Create app → Get authorization token
   - Open `index.html` and find line ~1373
   - Replace `'demo'` with your key

3. **Test it**:
   - Open browser DevTools (F12)
   - Go to Console tab
   - Reload page
   - Look for: `✅ Loaded NYTimes image` or `✅ Loaded Pexels image`

### Option 2: Use Backend Proxy (Production Safe)

For security, use the proxy server provided:

```bash
# Set environment variables
export NYTIMES_API_KEY='your-key-here'
export PEXELS_API_KEY='your-key-here'

# Run proxy server
python3 image_api_proxy.py

# This starts server on http://localhost:8001
```

Then update `index.html` lines 1376-1377 to use local endpoints:
```javascript
// Instead of direct API calls, use local proxy:
const nytResponse = await fetch('/api/images/nytimes');
const pexelsResponse = await fetch('/api/images/pexels');
```

## What You'll See

### Before (Placeholder Images)
- Generic Unsplash images
- Same images every time
- No real news relevance

### After (Real API Images)
- **Banner**: Latest NYTimes news article image
- **Article**: Relevant Pexels stock photo
- Updates with fresh news daily
- Professional photo credits shown

## API Limits (Free Tier)

- **NYTimes**: 4,000 requests/day (plenty)
- **Pexels**: 200 requests/hour (plenty)
- Both are **free** for production use

## Testing Without Keys

The code will gracefully fall back to Unsplash images if APIs fail:
```
⏳ Fetching images from APIs...
⚠️ NYTimes API fetch failed: ...
⚠️ Pexels API fetch failed: ...
✅ Using Unsplash fallback banner
✅ Using Unsplash fallback for article image
```

This means the site works even without API keys!

## File Structure

```
Tagtaly/
├── index.html                 ← Main file with API integration (lines 1369-1516)
├── IMAGE_API_SETUP.md         ← Detailed setup guide
├── QUICKSTART_IMAGES.md       ← This file
├── image_api_proxy.py         ← Backend proxy server (for security)
└── .env.example               ← Template for API keys
```

## Next Steps

1. Get API keys (5 min)
2. Update `index.html` with your keys
3. Reload page in browser
4. Check Console to confirm images loaded
5. Deploy! (No special setup needed, fallbacks work)

## Troubleshooting

**Q: Images not loading?**
- Check browser Console (F12) for error messages
- Verify API keys are correct
- Try hard refresh: Ctrl+Shift+R

**Q: Getting CORS errors?**
- This is expected with direct API calls from browser
- Solution: Use backend proxy (`image_api_proxy.py`)
- Or deploy using environment variables

**Q: Want to use different image sources?**
- Edit lines 1379 & 1413 in `index.html`
- Change search query to anything relevant
- Example: `'UK politics'`, `'health news'`, etc.

## Code Locations

**Image loading function**: `index.html` lines 1369-1516
- `fetchNYTimesImage()` → Gets banner image
- `fetchPexelsImage()` → Gets article image
- `loadFeaturedImages()` → Orchestrates both + fallbacks

**API keys**: Lines 1372-1373
```javascript
const NYTIMES_API_KEY = 'demo';  // ← Update here
const PEXELS_API_KEY = 'demo';   // ← Update here
```

## Performance

- Async loading: Images load in parallel with page
- Timeout: 10 seconds per API call (graceful fallback)
- Caching: Not currently implemented (could add for production)
- Image size: Optimized for responsive design

## Security Notes

⚠️ **Current approach**: Keys stored in JavaScript (dev only)

For production:
1. Use backend proxy server (`image_api_proxy.py`)
2. Store keys in `.env` file (never commit!)
3. Access via environment variables
4. Frontend calls local `/api/` endpoints instead

See `IMAGE_API_SETUP.md` for detailed security guide.
