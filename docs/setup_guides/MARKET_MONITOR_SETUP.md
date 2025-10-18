# 🔬 ZENYAI MARKET MONITORING SYSTEM - SETUP GUIDE

## 📧 EMAIL ALERTS (FREE - RECOMMENDED)

### Step 1: Setup Gmail App Password
1. Go to: https://myaccount.google.com/apppasswords
2. Sign in to your Google account
3. Create a new app password for "Mail"
4. Copy the 16-character password

### Step 2: Add to .env file
```bash
# Add these lines to your .env file
ALERT_EMAIL=your-email@example.com          # Where you want to receive alerts
SMTP_EMAIL=your-gmail@gmail.com             # Your Gmail address
SMTP_PASSWORD=xxxx xxxx xxxx xxxx           # The 16-char app password from Step 1
```

### Step 3: Start Monitoring
```bash
python3 market_monitor_alerts.py
```

**That's it!** The system will now:
- ✅ Check Reddit, Twitter, Google Trends every 10 minutes
- ✅ Send email alerts when market changes affect Zenyai
- ✅ Track competitor launches, viral discussions, pain point spikes
- ✅ Run 24/7 in the background

---

## 📱 SMS ALERTS (OPTIONAL - ~$1/month)

If you want SMS text messages instead of/in addition to email:

### Option 1: Twilio (Most Popular)
1. Sign up: https://www.twilio.com/try-twilio
2. Get $15 free credit (enough for ~500 SMS)
3. Get your Account SID, Auth Token, and Phone Number
4. Add to .env:
```bash
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
ALERT_PHONE_NUMBER=+1234567890  # Your phone
```

### Option 2: AWS SNS (Cheapest)
- $0.00645 per SMS (about $1 for 150 messages)
- Setup: https://aws.amazon.com/sns/

### Option 3: Vonage/Nexmo
- Similar to Twilio
- Good international coverage

**I can add SMS support once you choose a provider!**

---

## 🎯 WHAT GETS MONITORED

### Reddit Pain Points
- Subreddits: WeAreTheMusicMakers, audioengineering, edmproduction, podcasting
- Keywords: "file organization", "sample library", "metadata", "can't find"
- **Alert Trigger**: 50+ new mentions in 10 minutes OR viral post (1000+ upvotes)

### Competitor Activity
- Monitors: Splice, Loopcloud, Output Arcade, Native Instruments, Soundly
- **Alert Trigger**: New product launch, major feature update, pricing change

### Google Trends
- Keywords: "audio file organization", "sample library manager", "metadata audio"
- **Alert Trigger**: 50%+ spike in search volume

### Twitter Sentiment
- Tracks: Audio professional discussions, pain points, tool mentions
- **Alert Trigger**: Trending hashtag or viral tweet (1000+ engagement)

---

## 📊 ALERT EXAMPLES

You'll receive emails like:

**Subject**: 🚨 Zenyai Market Alert: 3 Market Changes Detected

**Body**:
- **Reddit Spike**: "file organization chaos" mentioned 87 times in last 10 min (r/WeAreTheMusicMakers)
- **Viral Discussion**: "I have 50GB of samples and can't find anything" - 2,340 upvotes
- **Competitor Launch**: Splice announced new AI organization feature

---

## 🛠️ CUSTOMIZATION

Edit `market_monitor_alerts.py` to adjust:
- **Monitoring interval**: Change `interval_minutes=10` to any value
- **Alert thresholds**: Modify `self.thresholds` dictionary
- **Keywords**: Add/remove keywords to track
- **Platforms**: Add YouTube, Product Hunt, Hacker News, etc.

---

## 🚀 RUNNING 24/7

### Option 1: Keep Terminal Open
```bash
python3 market_monitor_alerts.py
```

### Option 2: Background Process (Mac/Linux)
```bash
nohup python3 market_monitor_alerts.py > monitor.log 2>&1 &
```

### Option 3: System Service (Always Running)
```bash
# Create a launchd service (Mac) or systemd service (Linux)
# I can help set this up if needed
```

---

## 📞 NEED HELP?

Just ask me to:
- Add SMS support (once you have Twilio/AWS setup)
- Customize alert triggers
- Add more monitoring sources
- Set up as system service
- Integrate with Slack/Discord instead of email

---

## 🎯 READY TO START?

1. Add email credentials to `.env`
2. Run: `python3 market_monitor_alerts.py`
3. Check your email for startup notification
4. System will alert you automatically when market changes happen!
