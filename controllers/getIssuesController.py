class GetIssues:
    def __init__(self):
        pass
    
    def GetEpicJiraIssues(self, jira):  
        return jira.get_jira_issues(jql="issuetype = Epic ORDER BY created DESC", max_results=100)    

    def GetNonEpicJiraIssues(self, jira):  
        return jira.get_jira_issues(jql="issuetype != Epic ORDER BY created DESC", max_results=100) 

    def GetAllJiraIssues(self, jira):  
        return jira.get_jira_issues(max_results=100)

    def GetChildForEpicJiraIssues(self, jira,epic_key = "KAN-1"): 
        
        jql_query = f'"parent" = "{epic_key}"'
        return jira.get_jira_issues(jql=jql_query, max_results=100)   
    
    def get_issues_by_jql(self,jira, jql, max_results=100):
        return jira.get_jira_issues(jql=jql, max_results=max_results)
    
    def get_issues_by_project(self,jira, project_key, max_results=100):
        jql_query = f"project = {project_key} ORDER BY created DESC"
        return jira.get_jira_issues(jql=jql_query, max_results=max_results)

    def get_issues_by_issuetype(self,jira, issue_type, max_results=100):
        jql_query = f"issuetype = '{issue_type}' ORDER BY created DESC" # Quote issue type
        return jira.get_jira_issues(jql=jql_query, max_results=max_results)

    def get_issues_by_status(self,jira, status, max_results=100):
        jql_query = f"status = '{status}' ORDER BY created DESC" # Quote status
        return jira.get_jira_issues(jql=jql_query, max_results=max_results)

    def get_issues_by_assignee(self,jira, assignee, max_results=100):
        jql_query = f"assignee = '{assignee}' ORDER BY created DESC" # Quote assignee
        return jira.get_jira_issues(jql=jql_query, max_results=max_results)

    def get_issues_by_reporter(self,jira, reporter, max_results=100):
        jql_query = f"reporter = '{reporter}' ORDER BY created DESC" # Quote reporter
        return jira.get_jira_issues(jql=jql_query, max_results=max_results)

    def get_issues_created_after(self,jira, date_str, max_results=100): #YYYY-MM-DD
        jql_query = f"created >= '{date_str}' ORDER BY created DESC"
        return jira.get_jira_issues(jql=jql_query, max_results=max_results)

    def get_issues_created_before(self,jira, date_str, max_results=100): #YYYY-MM-DD
        jql_query = f"created <= '{date_str}' ORDER BY created DESC"
        return jira.get_jira_issues(jql=jql_query, max_results=max_results)

    def search_issues_by_text(self,jira, text, max_results=100):
        jql_query = f"text ~ '{text}' ORDER BY created DESC"
        return jira.get_jira_issues(jql=jql_query, max_results=max_results)


    # Example of combining queries (e.g. issues in a project assigned to someone)
    def get_issues_in_project_assigned_to(self,jira, project_key, assignee, max_results=100):
        jql_query = f"project = {project_key} AND assignee = '{assignee}' ORDER BY created DESC"
        return jira.get_jira_issues(jql=jql_query, max_results=max_results)
    
    def get_issue_by_key(self,jira, issue_key):
        """Retrieves a single issue by its key."""
        return jira.get_jira_ticket(issue_key)  # Most Jira libraries have a get_issue method
         