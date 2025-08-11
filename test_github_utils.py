import sys
import types
import unittest
from unittest.mock import patch, ANY

# Create a fake google.colab.userdata module for testing
fake_userdata = types.SimpleNamespace(
    get=lambda key: {
        "GitHubtoken": "fake_token",
        "GitHubusername": "fake_user",
    }.get(key)
)

colab_module = types.ModuleType("colab")
colab_module.userdata = fake_userdata

google_module = types.ModuleType("google")
google_module.colab = colab_module

sys.modules.setdefault("google", google_module)
sys.modules.setdefault("google.colab", colab_module)
sys.modules.setdefault("google.colab.userdata", fake_userdata)

from utility.github_utils import create_github_repository


class TestGithubUtils(unittest.TestCase):
    @patch("utility.github_utils.requests.get")
    @patch("utility.github_utils.requests.post")
    def test_existing_repo_uses_username(self, mock_post, mock_get):
        # Simulate repository already existing
        mock_post.return_value.status_code = 422

        # Simulate retrieving existing repository URL
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "html_url": "https://github.com/dummyuser/myrepo"
        }

        success, url = create_github_repository(
            "myrepo", "desc", username="dummyuser"
        )

        self.assertTrue(success)
        self.assertEqual(url, "https://github.com/dummyuser/myrepo")
        mock_get.assert_called_once_with(
            "https://api.github.com/repos/dummyuser/myrepo", headers=ANY
        )


if __name__ == "__main__":
    unittest.main()
