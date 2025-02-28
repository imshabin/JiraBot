import json

def print_filtered_json_data(issue_data):
    """
    Prints only the specified fields from the JSON response.

    Args:
        issue_data (dict): The JSON data containing Jira issue details.
    """
    print(f"Issue Key: {issue_data['key']}")  # Always print the issue key

    fields = issue_data.get("fields", {})  # Get the 'fields' dictionary

    # Print only hardcoded fields
    if "summary" in fields:
        print(f"  Summary: {fields['summary']}")

    if "parent" in fields:
        parent_name = fields["parent"].get("key", "Unknown id")
        print(f"  Parent: {parent_name}")

    if "status" in fields:
        status_name = fields["status"].get("name", "Unknown Status")  # Extracting status name
        print(f"  Status: {status_name}")

    print("-" * 30)