import jwt
import time
import requests

# Salesforce credentials
CLIENT_ID = "3MVG9GCMQoQ6rpzRwpe3RcijrqAIK0YrMJOl1.C80b39IKzVKbSQCijo_x3sPyPCFMSMBk3Ml_UEYIDs7KsAr"  # Replace with your Connected App's Consumer Key
USERNAME = "ujjwal2@sandbox.com"  # Replace with your Salesforce username
LOGIN_URL = "https://login.salesforce.com"  # Use test.salesforce.com for sandbox
PRIVATE_KEY_PATH = "/app/server.key"  # Path to your private key

# Load the private key
with open(PRIVATE_KEY_PATH, "rb") as key_file:
    private_key = key_file.read()

# Create JWT token
current_time = int(time.time())
jwt_payload = {
    "iss": CLIENT_ID,
    "sub": USERNAME,
    "aud": LOGIN_URL,
    "exp": current_time + 300,  # Token expiration time (5 mins)
}

jwt_token = jwt.encode(jwt_payload, private_key, algorithm="RS256")

# Request access token
token_url = f"{LOGIN_URL}/services/oauth2/token"
data = {
    "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
    "assertion": jwt_token,
}
response = requests.post(token_url, data=data)

if response.status_code == 200:
    access_token = response.json().get("access_token")
    instance_url = response.json().get("instance_url")
    print(f"✅ Authentication successful! Access Token: {access_token}")
    print(f"🌍 Instance URL: {instance_url}")

    # 🔥 Fetch accounts from Salesforce
    query = "SELECT Id, Name FROM Account LIMIT 5"
    query_url = f"{instance_url}/services/data/v59.0/query/?q={query}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    query_response = requests.get(query_url, headers=headers)

    if query_response.status_code == 200:
        records = query_response.json().get("records", [])
        print("\n📜 Retrieved Accounts:")
        for record in records:
            print(f"🆔 ID: {record['Id']} | 📛 Name: {record['Name']}")
    else:
        print(f"❌ Failed to fetch accounts: {query_response.text}")

else:
    print(f"❌ Authentication failed: {response.text}")
