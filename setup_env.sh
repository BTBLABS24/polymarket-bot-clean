#!/bin/bash
# Setup Environment Variables Helper Script

echo "=================================================="
echo "Polymarket Scanner - Environment Setup"
echo "=================================================="
echo ""

# Check if .env exists
if [ -f .env ]; then
    echo "⚠️  .env file already exists!"
    read -p "Overwrite? (y/N): " overwrite
    if [[ ! $overwrite =~ ^[Yy]$ ]]; then
        echo "Cancelled."
        exit 0
    fi
fi

# Create .env file
echo "Creating .env file..."
cp .env.example .env

# Get Alchemy API key
echo ""
echo "1. Alchemy API Key"
echo "   Get from: https://www.alchemy.com/"
echo "   Chain: Polygon, Network: Polygon Mainnet"
echo ""
read -p "Enter your Alchemy API key: " alchemy_key

if [ -z "$alchemy_key" ]; then
    echo "❌ Alchemy API key is required!"
    exit 1
fi

# Update .env file
sed -i.bak "s/ALCHEMY_API_KEY=.*/ALCHEMY_API_KEY=$alchemy_key/" .env
rm .env.bak 2>/dev/null

echo "✅ Alchemy API key saved"

# Telegram is already configured
echo ""
echo "2. Telegram Configuration"
echo "   Bot: @polyfebbot"
echo "   ✅ Already configured in .env"
echo ""

# Show final .env
echo "=================================================="
echo "✅ Environment configured!"
echo "=================================================="
echo ""
cat .env
echo ""
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Test setup: python3 test_setup.py"
echo "2. Run scanner: cd realtime_scanner && python3 main.py"
echo ""
echo "Or deploy to Railway:"
echo "1. Push to GitHub: git push"
echo "2. Deploy on Railway: https://railway.app"
echo "3. Add environment variables in Railway dashboard"
echo ""
