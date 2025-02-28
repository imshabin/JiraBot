from requests.auth import HTTPBasicAuth
import requests
from utils.payoadParser import parsePayload
# from utils.getAssignees import GetAssignees
JIRA_URL = "https://imshabin.atlassian.net"
JIRA_USER = "imshabin@gmail.com"  # Your Jira username or email
JIRA_API_TOKEN = "ATATT3xFfGF0FTfgtosPi4EAXf_yXkRfhxemo6fove9etYm9lGgflMLTRA9XaD9SIuHQ5AR9cpb3f-yf3T6Ihpix3BYQBnjWZkBcTee4fKqsQAeOsjYpx2fHKhmbQuttan3vVzA0xjtPa5eMH4ZZtWXbVqSl5nt68dCqOvu67-BFeAczo4tX0og=8A727355"# Your Jira API token
postauth = HTTPBasicAuth(JIRA_USER, JIRA_API_TOKEN)


class CreateOrLinkJiraTicket:
    def __init__(self):
        pass


    def create_jira_ticket(self, **params):
        """
        Create a Jira issue.
        
        Args:
            **params: Dictionary containing all Jira issue parameters
                Required: project_key, summary, description, issue_type
                Optional: parent_key, assignee, priority, labels, etc.
        """
        url = f"{JIRA_URL}/rest/api/2/issue"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        # Pass all parameters to generate_jira_payload
        payload = parsePayload.generate_jira_payload(**params)

        try:
            response = requests.post(url, auth=postauth, headers=headers, json=payload)
            response.raise_for_status()
            issue_key = response.json().get("key")
            print(f"✅ Issue created successfully: {issue_key}")
            return issue_key
        except requests.exceptions.RequestException as e:
            print(f"❌ Error creating Jira issue: {e}")
            if response is not None:
                print(f"Response: {response.text}")
            return None
        

    