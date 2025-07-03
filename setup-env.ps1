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

# Check if credentials.json exists
if (Test-Path "server/credentials.json") {
    Write-Host "Warning: server/credentials.json already exists!" -ForegroundColor Yellow
    $response = Read-Host "Do you want to overwrite it? (y/N)"
    if ($response -ne "y" -and $response -ne "Y") {
        Write-Host "Skipping credentials.json setup." -ForegroundColor Yellow
    } else {
        if (Test-Path "server/credentials.example.json") {
            Copy-Item "server/credentials.example.json" "server/credentials.json" -Force
            Write-Host "✓ Created server/credentials.json from server/credentials.example.json" -ForegroundColor Green
        } else {
            Write-Host "✗ server/credentials.example.json not found!" -ForegroundColor Red
        }
    }
} else {
    if (Test-Path "server/credentials.example.json") {
        Copy-Item "server/credentials.example.json" "server/credentials.json" -Force
        Write-Host "✓ Created server/credentials.json from server/credentials.example.json" -ForegroundColor Green
    } else {
        Write-Host "✗ server/credentials.example.json not found!" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Setup completed!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env file with your actual credentials" -ForegroundColor White
Write-Host "2. Edit server/credentials.json with your actual credentials (if using file-based config)" -ForegroundColor White
Write-Host "3. Run: docker-compose up --build" -ForegroundColor White
Write-Host ""
Write-Host "For more information, see README.CREDENTIALS.md" -ForegroundColor Cyan 