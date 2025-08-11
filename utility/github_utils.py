import requests
from google.colab import userdata


def create_github_repository(repo_name, description, private=False, username=None):
    """
    Creates a new GitHub repository using the GitHub API.

    Args:
        repo_name (str): The name of the repository to create.
        description (str): A brief description of the repository.
        private (bool): Whether the repository should be private (default: False).
        username (str, optional): GitHub username. If not provided, it will be
            retrieved from Colab secrets.

    Returns:
        tuple: A tuple containing a boolean indicating success, and the URL of the created repository or an error message.
    """
    try:
        github_token = userdata.get("GitHubtoken")
        if github_token is None:
            print("Error: GitHub token not found in Colab secrets.")
            return False, "GitHub token not found"
        if username is None:
            username = userdata.get("GitHubusername")
            if username is None:
                print("Error: GitHub username not found in Colab secrets.")
                return False, "GitHub username not found"
    except Exception as e:
        print(f"Error retrieving GitHub token: {e}")
        return False, f"Error retrieving GitHub token: {e}"

    api_url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    payload = {"name": repo_name, "description": description, "private": private}

    try:
        response = requests.post(api_url, headers=headers, json=payload)

        if response.status_code == 201:
            print(f"Repository '{repo_name}' created successfully!")
            return True, response.json().get("html_url")
        elif response.status_code == 422:
            print(f"Repository '{repo_name}' already exists.")
            # Attempt to get the URL of the existing repository
            try:
                # Use the API to get the repo details and extract the URL
                check_response = requests.get(
                    f"https://api.github.com/repos/{username}/{repo_name}",
                    headers=headers,
                )
                if check_response.status_code == 200:
                    return True, check_response.json().get("html_url")
                else:
                    return (
                        True,
                        f"Repository '{repo_name}' already exists, but could not retrieve URL.",
                    )
            except Exception as e:
                return (
                    True,
                    f"Repository '{repo_name}' already exists, but an error occurred retrieving URL: {e}",
                )
        else:
            print(
                f"Error creating repository: {response.status_code} - {response.text}"
            )
            return (
                False,
                f"Error creating repository: {response.status_code} - {response.text}",
            )

    except Exception as e:
        print(f"An error occurred during the API request: {e}")
        return False, f"API request failed: {e}"


if __name__ == "__main__":
    pass
