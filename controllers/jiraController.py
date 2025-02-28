import requests

jql_templates = {
    "by_project": "project = {project_key}",
    "by_assignee": "assignee = '{assignee}'",
    "by_status": "status = {status}",
    "by_date_range": "created >= {start_date} AND created <= {end_date}",
    "complex_query": "project = {project_key} AND assignee = {assignee}",
    "text_search": "text ~ '{text}'"
}
# Auth and Jira URL
JIRA_URL = "https://imshabin.atlassian.net"
JIRA_USER = "imshabin@gmail.com"  # Your Jira username or email
JIRA_API_TOKEN = "ATATT3xFfGF0FTfgtosPi4EAXf_yXkRfhxemo6fove9etYm9lGgflMLTRA9XaD9SIuHQ5AR9cpb3f-yf3T6Ihpix3BYQBnjWZkBcTee4fKqsQAeOsjYpx2fHKhmbQuttan3vVzA0xjtPa5eMH4ZZtWXbVqSl5nt68dCqOvu67-BFeAczo4tX0og=8A727355"  # Your Jira API token


class GetJiraIssues:
    """
    A class to interact with the Jira API to fetch issue data.
    """
    def __init__(self):
        """
        Initializes the GetJiraIssues class with Jira API credentials and URL.
        """
        self.jira_url = JIRA_URL
        self.jira_user = JIRA_USER
        self.auth = (JIRA_USER, JIRA_API_TOKEN)

    def get_jira_issues(self, jql="ORDER BY created DESC", max_results=100):
        """
        Fetches Jira issues based on a JQL query.

        Args:
            jql (str): Jira Query Language string to filter issues. Defaults to "ORDER BY created DESC" (all issues sorted by creation date).
            max_results (int): Maximum number of issues to retrieve. Defaults to 100 (Jira API limit is usually 1000).

        Returns:
            list: A list of dictionaries, where each dictionary represents a Jira issue.
                  Returns None if there is an error fetching issues.
        """
        url = f"{self.jira_url}/rest/api/2/search"
        headers = {"Accept": "application/json"}
        params = {
            "jql": jql,
            "maxResults": max_results,
            "fields": "summary,status,key,parent"  # Fetch essential fields
        }

        try:
            response = requests.get(url, auth=self.auth, headers=headers, params=params)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            data = response.json()
            # print(json.dumps(data.get("issues", []), indent=4))
            return data.get("issues", [])  # Return list of issue dictionaries
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Jira issues: {e}")
            return None

        
    def get_jira_ticket(self,issue_key):
        url = f"{self.jira_url}/rest/api/2/issue/{issue_key}"

        headers = {"Accept": "application/json"}  # Important: Specify JSON

        try:
            response = requests.get(url, auth=self.auth, headers=headers)
            response.raise_for_status()
            print(response.json())  # Raise an exception for bad status codes (4xx or 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Jira ticket: {e}")
            return None   
        
    # In GetJiraIssues class
    def generate_jql(self, **kwargs) -> str:  # Remove query_type
        """
        Generates a JQL query based on a predefined template and user-provided parameters.

        Args:
            kwargs: Dynamic values like project_key, assignee, status, etc.

        Returns:
            str: The formatted JQL query.
        """
        query_type = kwargs.pop("query_type") #get from kwargs and remove
        if query_type not in jql_templates:
            raise ValueError(f"Invalid query type: {query_type}")

        try:
            jql_query = jql_templates[query_type].format(**kwargs)
            print(jql_query)
            return jql_query
        except KeyError as e:
            raise ValueError(f"Missing required parameter: {e}") 