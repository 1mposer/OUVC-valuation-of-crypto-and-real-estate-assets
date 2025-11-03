# 🔐 Secure Configuration Directory

This directory contains sensitive API keys and credentials for the OUVC project.

## ⚠️ IMPORTANT SECURITY NOTES

1. **Never commit this directory to version control**
   - This directory is included in `.gitignore`
   - Double-check before any git commits

2. **Restrict file permissions**
   - On Unix systems: `chmod 700 secure_config/`
   - API keys file: `chmod 600 secure_config/api_keys.env`

3. **Do not share these files**
   - Never email or share API keys
   - Don't include in documentation or screenshots

## 📝 Setup Instructions

1. Copy `api_keys.env.template` to `api_keys.env`:
   ```bash
   cp api_keys.env.template api_keys.env
   ```

2. Edit `api_keys.env` with your actual API keys

3. Run the application - it will automatically load from this file

## 🔑 Required API Keys

### Bayut API (Dubai Property Data)
- **Where to get**: [RapidAPI - Bayut](https://rapidapi.com/apidojo/api/bayut/)
- **Required for**: Dubai property analysis
- **Key name**: `BAYUT_API_KEY`
- **Cost**: Free tier available

### CoinGecko API (Cryptocurrency Data)
- **Where to get**: [CoinGecko API](https://www.coingecko.com/en/api)
- **Required for**: Crypto analysis
- **Key name**: `COINGECKO_API_KEY`
- **Cost**: Free tier available (30 calls/min)

### Optional APIs
- **DLD_API_KEY**: Dubai Land Department (if you have access)
- **NEWS_API_KEY**: For market sentiment analysis (future feature)

## 🧪 Demo Mode

If you don't have API keys yet, you can run the application in demo mode:
- The system will use sample data
- Select option 3 (Demo Mode) in the main menu
- No API keys required

## 🛠️ Troubleshooting

**Keys not loading?**
- Check file permissions: `ls -la secure_config/`
- Ensure no spaces around `=` in the env file
- Verify file is named exactly `api_keys.env`

**Permission denied errors?**
- On Unix: `chmod 700 secure_config && chmod 600 secure_config/api_keys.env`
- On Windows: Right-click folder → Properties → Security

## 📂 File Structure
```
secure_config/
├── README.md              # This file
├── api_keys.env.template  # Template with placeholders
└── api_keys.env          # Your actual keys (gitignored)
```
