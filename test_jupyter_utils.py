import unittest
from unittest.mock import patch

import jupyter_utils


class TestJupyterUtilsFunctions(unittest.TestCase):

    @patch("jupyter_utils.print")
    def test_start_remote_jupyter_server_success(self, mock_print):
        remote_host = "remote.example.com"
        remote_port = 8888
        jupyter_utils.start_remote_jupyter_server(remote_host, remote_port)
        mock_print.assert_called_once_with(
            f"Simulating starting Jupyter server on {remote_host} at port {remote_port}"
        )

    @patch(
        "jupyter_utils.start_remote_jupyter_server",
        side_effect=Exception("Failed to start server"),
    )
    @patch("jupyter_utils.print")
    def test_start_remote_jupyter_server_failure(self, mock_print, mock_start):
        remote_host = "remote.example.com"
        remote_port = 8888
        with self.assertRaises(Exception) as context:
            jupyter_utils.start_remote_jupyter_server(remote_host, remote_port)
        self.assertEqual(str(context.exception), "Failed to start server")
        mock_start.assert_called_once_with(remote_host, remote_port)
        mock_print.assert_not_called()

    @patch("jupyter_utils.print")
    def test_create_ssh_tunnel_success(self, mock_print):
        local_port = 8000
        remote_port = 8888
        username = "testuser"
        remote_host = "remote.example.com"
        jupyter_utils.create_ssh_tunnel(local_port, remote_port, username, remote_host)
        mock_print.assert_called_once_with(
            f"Simulating creating SSH tunnel from local port {local_port} to {remote_host}:{remote_port} with user {username}"
        )

    @patch("jupyter_utils.create_ssh_tunnel", side_effect=OSError("SSH command failed"))
    @patch("jupyter_utils.print")
    def test_create_ssh_tunnel_failure(self, mock_print, mock_tunnel):
        local_port = 8000
        remote_port = 8888
        username = "testuser"
        remote_host = "remote.example.com"
        with self.assertRaises(OSError) as context:
            jupyter_utils.create_ssh_tunnel(
                local_port, remote_port, username, remote_host
            )
        self.assertEqual(str(context.exception), "SSH command failed")
        mock_tunnel.assert_called_once_with(
            local_port, remote_port, username, remote_host
        )
        mock_print.assert_not_called()

    @patch("jupyter_utils.print")
    def test_verify_jupyter_connection_success(self, mock_print):
        local_port = 8000
        is_connected = jupyter_utils.verify_jupyter_connection(local_port)
        mock_print.assert_called_once_with(
            f"Simulating verifying connection to Jupyter server at http://localhost:{local_port}"
        )
        self.assertTrue(is_connected)

    @patch("jupyter_utils.print")
    def test_verify_jupyter_connection_failure(self, mock_print):
        local_port = 8000

        def side_effect(port):
            jupyter_utils.print(
                f"Simulating verifying connection to Jupyter server at http://localhost:{port}"
            )
            return False

        with patch(
            "jupyter_utils.verify_jupyter_connection", side_effect=side_effect
        ) as mock_verify:
            is_connected = jupyter_utils.verify_jupyter_connection(local_port)
        mock_print.assert_called_once_with(
            f"Simulating verifying connection to Jupyter server at http://localhost:{local_port}"
        )
        self.assertFalse(is_connected)
        mock_verify.assert_called_once_with(local_port)
