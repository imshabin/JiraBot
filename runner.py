from controllers.jiraController import GetJiraIssues
from controllers.getIssuesController import GetIssues
from controllers.IssueController import Issuer 
# from utils.jsonParser import print_filtered_json_data as jsonparser
from Issuer.IssueCreator import CreateOrLinkJiraTicket

# from Issuer.IssueCreator import CloneJiraTicket
from Agent.tools import JiraAIController
import nest_asyncio
nest_asyncio.apply()

def runner():
    """
    Main runner function to fetch and print Jira issue details.
    """

 
    ###############
    # ai agents
    ###############
    post_jira = CreateOrLinkJiraTicket()
    jira_instance = GetJiraIssues()
    issues_handler = GetIssues()
    post_jira_controller = Issuer()
    # Pass them to JiraAIController
    jira_ai = JiraAIController(jira_instance, issues_handler, post_jira,post_jira_controller)

    # # Process queries
    query ="""
 create a task ticket.assign it to shabin. summary=test,decription=test 
"""
    result1 = jira_ai.process_query(query)     
    print(result1)


    # result2 = jira_ai.process_query("Get child issues for epic KAN-1")
    # print(result2)



def main():
    """
    runs the code.
    """
    runner()


if __name__ == "__main__":
    main()






