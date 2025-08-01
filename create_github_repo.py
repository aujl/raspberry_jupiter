import requests
import sys
from google.colab import userdata

try:
    github_token = userdata.get("GitHubtoken")
    if github_token is None:
        print("Error: GitHub token not found in Colab secrets.")
        sys.exit(1)
except Exception as e:
    print(f"Error retrieving GitHub token: {e}")
    sys.exit(1)

# Define the GitHub API endpoint for creating repositories for the
# authenticated user
api_url = "https://api.github.com/user/repos"

# Define the request headers
headers = {
    "Authorization": f"token {github_token}",
    "Accept": "application/vnd.github.v3+json",
}

# Define the request payload
repo_name = "raspberry_jupiter"
payload = {
    "name": repo_name,
    "description": "Repository for the Raspberry Pi Jupyter project",
    "private": False,  # Set to True if you want a private repository
}

# Make the POST request to create the repository
response = requests.post(api_url, headers=headers, json=payload)

# Check the response status code and print a message
if response.status_code == 201:
    print(f"Repository '{repo_name}' created successfully!")
elif response.status_code == 422:
    print(f"Repository '{repo_name}' already exists.")
    # It's okay if the repository already exists, we can proceed.
    sys.exit(0)
else:
    print(f"Error creating repository: {response.status_code} - {response.text}")
    sys.exit(1)
