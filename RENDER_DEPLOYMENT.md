# 🚀 Deploy YOLOv10 Backend to Render

## Why Render?
- ✅ **Better for ML applications** than Railway
- ✅ **Longer build times** (no timeouts)
- ✅ **GPU support** available
- ✅ **Free tier** with generous limits
- ✅ **Automatic HTTPS** and custom domains

## 📋 Prerequisites
1. [Render Account](https://render.com) (free)
2. GitHub repository connected
3. Python 3.8+ support

## 🎯 Step-by-Step Deployment

### 1. Create Render Account
- Go to [render.com](https://render.com)
- Sign up with GitHub (recommended)
- Verify your email

### 2. Create New Web Service
- Click **"New +"** → **"Web Service"**
- Connect your GitHub repository
- Select the `cv` repository

### 3. Configure Service
```
Name: yolov10-backend
Environment: Python 3
Region: Choose closest to you
Branch: main (or your default branch)
Build Command: pip install -r requirements.txt
Start Command: python start.py
```

### 4. Environment Variables
Add these in the **Environment** section:
```
FLASK_DEBUG=False
PORT=10000
```

### 5. Plan Selection
- **Free Plan**: Good for testing (builds in ~15-20 minutes)
- **Starter Plan ($7/month)**: Faster builds, better performance
- **Pro Plan ($25/month)**: GPU support, fastest builds

### 6. Deploy
- Click **"Create Web Service"**
- Wait for build to complete (15-30 minutes for ML dependencies)
- Your backend will be available at: `https://your-app-name.onrender.com`

## 🔧 Troubleshooting

### Build Fails
- Check build logs in Render dashboard
- Ensure `requirements.txt` is in root directory
- Verify Python version compatibility

### Runtime Errors
- Check logs in Render dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify `start.py` path is correct

### Performance Issues
- Upgrade to paid plan for better performance
- Consider using GPU instances for ML workloads

## 🌐 After Deployment

1. **Get your backend URL** from Render dashboard
2. **Update React frontend** with the new backend URL
3. **Deploy React to Vercel**
4. **Test the connection**

## 📱 Frontend Integration

Update your React app to call the Render backend:

```javascript
const backendUrl = 'https://your-app-name.onrender.com';
const response = await fetch(`${backendUrl}/api/upload`, {
  method: 'POST',
  body: formData,
});
```

## 🎉 Success!

Your Flask backend will be running on Render with:
- ✅ **Automatic HTTPS**
- ✅ **Custom domain support**
- ✅ **Auto-deploy on Git push**
- ✅ **Built-in monitoring**
- ✅ **Scalability options**

## 💰 Cost
- **Free**: $0/month (limited builds, slower performance)
- **Starter**: $7/month (faster builds, better performance)
- **Pro**: $25/month (GPU support, fastest builds)

**Recommendation**: Start with free plan, upgrade if needed!
