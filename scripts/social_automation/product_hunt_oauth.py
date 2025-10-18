#!/usr/bin/env python3
"""
Product Hunt OAuth 2.0 Setup
Get access token for Product Hunt API automation
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class ProductHuntOAuth:
    def __init__(self):
        self.client_id = os.getenv('PRODUCTHUNT_API_KEY')
        self.client_secret = os.getenv('PRODUCTHUNT_API_SECRET')
        self.redirect_uri = 'https://www.mit.edu/'
        
    def get_access_token(self):
        """Get access token using client credentials flow"""
        print("🔐 Getting Product Hunt access token...")
        
        # Product Hunt uses OAuth 2.0 Client Credentials flow
        token_url = "https://api.producthunt.com/v2/oauth/token"
        
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        try:
            response = requests.post(token_url, json=data, headers=headers)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data.get('access_token')
                
                if access_token:
                    print(f"✅ Access token obtained: {access_token[:20]}...")
                    
                    # Save to .env file
                    self.save_access_token(access_token)
                    return access_token
                else:
                    print("❌ No access token in response")
                    
            else:
                print(f"❌ Failed to get access token: {response.status_code}")
                print(f"Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Error getting access token: {e}")
            
        return None
        
    def save_access_token(self, access_token):
        """Save access token to .env file"""
        try:
            # Read current .env file
            env_file = '.env'
            lines = []
            
            if os.path.exists(env_file):
                with open(env_file, 'r') as f:
                    lines = f.readlines()
            
            # Add or update access token
            token_line = f'PRODUCTHUNT_ACCESS_TOKEN={access_token}\n'
            
            # Check if token already exists
            updated = False
            for i, line in enumerate(lines):
                if line.startswith('PRODUCTHUNT_ACCESS_TOKEN='):
                    lines[i] = token_line
                    updated = True
                    break
                    
            if not updated:
                lines.append(token_line)
                
            # Write back to file
            with open(env_file, 'w') as f:
                f.writelines(lines)
                
            print(f"✅ Access token saved to {env_file}")
            
        except Exception as e:
            print(f"❌ Error saving access token: {e}")
            
    def test_api_access(self, access_token):
        """Test API access with the token"""
        print("🔍 Testing Product Hunt API access...")
        
        url = "https://api.producthunt.com/v2/api/graphql"
        
        # Simple query to test access
        query = """
        query {
            posts(first: 1) {
                edges {
                    node {
                        id
                        name
                        tagline
                    }
                }
            }
        }
        """
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        try:
            response = requests.post(
                url,
                json={'query': query},
                headers=headers
            )
            
            print(f"Test Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                if 'data' in data and 'posts' in data['data']:
                    posts = data['data']['posts']['edges']
                    if posts:
                        product = posts[0]['node']
                        print(f"✅ API access working! Found product: {product['name']}")
                        return True
                    else:
                        print("⚠️ API access working but no products found")
                        return True
                else:
                    print(f"❌ Unexpected API response: {data}")
                    
            else:
                print(f"❌ API test failed: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error testing API: {e}")
            
        return False

def main():
    """Main OAuth setup function"""
    print("🏆 Product Hunt OAuth 2.0 Setup")
    print("=" * 40)
    
    oauth = ProductHuntOAuth()
    
    if not oauth.client_id or not oauth.client_secret:
        print("❌ Missing Product Hunt API credentials in .env file")
        print("Make sure you have:")
        print("PRODUCTHUNT_API_KEY=your_api_key")
        print("PRODUCTHUNT_API_SECRET=your_api_secret")
        return
        
    # Get access token
    access_token = oauth.get_access_token()
    
    if access_token:
        # Test API access
        if oauth.test_api_access(access_token):
            print("\n🎉 Product Hunt API setup complete!")
            print("You can now run: python3 product_hunt_automation.py")
        else:
            print("\n❌ API access test failed")
    else:
        print("\n❌ Failed to get access token")
        print("\n🔧 Troubleshooting:")
        print("1. Check your API key and secret are correct")
        print("2. Make sure your Product Hunt app is properly configured")
        print("3. Verify the redirect URI matches your app settings")

if __name__ == "__main__":
    main()
