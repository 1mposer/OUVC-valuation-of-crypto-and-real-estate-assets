# 🔒 Security Checklist for OUVC Project

## ✅ Before Each Commit

- [ ] Run `git status` and verify no sensitive files are staged
- [ ] Check that `.env` and `api_keys.env` are NOT in the commit
- [ ] Verify `secure_config/api_keys.env` is gitignored
- [ ] Review all changed files for hardcoded credentials
- [ ] Ensure no API keys in code comments or print statements

## 🔐 API Key Security

- [ ] All API keys stored in `secure_config/api_keys.env`
- [ ] Template file (`api_keys.env.template`) contains only placeholders
- [ ] No API keys hardcoded in Python files
- [ ] File permissions set: `chmod 600 secure_config/api_keys.env` (Unix)
- [ ] Directory permissions set: `chmod 700 secure_config/` (Unix)

## 📁 Files That Should NEVER Be Committed

### Critical - Contains Actual Secrets
- `secure_config/api_keys.env`
- `.env`
- `*.key`
- `*.pem`
- `credentials.json`

### Safe - Templates Only
- ✅ `secure_config/api_keys.env.template` - Safe to commit (placeholders only)
- ✅ `.env.template` - Safe to commit (placeholders only)
- ✅ `secure_config/README.md` - Safe to commit (documentation)
- ✅ `secure_config/.gitkeep` - Safe to commit (directory structure)

## 🛡️ Best Practices

### For Development
1. **Never log API keys** - Check all print/log statements
2. **Use environment variables** - Don't hardcode in source
3. **Rotate keys regularly** - Change keys every 3-6 months
4. **Use read-only keys** - When possible, use keys with minimal permissions
5. **Test in demo mode first** - Verify logic before using real keys

### For Production
1. **Use separate keys** - Different keys for dev/staging/production
2. **Enable key restrictions** - Restrict by IP/domain when possible
3. **Monitor usage** - Set up alerts for unusual activity
4. **Use secrets management** - Consider AWS Secrets Manager, HashiCorp Vault
5. **Regular audits** - Review access logs and key usage

### For Collaboration
1. **Share keys securely** - Use 1Password, LastPass, or similar
2. **Document key ownership** - Know who has which keys
3. **Revoke on departure** - Rotate keys when team members leave
4. **Limit distribution** - Only share keys with those who need them

## 🚨 Emergency Response

### If You Accidentally Commit a Secret:

1. **Immediately revoke/regenerate** the exposed key
2. **Don't just delete the file** - It's still in git history
3. **Use git-filter-branch or BFG Repo-Cleaner** to remove from history
4. **Force push** to remote (if you have permission)
5. **Notify team members** to re-clone the repository
6. **Review access logs** for unauthorized usage

### Commands to Check History:
```bash
# Search all commits for potential secrets
git log -p -S 'BAYUT_API_KEY' --all

# Search for files that might contain secrets
git log --all --full-history -- "*api_keys*"

# Use git-secrets to prevent commits
git secrets --scan
```

## 🔍 Verification Commands

### Check if secrets are properly gitignored:
```bash
# Should return nothing (empty)
git check-ignore secure_config/api_keys.env
git check-ignore .env

# List all ignored files
git status --ignored
```

### Verify no secrets in staged files:
```bash
# Before committing
git diff --cached | grep -i "api_key"
git diff --cached | grep -i "password"
git diff --cached | grep -i "secret"
```

### Check file permissions (Unix):
```bash
ls -la secure_config/
# Should show: drwx------ (700) for directory
# Should show: -rw------- (600) for api_keys.env
```

## 📚 Additional Resources

- [GitHub: Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [git-secrets tool](https://github.com/awslabs/git-secrets)
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)
- [OWASP API Security](https://owasp.org/www-project-api-security/)

## 🎯 Quick Reference

### Safe to commit:
- Source code (*.py)
- Templates (*.template, *.env.template)
- Documentation (*.md, *.txt)
- Configuration (requirements.txt, setup.sh)
- Empty directories (.gitkeep)

### NEVER commit:
- API keys (api_keys.env, .env)
- Credentials (*.pem, *.key, credentials.*)
- Database dumps (*.sql, *.db)
- User data (data/, *.csv with PII)
- Cache files (*.cache, __pycache__/)

---

**Last Updated**: 2025-11-03
**Review Frequency**: Before each commit and monthly audit
