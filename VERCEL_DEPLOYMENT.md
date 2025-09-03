# 🚀 Vercel Deployment Guide

This guide explains how to deploy your YOLOv10 Object Detection app to Vercel and why the backend needed to be converted to serverless functions.

## 🔄 What Changed

### Before (Flask Backend)
- Flask server running on localhost:5000
- Heavy ML models running on the same server
- Not compatible with Vercel's serverless environment

### After (Vercel Serverless)
- React frontend served as static files
- Backend converted to Vercel serverless functions
- ML processing moved to mock functions (can be replaced with external ML services)

## 📁 New File Structure

```
cv/
├── api/                          # Vercel serverless functions
│   ├── upload.js                # Image upload handler
│   └── health.js                # Health check endpoint
├── web/                         # React frontend (unchanged)
├── vercel.json                  # Vercel configuration
├── package.json                 # Root package.json for Vercel
└── README.md
```

## 🚀 Deployment Steps

### 1. Install Vercel CLI
```bash
npm install -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Deploy to Vercel
```bash
vercel
```

### 4. Follow the prompts:
- Set up and deploy: `Y`
- Which scope: Select your account
- Link to existing project: `N`
- Project name: `yolov10-app` (or your preferred name)
- Directory: `.` (current directory)
- Override settings: `N`

### 5. Deploy to Production
```bash
vercel --prod
```

## 🔧 Configuration Files

### vercel.json
- Configures builds for React frontend and Node.js API functions
- Sets up routing between frontend and API
- Configures function timeouts

### Root package.json
- Manages dependencies for serverless functions
- Provides build scripts for Vercel

## 🌐 API Endpoints

After deployment, your API will be available at:
- **Upload**: `https://your-domain.vercel.app/api/upload`
- **Health**: `https://your-domain.vercel.app/api/health`

## ⚠️ Important Notes

### ML Model Limitations
- **Current**: Mock YOLO detection (for demo purposes)
- **Production**: Replace with external ML service (Google Cloud Vision, AWS Rekognition, etc.)

### File Upload
- Files are processed in memory (Vercel's temp directory)
- Maximum file size: 16MB
- Supported formats: JPG, PNG, GIF, BMP

### Cold Starts
- Serverless functions may have cold start delays
- Consider using Vercel Pro for better performance

## 🔄 Updating the ML Backend

To use real YOLO detection, you have several options:

### Option 1: External ML Service
```javascript
// In api/upload.js, replace mockYoloDetection with:
async function realYoloDetection(imageBuffer) {
  const response = await fetch('https://your-ml-service.com/detect', {
    method: 'POST',
    body: imageBuffer,
    headers: { 'Content-Type': 'application/octet-stream' }
  });
  return response.json();
}
```

### Option 2: Separate Backend Service
- Deploy Flask app to Railway, Render, or Heroku
- Update frontend to call external backend
- Keep Vercel for frontend only

### Option 3: Edge Functions
- Use Vercel Edge Functions for lighter ML processing
- Limited by Edge Runtime constraints

## 🧪 Testing Locally

### 1. Install dependencies
```bash
npm install
cd web && npm install
```

### 2. Test API functions
```bash
vercel dev
```

### 3. Test frontend
```bash
cd web && npm start
```

## 📊 Monitoring

- **Vercel Dashboard**: Monitor function performance and errors
- **Function Logs**: View serverless function execution logs
- **Analytics**: Track API usage and performance

## 🚨 Troubleshooting

### Common Issues

**Build Failures**
```bash
# Clear cache and rebuild
vercel --force
rm -rf .vercel
vercel
```

**API Timeouts**
- Increase `maxDuration` in vercel.json
- Optimize function performance
- Consider external ML service

**CORS Issues**
- CORS is handled by Vercel automatically
- Check if frontend is calling correct API endpoints

**File Upload Errors**
- Verify file size limits
- Check supported file types
- Ensure proper FormData usage

## 🔗 Useful Links

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Serverless Functions](https://vercel.com/docs/concepts/functions)
- [Vercel CLI](https://vercel.com/docs/cli)
- [Formidable.js](https://github.com/node-formidable/formidable)

## 🎯 Next Steps

1. **Deploy to Vercel** using the steps above
2. **Test the deployment** with sample images
3. **Replace mock ML** with real service when ready
4. **Monitor performance** in Vercel dashboard
5. **Set up custom domain** if needed

---

**Your app is now Vercel-ready! 🎉**
