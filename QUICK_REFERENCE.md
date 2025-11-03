# 🔐 Quick Reference: Secure API Keys Setup

## ⚡ Quick Start (3 Steps)

```bash
# 1. Create your API keys file
cp secure_config/api_keys.env.template secure_config/api_keys.env

# 2. Edit and add your actual keys
nano secure_config/api_keys.env

# 3. Set secure permissions
chmod 600 secure_config/api_keys.env
```

## 🔑 Get API Keys

| Service | URL | Required? |
|---------|-----|-----------|
| **Bayut** | https://rapidapi.com/apidojo/api/bayut/ | ✅ Yes (for properties) |
| **CoinGecko** | https://www.coingecko.com/en/api | ⚠️ Optional |

## 🧪 Test Without Keys

```bash
python3 main.py
# Select: 3 (Demo Mode)
```

## ✅ Verify Security

```bash
# Should output the filename (means it's ignored):
git check-ignore secure_config/api_keys.env

# Should NOT show any .env files:
git status

# Verify permissions (should be 700):
ls -ld secure_config/
```

## 🚨 Before Each Commit

```bash
# Check what you're committing:
git status
git diff

# Make sure no secrets:
git diff --cached | grep -i "api_key"
```

## 📂 Safe vs Unsafe Files

### ✅ SAFE to commit:
- `*.py` (source code)
- `*.template` (templates)
- `README.md` (docs)
- `requirements.txt`
- `.gitignore`

### ❌ NEVER commit:
- `api_keys.env`
- `.env`
- `*.key`, `*.pem`
- Any file with actual API keys

## 🆘 Emergency: I Committed a Secret!

```bash
# 1. Regenerate the key IMMEDIATELY at the provider
# 2. Remove from git history:
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch secure_config/api_keys.env" \
  --prune-empty --tag-name-filter cat -- --all

# 3. Force push (careful!)
git push origin --force --all
```

## 📋 File Structure

```
secure_config/
├── .gitkeep              ← Tracks directory (safe)
├── README.md             ← Documentation (safe)
├── api_keys.env.template ← Template (safe)
└── api_keys.env         ← YOUR KEYS (gitignored!)
```

## 💡 Pro Tips

1. **Demo Mode**: Test logic without real API keys
2. **Separate Keys**: Use different keys for dev/prod
3. **Check Often**: Run `git status` frequently
4. **Read Docs**: Check `SECURITY_CHECKLIST.md` for details

## 🔗 Full Documentation

- `SECURITY_SETUP_COMPLETE.md` - Complete setup guide
- `SECURITY_CHECKLIST.md` - Security best practices
- `secure_config/README.md` - API keys setup

---
**Quick help**: If stuck, open `SECURITY_SETUP_COMPLETE.md`
