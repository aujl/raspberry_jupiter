import requests


def start_remote_jupyter_server(remote_host, remote_port):
    """Simulates starting a Jupyter server on the remote machine."""
    print(f"Simulating starting Jupyter server on {remote_host} at port {remote_port}")
    # In a real scenario, you would execute the shell command here
    # For simulation purposes, we simply log the action.


def create_ssh_tunnel(local_port, remote_port, username, remote_host):
    """Simulates creating an SSH tunnel to the remote Jupyter server."""
    print(
        "Simulating creating SSH tunnel from local port "
        f"{local_port} to {remote_host}:{remote_port} with user {username}"
    )
    # In a real scenario, you would execute the shell command here
    # For simulation purposes, we simply log the action.


def verify_jupyter_connection(local_port, timeout=5):
    """Verifies the connection to the Jupyter server through the local port.

    The previous implementation always returned ``True`` regardless of whether
    the server was reachable, which made it impossible to detect connection
    issues. This function now attempts to make an HTTP request to the Jupyter
    server and returns ``True`` only when the request succeeds.

    Args:
        local_port: The local port number of the SSH tunnel.
        timeout: Number of seconds to wait for a response.

    Returns:
        bool: ``True`` if the server responds with HTTP 200, ``False``
        otherwise.
    """
    url = f"http://localhost:{local_port}"
    print(f"Simulating verifying connection to Jupyter server at {url}")
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except requests.RequestException:
        return False
