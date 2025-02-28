from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext 
from pydantic_ai.models.gemini import GeminiModel
import logging
from typing import Optional
import logging  # Import the logging module
from typing import List, Optional

# 1. Create a Pydantic Model for JQL Parameters
class JQLParams(BaseModel):
    project_key: Optional[str] = Field(None, description="The key of the Jira project")
    assignee: Optional[str] = Field(None, description="The username of the assignee")
    status: Optional[str] = Field(None, description="The status of the issue (e.g., 'To Do', 'In Progress')")
    # Add other parameters as needed, with descriptions

class JiraIssueParams(BaseModel):
    project_key: str = 'KAN'
    summary: str
    description_init: str
    issue_type: str
    parent_key: Optional[str] = None
    assignee: Optional[str] = None
    priority: Optional[str] = None
    labels: Optional[List[str]] = None
    components: Optional[List[str]] = None
    due_date: Optional[str] = None
    sprint: Optional[str] = None
    story_points: Optional[int] = None
    watchers: Optional[List[str]] = None
    environment: Optional[str] = None
    affects_versions: Optional[List[str]] = None
    fix_versions: Optional[List[str]] = None

class JiraAIController:
    def __init__(self, jira_instance, issues_handler,post_jira,post_jira_controller):
        """
        Initializes the AI agent with externally provided Jira instances.
        
        Args:
            jira_instance (GetJiraIssues): Instance responsible for Jira API interactions.
            issues_handler (GetIssues): Instance responsible for handling Jira issue retrieval logic.
        """

        self.jira_instance = jira_instance
        self.issues_handler = issues_handler
        self.post_jira = post_jira
        self.post_jira_controller = post_jira_controller

        model = GeminiModel('gemini-2.0-flash-exp', api_key='AIzaSyDX8cPP9J3EXEQqFB-XpQ6HumU4zQ16u8A')
        # Create AI Agent
        self.agent = Agent(
            model,
            system_prompt=(
                "You are a Jira assistant that retrieves and explain in very detail about the different Jira issues/tickets. "
                "Choose the appropriate function to call from GetIssues, passing parameters only when necessary."
                "You have the ability to create new Jira Epic issues and assign them to users."
                
            ),
        )

        # Register agent tools
        self.register_tools()

    def register_tools(self):
        """Register Jira issue fetching functions as AI tools."""
        
        @self.agent.tool
        def post_jira_issues(
            ctx: RunContext,
            issue_params: JiraIssueParams
        ) -> dict:
            """Creates a new Jira issue.
            
            Args:
                ctx: The run context for the agent
                issue_params: Dictionary containing all issue parameters including:
                    - project_key: The project where the issue will be created (default: 'KAN')
                    - summary: The title/summary of the issue
                    - description_init: The description of the issue
                    - issue_type: The type of issue to create
                    - parent_key: The key of the parent issue if this is a sub-task (optional)
                    - assignee: Username of the assignee (optional)
                    - priority: Issue priority level (optional)
                    - labels: List of labels to apply (optional)
                    - components: List of components to assign (optional)
                    - due_date: Due date in YYYY-MM-DD format (optional)
                    - sprint: Sprint name or ID (optional)
                    - story_points: Number of story points (optional)
                    - watchers: List of usernames to add as watchers (optional)
                    - environment: Environment specification (optional)
                    - affects_versions: List of affected versions (optional)
                    - fix_versions: List of fix versions (optional)
            
            Returns:
                dict: The created Jira issue data
            """
            print("tool used is post_jira_issues")
            return self.post_jira_controller.PostIssues(
                controller=self.post_jira,
                **issue_params.model_dump()
            )
        
        @self.agent.tool
        def get_child_for_epic_jira_issues(ctx: RunContext, epic_key: str = "KAN-1") -> list:
            print("tool used is get_child_for_epic_jira_issues")
            """Fetches child issues for a specific Epic in Jira."""
            return self.issues_handler.GetChildForEpicJiraIssues(self.jira_instance, epic_key)

        @self.agent.tool
        def get_issues_by_issuetype(ctx: RunContext, issue_type: str, max_results: int = 100) -> list:
            """Fetches Jira issues of a specific issue type."""
            print("tool used is get_issues_by_issuetype")
            return self.issues_handler.get_issues_by_issuetype(self.jira_instance, issue_type, max_results)


        @self.agent.tool
        def get_issues_by_reporter(ctx: RunContext, reporter: str, max_results: int = 100) -> list:
            """Fetches Jira issues reported by a specific user."""
            print("tool used is get_issues_by_reporter")
            return self.issues_handler.get_issues_by_reporter(self.jira_instance, reporter, max_results)

        
        @self.agent.tool
        def get_issues_by_predefined_jql(ctx: "RunContext", query_type: str, params: JQLParams) -> list: #Changed here
            """
            Retrieves Jira issues using a predefined JQL template.

            Args:
                query_type (str): The type of query to run (e.g., "by_project", "by_assignee").
                params (JQLParams):  The parameters for the JQL template.
            Returns:
                list: Jira issues matching the query.
            """
            print("tool used is get_issues_by_predefined_jql")
            try:
                # Convert the Pydantic model to a dictionary, excluding None values
                param_dict = params.dict(exclude_none=True)  # IMPORTANT: Exclude None values
                param_dict["query_type"] = query_type #add to the dict
                jql_query = self.jira_instance.generate_jql(**param_dict) #pass all as kwargs
                return self.issues_handler.get_issues_by_jql(self.jira_instance, jql_query)
            except ValueError as e:
                return {"error": str(e)}

        @self.agent.tool
        def search_issues_by_text(ctx: RunContext, text: str, max_results: int = 100) -> list:
            """Searches Jira issues/tickets for a specific text string. if the the query does not specify any type of issue then we do this search by text"""
            print("tool used is search_issues_by_text")
            return self.issues_handler.search_issues_by_text(self.jira_instance, text, max_results)
        
        @self.agent.tool
        def get_issue_by_key(ctx: RunContext, issue_key: str) -> dict:  # Changed return type to dict
            """Retrieves a single Jira issue/ticket by its key.  Returns a dictionary representing the issue. The key should always be in Capital letters."""
            print("tool used is get_issue_by_key")
            return self.issues_handler.get_issue_by_key(self.jira_instance, issue_key)





    def process_query(self, query: str):
        """Process a user query, log the tool being used, and return the result."""

        # Hook to log tool calls
        def tool_call_hook(tool_name, args, kwargs):
            logging.info(f"🔍 AI is calling tool: {tool_name} with args={args} kwargs={kwargs}")

        
        # Run the query
        result = self.agent.run_sync(query)

        return result.data
