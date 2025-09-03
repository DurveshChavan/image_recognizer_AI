@echo off
echo 🚀 Deploying YOLOv10 App to Vercel...
echo.

echo 📦 Installing dependencies...
npm install
cd web
npm install
cd ..

echo.
echo 🔧 Building React app...
cd web
npm run build
cd ..

echo.
echo 🚀 Deploying to Vercel...
vercel --prod

echo.
echo ✅ Deployment complete!
echo 🌐 Your app should be available at the URL shown above
pause
