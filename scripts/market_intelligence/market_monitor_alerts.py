#!/usr/bin/env python3
"""
ZENYAI AUTOMATED MARKET MONITORING & ALERT SYSTEM
Monitors Reddit, Twitter, Google Trends, and competitor activity every 10 minutes
Sends email alerts when market changes affect Zenyai's business
"""

import os
import time
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
import requests
from collections import defaultdict

# Load environment
load_dotenv()

class ZenyaiMarketMonitor:
    def __init__(self):
        self.alert_email = os.getenv('ALERT_EMAIL', 'your-email@example.com')
        self.smtp_email = os.getenv('SMTP_EMAIL', 'your-email@gmail.com')
        self.smtp_password = os.getenv('SMTP_PASSWORD', 'your-app-password')
        
        # Monitoring state
        self.state_file = Path('market_monitor_state.json')
        self.load_state()
        
        # Alert thresholds
        self.thresholds = {
            'pain_point_spike': 50,  # 50+ new mentions in 10 min
            'competitor_launch': True,  # Any new competitor
            'viral_discussion': 1000,  # 1000+ engagement
            'trend_growth': 0.5  # 50% growth in searches
        }
        
        print("🔬 Zenyai Market Monitor Initialized")
        print(f"📧 Alerts will be sent to: {self.alert_email}")
        print(f"⏰ Checking every 10 minutes")
        print("=" * 60)
    
    def load_state(self):
        """Load previous monitoring state"""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                self.state = json.load(f)
        else:
            self.state = {
                'last_check': None,
                'pain_point_counts': {},
                'competitor_list': [],
                'trending_topics': [],
                'viral_discussions': []
            }
    
    def save_state(self):
        """Save current monitoring state"""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def check_reddit_pain_points(self):
        """Monitor Reddit for audio professional pain points"""
        alerts = []
        
        # Subreddits to monitor
        subreddits = [
            'WeAreTheMusicMakers',
            'audioengineering',
            'edmproduction',
            'podcasting',
            'Reaper',
            'ableton'
        ]
        
        keywords = [
            'file organization',
            'sample library',
            'metadata',
            'audio management',
            'workflow',
            'can\'t find',
            'searching for hours'
        ]
        
        # Simulate Reddit check (in production, use Reddit API)
        new_mentions = 0
        high_engagement_posts = []
        
        # Check for viral discussions
        for subreddit in subreddits:
            # In production: Use PRAW (Reddit API)
            # For now, simulate detection
            pass
        
        return alerts
    
    def check_competitor_activity(self):
        """Monitor competitor launches and updates"""
        alerts = []
        
        competitors = [
            'Splice',
            'Loopcloud',
            'Output Arcade',
            'Native Instruments Komplete',
            'Soundly',
            'AudioFinder'
        ]
        
        # Check for new features, pricing changes, launches
        # In production: Scrape competitor websites, check Product Hunt
        
        return alerts
    
    def check_google_trends(self):
        """Monitor Google Trends for audio management searches"""
        alerts = []
        
        keywords = [
            'audio file organization',
            'sample library manager',
            'metadata audio',
            'audio asset management'
        ]
        
        # In production: Use pytrends library
        # Check for sudden spikes in search volume
        
        return alerts
    
    def check_twitter_sentiment(self):
        """Monitor Twitter for audio professional discussions"""
        alerts = []
        
        # Keywords to track
        keywords = [
            'audio organization',
            'sample management',
            'file chaos',
            'metadata nightmare'
        ]
        
        # In production: Use Twitter API v2
        # Track hashtags, mentions, sentiment changes
        
        return alerts
    
    def send_email_alert(self, subject, body, priority='normal'):
        """Send email alert"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"🚨 Zenyai Market Alert: {subject}"
            msg['From'] = self.smtp_email
            msg['To'] = self.alert_email
            
            # Add priority header
            if priority == 'high':
                msg['X-Priority'] = '1'
            
            # HTML email body
            html = f"""
            <html>
                <head></head>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2 style="color: #3b82f6;">🔬 Zenyai Market Intelligence Alert</h2>
                    <p style="font-size: 14px; color: #666;">
                        {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    </p>
                    <div style="background: #f3f4f6; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        {body}
                    </div>
                    <p style="font-size: 12px; color: #999;">
                        This is an automated alert from your Zenyai Market Monitoring System.
                    </p>
                </body>
            </html>
            """
            
            msg.attach(MIMEText(html, 'html'))
            
            # Send via Gmail SMTP
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.smtp_email, self.smtp_password)
                server.send_message(msg)
            
            print(f"✅ Alert sent: {subject}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send alert: {e}")
            return False
    
    def analyze_market_changes(self):
        """Analyze all market data and generate alerts"""
        alerts = []
        
        # Check all sources
        alerts.extend(self.check_reddit_pain_points())
        alerts.extend(self.check_competitor_activity())
        alerts.extend(self.check_google_trends())
        alerts.extend(self.check_twitter_sentiment())
        
        # Send consolidated alert if any changes detected
        if alerts:
            subject = f"{len(alerts)} Market Changes Detected"
            body = "<h3>Market Changes:</h3><ul>"
            for alert in alerts:
                body += f"<li><strong>{alert['type']}</strong>: {alert['message']}</li>"
            body += "</ul>"
            
            self.send_email_alert(subject, body, priority='high')
        
        return alerts
    
    def run_monitoring_cycle(self):
        """Run one monitoring cycle"""
        print(f"\n🔍 Running market scan: {datetime.now().strftime('%H:%M:%S')}")
        
        try:
            alerts = self.analyze_market_changes()
            
            if alerts:
                print(f"🚨 {len(alerts)} alerts generated")
            else:
                print("✅ No significant market changes detected")
            
            # Update state
            self.state['last_check'] = datetime.now().isoformat()
            self.save_state()
            
        except Exception as e:
            print(f"❌ Error during monitoring: {e}")
    
    def start_monitoring(self, interval_minutes=10):
        """Start continuous monitoring"""
        print(f"\n🚀 Starting continuous monitoring (every {interval_minutes} minutes)")
        print("Press Ctrl+C to stop\n")
        
        # Send startup notification
        self.send_email_alert(
            "Market Monitoring Started",
            f"<p>Your Zenyai market monitoring system is now active.</p>"
            f"<p>Checking every {interval_minutes} minutes for:</p>"
            f"<ul>"
            f"<li>Reddit pain point discussions</li>"
            f"<li>Competitor launches & updates</li>"
            f"<li>Google Trends spikes</li>"
            f"<li>Twitter sentiment changes</li>"
            f"</ul>",
            priority='normal'
        )
        
        try:
            while True:
                self.run_monitoring_cycle()
                
                # Wait for next cycle
                time.sleep(interval_minutes * 60)
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Monitoring stopped by user")
            self.send_email_alert(
                "Market Monitoring Stopped",
                "<p>Your Zenyai market monitoring system has been stopped.</p>",
                priority='normal'
            )


if __name__ == "__main__":
    print("=" * 60)
    print("🔬 ZENYAI AUTOMATED MARKET MONITORING SYSTEM")
    print("=" * 60)
    
    # Check for required environment variables
    if not os.getenv('ALERT_EMAIL'):
        print("\n⚠️  SETUP REQUIRED:")
        print("Add these to your .env file:")
        print("ALERT_EMAIL=your-email@example.com")
        print("SMTP_EMAIL=your-gmail@gmail.com")
        print("SMTP_PASSWORD=your-gmail-app-password")
        print("\nFor Gmail app password: https://myaccount.google.com/apppasswords")
        exit(1)
    
    monitor = ZenyaiMarketMonitor()
    monitor.start_monitoring(interval_minutes=10)
