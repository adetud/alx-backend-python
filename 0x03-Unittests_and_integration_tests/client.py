#!/usr/bin/env python3
"""GithubOrgClient module."""

from typing import List, Dict
import requests
from utils import get_json, memoize


class GithubOrgClient:
    """Github Org client to access Github API."""

    def __init__(self, org_name: str):
        """Initialize with organization name."""
        self.org_name = org_name

    def org(self) -> Dict:
        """Return the JSON payload of the organization."""
        return get_json(f"https://api.github.com/orgs/{self.org_name}")

    @property
    def _public_repos_url(self) -> str:
        """Return the repos URL from the organization payload."""
        return self.org()["repos_url"]

    @memoize
    def public_repos(self) -> List[str]:
        """Return the list of public repository names for the organization."""
        repos_data = get_json(self._public_repos_url)
        return [repo["name"] for repo in repos_data]

    @staticmethod
    def has_license(repo: Dict, license_key: str) -> bool:
        """Return True if repo has the specified license key."""
        license_info = repo.get("license")
        if license_info is None:
            return False
        return license_info.get("key") == license_key
