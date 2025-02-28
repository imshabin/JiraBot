from typing import Dict, Any

class Issuer:
    def __init__(self):
        pass

    def PostIssues(self, controller, **params: Dict[str, Any]):  
        return controller.create_jira_ticket(**params)