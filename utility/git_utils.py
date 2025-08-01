import subprocess


def run_git_command(command, cwd=None):
    """
    Runs a Git command using subprocess.

    Args:
        command (list): A list of strings representing the Git command and its arguments.
        cwd (str, optional): The current working directory to run the command in. Defaults to None.

    Returns:
        tuple: A tuple containing a boolean indicating success, and the stdout/stderr output.
    """
    try:
        result = subprocess.run(
            command, cwd=cwd, capture_output=True, text=True, check=True
        )
        print(result.stdout)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing Git command: {e}")
        print(f"Stderr: {e.stderr}")
        return False, e.stderr
    except FileNotFoundError:
        print(
            f"Error: Git command not found. Is Git installed and in your PATH? Command: {' '.join(command)}"
        )
        return False, f"Git command not found: {' '.join(command)}"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False, f"Unexpected error: {e}"


def git_init(cwd):
    """Initializes a new Git repository."""
    print(f"Initializing Git repository in {cwd}")
    return run_git_command(["git", "init"], cwd=cwd)


def git_add(files, cwd):
    """Adds files to the Git staging area."""
    print(f"Adding files to Git staging area in {cwd}")
    command = ["git", "add"] + files
    return run_git_command(command, cwd=cwd)


def git_commit(message, cwd):
    """Commits changes to the repository."""
    print(f"Committing changes in {cwd}")
    return run_git_command(["git", "commit", "-m", message], cwd=cwd)


def git_add_remote(name, url, cwd):
    """Adds a remote repository."""
    print(f"Adding remote '{name}' with URL '{url}' in {cwd}")
    return run_git_command(["git", "remote", "add", name, url], cwd=cwd)


def git_remove_remote(name, cwd):
    """Removes a remote repository."""
    print(f"Removing remote '{name}' in {cwd}")
    # Use check=False as remote might not exist, which is not an error for this operation
    try:
        result = subprocess.run(
            ["git", "remote", "remove", name],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
        print(result.stdout)
        if result.returncode != 0 and "fatal: No such remote" not in result.stderr:
            print(f"Error removing remote: {result.stderr}")
            return False, result.stderr
        return True, result.stdout
    except Exception as e:
        print(f"An unexpected error occurred while removing remote: {e}")
        return False, f"Unexpected error: {e}"


def git_push(remote, branch, cwd, token=None):
    """Pushes commits to a remote repository."""
    print(f"Pushing to remote '{remote}' branch '{branch}' from {cwd}")
    command = ["git", "push", "--set-upstream", remote, branch]

    if token:
        # Using token in URL - note: less secure than SSH or credential helper
        # Assumes HTTPS URL is already set for the remote
        print("Attempting push using GitHub token...")
        # Need to get the remote URL to insert the token
        success_url, url_output = run_git_command(
            ["git", "remote", "get-url", remote], cwd=cwd
        )
        if success_url:
            remote_url = url_output.strip()
            if remote_url.startswith("https://github.com/"):
                # Insert token into the URL
                auth_url = remote_url.replace(
                    "https://github.com/", f"https://{token}@github.com/"
                )
                # Use the authenticated URL directly in the push command
                command = ["git", "push", auth_url, branch]
                # Remove --set-upstream as it's not needed with direct URL push
                if "--set-upstream" in command:
                    command.remove("--set-upstream")
                print(f"Executing push with authenticated URL: {auth_url}")
            else:
                print(
                    f"Remote URL is not HTTPS GitHub: {remote_url}. Cannot use token in URL."
                )
                # Fallback to standard push command
                command = ["git", "push", "--set-upstream", remote, branch]
        else:
            print("Could not get remote URL to use token.")
            # Fallback to standard push command
            command = ["git", "push", "--set-upstream", remote, branch]

    return run_git_command(command, cwd=cwd)


if __name__ == "__main__":
    # Example usage (won't run in this writefile cell, but for context)
    # repo_dir = "/tmp/my_temp_repo"
    # os.makedirs(repo_dir, exist_ok=True)
    # git_init(repo_dir)
    # with open(os.path.join(repo_dir, "test.txt"), "w") as f:
    #     f.write("test content")
    # git_add(["test.txt"], repo_dir)
    # git_commit("Add test file", repo_dir)
    # git_add_remote("origin", "https://github.com/user/repo.git", repo_dir)
    # git_push("origin", "main", repo_dir, token="YOUR_GITHUB_TOKEN")
    pass
