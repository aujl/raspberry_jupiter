import os


def change_directory(path):
    """
    Changes the current working directory.

    Args:
        path (str): The path to change to.

    Returns:
        tuple: True if the directory change was successful, False otherwise.
        str: The new working directory or an error message.
    """
    try:
        os.chdir(path)
        print(f"Changed directory to: {os.getcwd()}")
        return True, os.getcwd()
    except FileNotFoundError:
        print(f"Error: Directory not found: {path}")
        return False, f"Directory not found: {path}"
    except Exception as e:
        print(f"An error occurred while changing directory: {e}")
        return False, f"Error changing directory: {e}"


if __name__ == "__main__":
    # Example usage (won't run in this writefile cell, but for context)
    # success, message = change_directory("/gdrive/MyDrive/my_jupyter_repo")
    # print(message)
    pass
