# Setup Environment Script for GiveAndTake
# This script helps you set up your environment files for development

Write-Host "Setting up GiveAndTake environment files..." -ForegroundColor Green

# Check if .env exists
if (Test-Path ".env") {
    Write-Host "Warning: .env file already exists!" -ForegroundColor Yellow
    $response = Read-Host "Do you want to overwrite it? (y/N)"
    if ($response -ne "y" -and $response -ne "Y") {
        Write-Host "Setup cancelled." -ForegroundColor Red
        exit
    }
}

# Copy .env.example to .env
if (Test-Path ".env.example") {
    Copy-Item ".env.example" ".env" -Force
    Write-Host "✓ Created .env file from .env.example" -ForegroundColor Green
} else {
    Write-Host "✗ .env.example not found!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Setup completed!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env file with your actual configuration" -ForegroundColor White
Write-Host "2. Run: docker-compose up --build" -ForegroundColor White 