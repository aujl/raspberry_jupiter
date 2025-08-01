import subprocess


def run_shell_command(command, cwd=None):
    """
    Runs a shell command using subprocess.

    Args:
        command (list or str): The command to run. If a string, it will be run through the shell.
                                If a list, the first item is the command, and subsequent items are arguments.
        cwd (str, optional): The current working directory to run the command in. Defaults to None.

    Returns:
        tuple: A tuple containing a boolean indicating success, and the stdout/stderr output.
    """
    shell = isinstance(command, str)  # Run through shell if command is a string
    try:
        result = subprocess.run(
            command, cwd=cwd, capture_output=True, text=True, check=True, shell=shell
        )
        print(result.stdout)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Stderr: {e.stderr}")
        return False, e.stderr
    except FileNotFoundError:
        print(
            f"Error: Command not found: {command[0] if isinstance(command, list) else command}"
        )
        return (
            False,
            f"Command not found: {command[0] if isinstance(command, list) else command}",
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False, f"Unexpected error: {e}"


if __name__ == "__main__":
    # Example usage (won't run in this writefile cell, but for context)
    # success, output = run_shell_command(["ls", "-l"])
    # print(output)
    # success, output = run_shell_command("echo 'hello world'")
    # print(output)
    pass
