from jira import JIRA

jira_url = "https://imshabin.atlassian.net"
jira_email = "imshabin@gmail.com"  # Your Jira username or email
jira_token = "ATATT3xFfGF0FTfgtosPi4EAXf_yXkRfhxemo6fove9etYm9lGgflMLTRA9XaD9SIuHQ5AR9cpb3f-yf3T6Ihpix3BYQBnjWZkBcTee4fKqsQAeOsjYpx2fHKhmbQuttan3vVzA0xjtPa5eMH4ZZtWXbVqSl5nt68dCqOvu67-BFeAczo4tX0og=8A727355"# Your Jira API token
jira = JIRA(
        server=jira_url,
        basic_auth=(jira_email, jira_token)
    )


class parsePayload:
    def __init__(self):
        self.assignees = self.get_assignees()  # Initialize assignees in constructor
    
    @staticmethod
    def get_assignees():
        try:
            users = jira.search_users(query='%', maxResults=1000)
            
            assignee_map = {}
            system_accounts = [
                'Alert Integration', 'Atlas for Jira Cloud', 'Atlassian Assist',
                'Automation for Jira', 'Chat Notifications', 'Confluence Analytics',
                'Jira Outlook', 'Jira Service Management', 'Jira Spreadsheets',
                'Microsoft Teams', 'Opsgenie', 'Proforma', 'Slack', 'Statuspage',
                'Trello'
            ]
            
            for user in users:
                # Skip system accounts
                if any(system in user.displayName for system in system_accounts):
                    continue
                    
                try:
                    # Store multiple variations of the name
                    full_name = user.displayName
                    assignee_map[full_name] = {
                        'accountId': user.accountId,
                        'displayName': full_name,
                        'searchTerms': set([
                            full_name.lower(),
                            *[part.lower() for part in full_name.split()]
                        ])
                    }
                except AttributeError as e:
                    print(f"Skipping user due to missing attribute: {e}")
                    
            return assignee_map
        
        except Exception as e:
            print(f"Error getting assignees: {str(e)}")
            return {}

    @classmethod
    def find_assignee(cls, partial_name):
        assignees = cls.get_assignees()  # Use class method to get assignees
        partial_name = partial_name.lower()
        for assignee in assignees.values():
            if partial_name in assignee['searchTerms']:
                return assignee['accountId']
        return None

    def parse_description(input_string):
        """
        Format a string containing a table-like structure with headers and rows.
        Preserves text before and after the table.
        
        Args:
            input_string (str): Input string containing table with headers marked by asterisks
            
        Returns:
            str: Formatted string with proper spacing and capitalization
        """
        # Split at the table markers
        table_split = input_string.split('||')
        
        # Extract text before table
        before_table = table_split[0].strip()
        
        # Find the part containing the table rows
        table_end_index = None
        for i, part in enumerate(table_split):
            if '|' in part and not part.strip().startswith('*'):
                table_end_index = i
                break
                
        if table_end_index is None:
            return input_string
        
        # Get headers
        headers = []
        for header in table_split[1:table_end_index]:
            # Remove asterisks and transform to title case
            clean_header = header.replace('*', '').strip()
            header_words = clean_header.split()
            capitalized_words = [word.capitalize() for word in header_words]
            headers.append(' '.join(capitalized_words))
        
        # Process table rows
        table_rows_part = table_split[table_end_index]
        rows = [row.strip() for row in table_rows_part.split('|') if row.strip()]
        
        # Group rows into sets of 3 (assuming 3 columns)
        grouped_rows = []
        for i in range(0, len(rows), 3):
            if i + 2 < len(rows):
                grouped_rows.append(rows[i:i+3])
                
        # Extract text after the table rows
        after_table = ' '.join(rows[len(grouped_rows) * 3:]).strip()
        
        # Build output string
        output_parts = []
        
        # Add text before table if it exists
        if before_table:
            output_parts.append(before_table)
        
        # Add headers
        output_parts.append('|| ' + ' || '.join(headers) + ' ||')
        
        # Add rows
        for row in grouped_rows:
            output_parts.append('| ' + ' | '.join(row) + ' |')
        
        # Add text after table if it exists
        if after_table:
            output_parts.append(after_table)
        
        return '\n'.join(output_parts)
    def generate_jira_payload(**params):
        """
        Generate a payload for creating a Jira issue.
        
        Args:
            **params: Dictionary containing:
                project_key (str): The project key where the issue will be created
                summary (str): The summary/title of the issue
                description (str): The description of the issue
                issue_type (str, optional): The type of issue. Defaults to "Task"
                parent_key (str, optional): The key of the parent issue if this is a sub-task
                assignee (str, optional): The account ID of the assignee
        
        Returns:
            dict: A dictionary containing the formatted Jira payload
        """
        # Extract required fields with defaults
        project_key = params.get('project_key')
        summary = params.get('summary')
        description = params.get('description_init', '')  # Note: using description_init as per your previous code
        issue_type = params.get('issue_type', 'Task')
        parent_key = params.get('parent_key')
        assignee = params.get('assignee')

        # Initialize the basic fields that are always required
        fields = {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type},
            "customfield_10016": 3
        }
        
        description = parsePayload.parse_description(description)
        
        # Add optional fields if they are provided
        if parent_key:
            fields["parent"] = {"key": parent_key}
        
        if assignee:
            assignee_id = parsePayload.find_assignee(assignee)
            if assignee_id:
                print(f"Found assignee ID: {assignee_id}")
                fields["assignee"] = {"accountId": assignee_id}
            else:
                print("No matching assignee found")
        
        # Create the final payload structure
        payload = {
            "fields": fields
        }
        
        return payload
    
