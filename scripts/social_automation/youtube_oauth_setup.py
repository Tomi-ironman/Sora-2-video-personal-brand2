#!/usr/bin/env python3
"""
YouTube OAuth 2.0 Setup for Automated Commenting
Enables full automation of YouTube comment posting
"""

import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# YouTube API scopes for commenting
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

class YouTubeOAuthSetup:
    def __init__(self):
        self.credentials_dir = "youtube_credentials"
        self.ensure_credentials_dir()
        
    def ensure_credentials_dir(self):
        """Create credentials directory if it doesn't exist"""
        if not os.path.exists(self.credentials_dir):
            os.makedirs(self.credentials_dir)
            
    def create_oauth_credentials_file(self, account_name="youtube1"):
        """Create OAuth credentials file template"""
        credentials_template = {
            "installed": {
                "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
                "project_id": "your-project-id",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": "YOUR_CLIENT_SECRET",
                "redirect_uris": ["http://localhost"]
            }
        }
        
        credentials_file = f"{self.credentials_dir}/{account_name}_credentials.json"
        
        with open(credentials_file, 'w') as f:
            json.dump(credentials_template, f, indent=2)
            
        print(f"📝 Created template: {credentials_file}")
        print("🔧 Please fill in your OAuth credentials from Google Console")
        
        return credentials_file
        
    def setup_oauth_flow(self, account_name="youtube1"):
        """Set up OAuth 2.0 flow for YouTube account"""
        credentials_file = f"{self.credentials_dir}/{account_name}_credentials.json"
        token_file = f"{self.credentials_dir}/{account_name}_token.json"
        
        creds = None
        
        # Load existing token if available
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
            
        # If no valid credentials, run OAuth flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print(f"🔄 Refreshing credentials for {account_name}...")
                creds.refresh(Request())
            else:
                print(f"🔐 Starting OAuth flow for {account_name}...")
                print("📱 This will open a browser window for authorization")
                
                if not os.path.exists(credentials_file):
                    print(f"❌ Credentials file not found: {credentials_file}")
                    print("🔧 Run create_oauth_credentials_file() first")
                    return None
                    
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
                
            # Save credentials for next run
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
                
        print(f"✅ OAuth setup complete for {account_name}")
        return creds
        
    def test_youtube_api(self, account_name="youtube1"):
        """Test YouTube API access with OAuth credentials"""
        creds = self.setup_oauth_flow(account_name)
        
        if not creds:
            return False
            
        try:
            # Build YouTube service
            youtube = build('youtube', 'v3', credentials=creds)
            
            # Test API access
            channels_response = youtube.channels().list(
                part='snippet',
                mine=True
            ).execute()
            
            if channels_response['items']:
                channel = channels_response['items'][0]
                channel_title = channel['snippet']['title']
                print(f"✅ Connected to YouTube channel: {channel_title}")
                return True
            else:
                print("❌ No YouTube channel found for this account")
                return False
                
        except Exception as e:
            print(f"❌ YouTube API test failed: {e}")
            return False
            
    def setup_multiple_accounts(self, account_names=["youtube1", "youtube2", "youtube3"]):
        """Set up OAuth for multiple YouTube accounts"""
        print("🚀 Setting up OAuth for multiple YouTube accounts")
        print("=" * 60)
        
        for account_name in account_names:
            print(f"\n🔧 Setting up {account_name}...")
            
            # Create credentials template
            self.create_oauth_credentials_file(account_name)
            
            print(f"📋 Next steps for {account_name}:")
            print("1. Go to: https://console.developers.google.com/")
            print("2. Create OAuth 2.0 credentials (Desktop application)")
            print("3. Download the JSON file")
            print(f"4. Replace the template in: {self.credentials_dir}/{account_name}_credentials.json")
            print("5. Run the OAuth flow")
            
        print("\n🎯 After setting up credentials, run:")
        print("python youtube_oauth_setup.py --authorize")

def show_oauth_setup_guide():
    """Show detailed OAuth setup guide"""
    print("🔐 YouTube OAuth 2.0 Setup Guide")
    print("=" * 50)
    
    print("\n📋 Step 1: Google Cloud Console Setup")
    print("1. Go to: https://console.developers.google.com/")
    print("2. Select your project (or create new one)")
    print("3. Enable 'YouTube Data API v3'")
    print("4. Go to 'Credentials' → 'Create Credentials' → 'OAuth 2.0 Client ID'")
    print("5. Choose 'Desktop application'")
    print("6. Download the JSON file")
    
    print("\n📋 Step 2: Configure Credentials")
    print("1. Replace the template JSON with your downloaded credentials")
    print("2. Make sure the file is named correctly (e.g., youtube1_credentials.json)")
    
    print("\n📋 Step 3: Authorize Application")
    print("1. Run the OAuth flow")
    print("2. Browser will open for Google authorization")
    print("3. Sign in with your YouTube account")
    print("4. Grant permissions for commenting")
    
    print("\n📋 Step 4: Test Integration")
    print("1. Verify API access works")
    print("2. Test comment posting capability")
    
    print("\n🔒 Security Notes:")
    print("• Keep credentials files secure and private")
    print("• Don't commit OAuth tokens to version control")
    print("• Each YouTube account needs separate OAuth setup")
    print("• Tokens can be refreshed automatically")

def main():
    """Main OAuth setup function"""
    import sys
    
    oauth_setup = YouTubeOAuthSetup()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--authorize":
        # Run authorization for existing credentials
        print("🔐 Running OAuth authorization...")
        
        account_names = ["youtube1", "youtube2", "youtube3"]
        for account_name in account_names:
            credentials_file = f"{oauth_setup.credentials_dir}/{account_name}_credentials.json"
            
            if os.path.exists(credentials_file):
                print(f"\n🔧 Authorizing {account_name}...")
                if oauth_setup.test_youtube_api(account_name):
                    print(f"✅ {account_name} ready for automated commenting!")
                else:
                    print(f"❌ {account_name} authorization failed")
            else:
                print(f"⚠️ Credentials file not found for {account_name}")
                
    else:
        # Show setup guide and create templates
        show_oauth_setup_guide()
        oauth_setup.setup_multiple_accounts()

if __name__ == "__main__":
    main()
