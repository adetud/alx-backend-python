#!/usr/bin/env python3
"""Unit and integration tests for client.py."""

import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient
from fixtures import (
    org_payload,
    repos_payload,
    expected_repos,
    apache2_repos
)


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that org returns the expected value and calls get_json."""
        client = GithubOrgClient(org_name)
        client.org()  # call method
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """Test _public_repos_url property returns expected URL."""
        client = GithubOrgClient("test_org")
        payload = {"repos_url": "http://api.example.com/repos"}

        # Patch org as a method
        with patch.object(GithubOrgClient, "org", return_value=payload) as mock_org:
            result = client._public_repos_url
            self.assertEqual(result, "http://api.example.com/repos")
            mock_org.assert_called_once()

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos property returns list of repo names."""
        client = GithubOrgClient("test_org")
        mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]

        # Patch _public_repos_url as a property using PropertyMock
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://api.example.com/repos"
            result = client.public_repos  # access memoized property
            self.assertEqual(result, ["repo1", "repo2"])
            mock_get_json.assert_called_once()
            mock_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean."""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [
        (org_payload, repos_payload, expected_repos, apache2_repos)
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos using fixtures."""


    @classmethod
    def setUpClass(cls):
        """Mock requests.get with side_effect for different URLs."""
        cls.get_patcher = patch("client.requests.get")
        mock_get = cls.get_patcher.start()

        # Side effect to return org payload or repos payload
        def json_side_effect(*args, **kwargs):
            url = args[0]
            if url == "https://api.github.com/orgs/google":
                return cls.org_payload
            return cls.repos_payload

        mock_get.return_value.json.side_effect = json_side_effect
    
def test_public_repos(self):
    """Test public_repos returns expected list of repo names from fixtures."""
    client = GithubOrgClient("google")
    result = client.public_repos
    self.assertEqual(result, self.expected_repos)

def test_public_repos_with_license(self):
    """Test public_repos filtered by license returns expected list from fixtures."""
    client = GithubOrgClient("google")
    result = [
        repo for repo in client.public_repos
        if GithubOrgClient.has_license(
            {"license": {"key": "apache-2.0"}}, "apache-2.0"
        )
    ]
    self.assertEqual(result, self.apache2_repos)

    @classmethod
    def tearDownClass(cls):
        """Stop patcher."""
        cls.get_patcher.stop()