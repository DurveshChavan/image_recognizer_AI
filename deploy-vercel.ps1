Write-Host "🚀 Deploying YOLOv10 App to Vercel..." -ForegroundColor Green
Write-Host ""

Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
npm install
Set-Location web
npm install
Set-Location ..

Write-Host ""
Write-Host "🔧 Building React app..." -ForegroundColor Yellow
Set-Location web
npm run build
Set-Location ..

Write-Host ""
Write-Host "🚀 Deploying to Vercel..." -ForegroundColor Yellow
vercel --prod

Write-Host ""
Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host "🌐 Your app should be available at the URL shown above" -ForegroundColor Cyan
Read-Host "Press Enter to continue"
