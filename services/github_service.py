import requests
import os
import logging

logger = logging.getLogger(__name__)

def create_github_issue(title, body):
    """
    Creates an issue on GitHub using the configured token and repository.
    """
    token = os.environ.get('GITHUB_TOKEN')
    owner = os.environ.get('GITHUB_OWNER')
    repo = os.environ.get('GITHUB_REPO')

    if not all([token, owner, repo]):
        logger.warning("GitHub integration not configured. Skipping issue creation.")
        return None

    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "title": title,
        "body": body
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 201:
            issue_data = response.json()
            return issue_data.get('html_url')
        else:
            logger.error(f"GitHub API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logger.error(f"GitHub integration failed: {str(e)}")
        return None
