#!/usr/bin/env python3
"""GithubOrgClient module for ALX 0x03 project."""

from typing import List, Dict
from utils import get_json, memoize


class GithubOrgClient:
    """Client to access GitHub organization data."""

    def __init__(self, org_name: str):
        """Initialize with the organization name."""
        self.org_name = org_name

    def org(self) -> Dict:
        """Return the organization payload as a dictionary."""
        return get_json(f"https://api.github.com/orgs/{self.org_name}")

    @property
    def _public_repos_url(self) -> str:
        """Return the repos_url from the organization payload."""
        return self.org()["repos_url"]

    @memoize
    def public_repos(self) -> List[str]:
        """Return a list of public repository names for the org."""
        repos_data = get_json(self._public_repos_url)
        return [repo["name"] for repo in repos_data]

    @staticmethod
    def has_license(repo: Dict, license_key: str) -> bool:
        """Check if a repository has a specific license key."""
        license_info = repo.get("license")
        if license_info is None:
            return False
        return license_info.get("key") == license_key