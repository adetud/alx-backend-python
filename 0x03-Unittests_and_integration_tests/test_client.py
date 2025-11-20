#!/usr/bin/env python3
"""Unit and integration tests for client.py ALX project."""

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
        """Test that org returns correct payload and calls get_json once."""
        client = GithubOrgClient(org_name)
        client.org()
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct URL from org payload."""
        client = GithubOrgClient("test_org")
        payload = {"repos_url": "http://api.example.com/repos"}

        with patch.object(GithubOrgClient, "org", return_value=payload) as mock_org:
            result = client._public_repos_url
            self.assertEqual(result, "http://api.example.com/repos")
            mock_org.assert_called_once()

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns a list of repo names."""
        client = GithubOrgClient("test_org")
        mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]

        with patch.object(GithubOrgClient, "_public_repos_url",
                          new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://api.example.com/repos"
            result = client.public_repos
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
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Mock get_json to return fixture payloads."""
        cls.get_patcher = patch("client.get_json")
        mock_get = cls.get_patcher.start()

        # Return org_payload or repos_payload depending on URL
        def side_effect(url):
            if url == "https://api.github.com/orgs/google":
                return cls.org_payload
            return cls.repos_payload

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected list of repo names."""
        client = GithubOrgClient("google")
        result = client.public_repos
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filtered by license returns expected repos."""
        client = GithubOrgClient("google")
        # Filter repos_payload by license
        result = [
            repo["name"] for repo in self.repos_payload
            if GithubOrgClient.has_license(repo, "apache-2.0")
        ]
        self.assertEqual(result, self.apache2_repos)