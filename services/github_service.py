import requests
import os
import logging

logger = logging.getLogger(__name__)

class GitHubService:
    def __init__(self):
        self.token = os.environ.get('GITHUB_TOKEN')
        self.owner = os.environ.get('GITHUB_OWNER')
        self.repo = os.environ.get('GITHUB_REPO')
        self.base_url = f"https://api.github.com/repos/{self.owner}/{self.repo}"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def is_configured(self):
        return all([self.token, self.owner, self.repo])

    def create_issue(self, title, body):
        if not self.is_configured():
            logger.warning("GitHub integration not configured. Skipping issue creation.")
            return None

        url = f"{self.base_url}/issues"
        payload = {"title": title, "body": body}

        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=10)
            if response.status_code == 201:
                issue_data = response.json()
                return issue_data.get('html_url'), issue_data.get('number')
            else:
                logger.error(f"GitHub API Error: {response.status_code} - {response.text}")
                return None, None
        except Exception as e:
            logger.error(f"GitHub integration failed: {str(e)}")
            return None, None

    def update_issue_status(self, issue_number, status):
        if not self.is_configured() or not issue_number:
            return False

        url = f"{self.base_url}/issues/{issue_number}"
        
        # Map app status to GitHub status
        gh_status = "closed" if status in ['Resolved', 'Closed'] else "open"
        payload = {"state": gh_status}

        try:
            response = requests.patch(url, headers=self.headers, json=payload, timeout=10)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"GitHub status update failed: {str(e)}")
            return False

# Functional wrapper for backward compatibility if needed, but better to use the class
def create_github_issue(title, body):
    service = GitHubService()
    url, _ = service.create_issue(title, body)
    return url
