org_payload = {"repos_url": "http://api.example.com/repos"}
repos_payload = [{"name": "repo1"}, {"name": "repo2", "license": {"key": "apache-2.0"}}]
expected_repos = ["repo1", "repo2"]
apache2_repos = ["repo2"]
