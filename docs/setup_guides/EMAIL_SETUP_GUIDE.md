# 📧 Outlook Email Auto-Send Setup Guide

## Quick Setup (5 Minutes)

### Step 1: Open email_config.py
Open the file: `/Users/tomi/Documents/GitHub/Video_-Analyzer/Sora-2-video-personal-brand2/email_config.py`

### Step 2: Add Your Outlook Credentials

Replace the empty strings with your info:

```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp-mail.outlook.com',
    'smtp_port': 587,
    'email': 'YOUR_EMAIL@outlook.com',  # ← Add your Outlook email here
    'password': 'YOUR_APP_PASSWORD',     # ← Add your password here
    'use_tls': True
}
```

---

## 🔐 RECOMMENDED: Use App Password (More Secure)

### For Personal Outlook/Hotmail:

1. **Go to:** https://account.microsoft.com/security
2. **Click:** "Advanced security options"
3. **Scroll to:** "App passwords"
4. **Click:** "Create a new app password"
5. **Copy** the generated password (looks like: `abcd-efgh-ijkl-mnop`)
6. **Paste** that password into `email_config.py`

### For Microsoft 365 / Office 365 Business:

1. **Go to:** https://portal.office.com
2. **Click:** Settings (gear icon) → View all Outlook settings
3. **Go to:** Mail → Sync email
4. **Enable:** "Let apps use SMTP AUTH to send mail"
5. **Use your regular password** in `email_config.py`
6. **SMTP Server:** Change to `smtp.office365.com`

---

## 📝 Example Configuration

### Personal Outlook/Hotmail:
```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp-mail.outlook.com',
    'smtp_port': 587,
    'email': 'john@outlook.com',
    'password': 'abcd-efgh-ijkl-mnop',  # App password
    'use_tls': True
}
```

### Office 365 Business:
```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.office365.com',
    'smtp_port': 587,
    'email': 'john@yourcompany.com',
    'password': 'your_regular_password',
    'use_tls': True
}
```

---

## ✅ Test Your Setup

1. **Restart backend:** Kill and restart `market_intelligence_web_fixed.py`
2. **Open app:** Go to http://localhost:5173
3. **Click:** Affiliate Partners
4. **Pick a partner**
5. **Click:** "🚀 Send Email" button
6. **Success!** Email will be sent from your Outlook

---

## 🚀 Features Now Available

### 1. **Regenerate Email** 🔄
- Click "Regenerate" to cycle through 5 different email templates
- Each partner has 5 unique variations
- Keep clicking until you find one you like

### 2. **Send Email** 📧
- One-click send directly from your Outlook
- Automatically marks partner as contacted
- Button becomes disabled after sending

### 3. **Copy Email** 📋
- Copy to clipboard for manual sending
- Useful for editing before sending

---

## 🎯 Workflow

1. **Browse** 240 partners
2. **Click "Regenerate"** if you don't like the email
3. **Click "Send Email"** when ready
4. **Email sent** from YOUR Outlook inbox
5. **Partner auto-marked** as contacted ✅

---

## ⚠️ Common Issues

### "Email not configured" error:
- Make sure you filled in `email` and `password` in `email_config.py`
- Restart the backend after editing config

### "Authentication failed" error:
- Check your password is correct
- If using regular password, try creating an App Password
- For Office 365, enable SMTP AUTH in settings

### "Connection timeout" error:
- Check your internet connection
- Try changing `smtp-mail.outlook.com` to `smtp.office365.com`
- Check if firewall is blocking port 587

---

## 📊 Email Limits

- **Outlook.com/Hotmail:** 300 emails per day
- **Office 365 Personal:** 500 emails per day  
- **Office 365 Business:** 10,000 emails per day

**You have 240 partners total, so you're well within limits!**

---

## 🔒 Security Notes

- Your email credentials are stored **locally only** in `email_config.py`
- Never committed to Git (added to `.gitignore`)
- Sent emails appear in YOUR "Sent Items" folder
- Recipients can reply directly to YOU
- Use App Passwords instead of real password for better security

---

## Need Help?

If you run into issues, check:
1. Credentials are correct in `email_config.py`
2. Backend is restarted after config changes
3. Internet connection is working
4. Outlook account is active

**Ready to send 240 partnership emails! 🚀**
