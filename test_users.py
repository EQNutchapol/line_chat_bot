import requests
import time
import uuid
from build.config import NG_GROK_DOMAIN

# The endpoint that LINE sends messages to.
CALLBACK_URL = f"https://{NG_GROK_DOMAIN}"
ADD_USER_URL = f"{CALLBACK_URL}/api/test/add_user"

# A list of 30 sample names for the test users.
TEST_NAMES = [
    "Alex", "Ben", "Catherine", "David", "Eva", "Frank", "Grace", "Henry", "Isabella", "Jack",
    "Kate", "Liam", "Mia", "Noah", "Olivia", "Peter", "Quinn", "Rachel", "Sam", "Tina",
    "Uma", "Victor", "Wendy", "Xander", "Yara", "Zane", "Chloe", "Daniel", "Emily", "Finn"
]

def simulate_user_join(user_name):
    """
    Simulates a single user sending their name to the test endpoint.
    """
    user_id = f"U{uuid.uuid4().hex}"

    # --- UPDATED: Simplified payload for the new endpoint ---
    payload = {
        "user_id": user_id,
        "name": user_name
    }

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        # Send the request to the new test URL
        response = requests.post(ADD_USER_URL, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"Successfully added user: {user_name}")
        else:
            print(f"Failed to add user: {user_name} | Status Code: {response.status_code} | Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the server: {e}")

if __name__ == "__main__":
    print(f"Starting test: Adding 30 users to the lobby via {ADD_USER_URL}...")
    for name in TEST_NAMES:
        simulate_user_join(name) # Keep the delay for stability
    print("Test finished.")
