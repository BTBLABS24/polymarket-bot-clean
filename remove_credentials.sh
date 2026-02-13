#!/bin/bash
# Remove exposed Telegram credentials from all files

echo "Removing exposed Telegram credentials..."

# Replace in all .md files
find . -name "*.md" -type f -exec sed -i.bak 's/YOUR_TELEGRAM_BOT_TOKEN/YOUR_TELEGRAM_BOT_TOKEN/g' {} \;
find . -name "*.md" -type f -exec sed -i.bak 's/YOUR_TELEGRAM_CHAT_ID/YOUR_TELEGRAM_CHAT_ID/g' {} \;

# Replace in shell scripts
find . -name "*.sh" -type f -exec sed -i.bak 's/YOUR_TELEGRAM_BOT_TOKEN/YOUR_TELEGRAM_BOT_TOKEN/g' {} \;
find . -name "*.sh" -type f -exec sed -i.bak 's/YOUR_TELEGRAM_CHAT_ID/YOUR_TELEGRAM_CHAT_ID/g' {} \;

# Remove backup files
find . -name "*.bak" -delete

echo "Done! Credentials removed from all files."
echo ""
echo "⚠️  IMPORTANT: You need to:"
echo "1. Regenerate your Telegram bot token (it's exposed in git history)"
echo "2. Make the GitHub repo private"
echo "3. Update your .env file with new credentials"
