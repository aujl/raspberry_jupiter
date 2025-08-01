
import unittest
from unittest.mock import patch, MagicMock
import sys

# Add /content/ to the Python path within the test file itself
sys.path.append('/content/')

# Assume jupyter_utils.py is in the /content/ directory
# In a real scenario, you would ensure this module is discoverable
try:
    from jupyter_utils import start_remote_jupyter_server, create_ssh_tunnel, verify_jupyter_connection
except ImportError:
    print("Error: Could not import jupyter_utils. Is jupyter_utils.py in /content/?")
    sys.exit(1)


class TestJupyterUtilsFunctions(unittest.TestCase):

    def setUp(self):
        # Add print statements to see which tests are running
        print(f"\nRunning test: {self._testMethodName}")

    @patch('jupyter_utils.print')
    def test_start_remote_jupyter_server_success(self, mock_print):
        remote_host = "remote.example.com"
        remote_port = 8888
        start_remote_jupyter_server(remote_host, remote_port)
        mock_print.assert_called_with(f"Simulating starting Jupyter server on {remote_host} at port {remote_port}")

    @patch('jupyter_utils.print')
    def test_start_remote_jupyter_server_different_port_success(self, mock_print):
        remote_host = "another.host.org"
        remote_port = 9999
        start_remote_jupyter_server(remote_host, remote_port)
        mock_print.assert_called_with(f"Simulating starting Jupyter server on {remote_host} at port {remote_port}")

    @patch('jupyter_utils.start_remote_jupyter_server', side_effect=Exception("Failed to start server"))
    @patch('jupyter_utils.print')
    def test_start_remote_jupyter_server_failure(self, mock_print, mock_start):
        remote_host = "remote.example.com"
        remote_port = 8888
        with self.assertRaises(Exception) as context:
            start_remote_jupyter_server(remote_host, remote_port)
        self.assertTrue("Failed to start server" in str(context.exception))
        mock_start.assert_called_once_with(remote_host, remote_port)
        # The original function's print is not called when the mock raises an exception
        mock_print.assert_not_called()


    @patch('jupyter_utils.print')
    def test_create_ssh_tunnel_success(self, mock_print):
        local_port = 8000
        remote_port = 8888
        username = "testuser"
        remote_host = "remote.example.com"
        create_ssh_tunnel(local_port, remote_port, username, remote_host)
        mock_print.assert_called_with(f"Simulating creating SSH tunnel from local port {local_port} to {remote_host}:{remote_port} with user {username}")

    @patch('jupyter_utils.print')
    def test_create_ssh_tunnel_different_ports_and_user_success(self, mock_print):
        local_port = 8080
        remote_port = 8889
        username = "anotheruser"
        remote_host = "another.host.org"
        create_ssh_tunnel(local_port, remote_port, username, remote_host)
        mock_print.assert_called_with(f"Simulating creating SSH tunnel from local port {local_port} to {remote_host}:{remote_port} with user {username}")

    @patch('jupyter_utils.create_ssh_tunnel', side_effect=OSError("SSH command failed"))
    @patch('jupyter_utils.print')
    def test_create_ssh_tunnel_failure(self, mock_print, mock_tunnel):
        local_port = 8000
        remote_port = 8888
        username = "testuser"
        remote_host = "remote.example.com"
        with self.assertRaises(OSError) as context:
             create_ssh_tunnel(local_port, remote_port, username, remote_host)
        self.assertTrue("SSH command failed" in str(context.exception))
        mock_tunnel.assert_called_once_with(local_port, remote_port, username, remote_host)
        mock_print.assert_not_called() # print should not be called if an exception is raised before it


    @patch('jupyter_utils.verify_jupyter_connection', return_value=True)
    @patch('jupyter_utils.print')
    def test_verify_jupyter_connection_success(self, mock_print, mock_verify):
        local_port = 8000
        is_connected = verify_jupyter_connection(local_port)
        mock_print.assert_called_with(f"Simulating verifying connection to Jupyter server at http://localhost:{local_port}")
        self.assertTrue(is_connected)
        mock_verify.assert_called_once_with(local_port)


    @patch('jupyter_utils.verify_jupyter_connection', return_value=False)
    @patch('jupyter_utils.print')
    def test_verify_jupyter_connection_failure(self, mock_print, mock_verify):
        local_port = 8000
        is_connected = verify_jupyter_connection(local_port)
        mock_print.assert_called_with(f"Simulating verifying connection to Jupyter server at http://localhost:{local_port}")
        self.assertFalse(is_connected)
        mock_verify.assert_called_once_with(local_port)

    @patch('jupyter_utils.verify_jupyter_connection', side_effect=[True, False, True])
    @patch('jupyter_utils.print')
    def test_verify_jupyter_connection_multiple_attempts(self, mock_print, mock_verify):
        local_port = 8000

        # First attempt: success
        is_connected_1 = verify_jupyter_connection(local_port)
        self.assertTrue(is_connected_1)
        mock_print.assert_any_call(f"Simulating verifying connection to Jupyter server at http://localhost:{local_port}")


        # Second attempt: failure
        is_connected_2 = verify_jupyter_connection(local_port)
        self.assertFalse(is_connected_2)
        mock_print.assert_any_call(f"Simulating verifying connection to Jupyter server at http://localhost:{local_port}")


        # Third attempt: success
        is_connected_3 = verify_jupyter_connection(local_port)
        self.assertTrue(is_connected_3)
        mock_print.assert_any_call(f"Simulating verifying connection to Jupyter server at http://localhost:{local_port}")


        self.assertEqual(mock_verify.call_count, 3)
        mock_verify.assert_any_call(local_port)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
