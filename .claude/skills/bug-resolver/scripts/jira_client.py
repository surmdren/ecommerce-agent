#!/usr/bin/env python3
"""
Jira API Client for Bug Fixer Skill

Handles Jira ticket fetching and updating operations.
Requires environment variables:
- JIRA_URL: Jira instance URL (e.g., https://your-company.atlassian.net)
- JIRA_EMAIL: Jira user email
- JIRA_API_TOKEN: Jira API token
"""

import os
import sys
import json
from typing import Dict, List, Optional
import requests
from requests.auth import HTTPBasicAuth


class JiraClient:
    def __init__(self):
        self.url = os.getenv("JIRA_URL")
        self.email = os.getenv("JIRA_EMAIL")
        self.token = os.getenv("JIRA_API_TOKEN")

        if not all([self.url, self.email, self.token]):
            raise ValueError(
                "Missing required environment variables: JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN"
            )

        self.auth = HTTPBasicAuth(self.email, self.token)
        self.headers = {"Accept": "application/json", "Content-Type": "application/json"}

    def get_bug(self, ticket_id: str) -> Dict:
        """Fetch a single bug ticket by ID"""
        url = f"{self.url}/rest/api/3/issue/{ticket_id}"
        response = requests.get(url, headers=self.headers, auth=self.auth)
        response.raise_for_status()
        return response.json()

    def search_bugs(self, jql: str, max_results: int = 50) -> List[Dict]:
        """Search bugs using JQL query"""
        url = f"{self.url}/rest/api/3/search"
        payload = {"jql": jql, "maxResults": max_results}
        response = requests.post(url, json=payload, headers=self.headers, auth=self.auth)
        response.raise_for_status()
        return response.json().get("issues", [])

    def update_bug(
        self,
        ticket_id: str,
        comment: str,
        status: Optional[str] = None,
        labels: Optional[List[str]] = None
    ) -> Dict:
        """Update bug ticket with fix details"""
        # Add comment
        comment_url = f"{self.url}/rest/api/3/issue/{ticket_id}/comment"
        comment_payload = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": comment}]
                    }
                ]
            }
        }
        response = requests.post(
            comment_url, json=comment_payload, headers=self.headers, auth=self.auth
        )
        response.raise_for_status()

        # Update status if provided
        if status:
            transition_url = f"{self.url}/rest/api/3/issue/{ticket_id}/transitions"
            transitions = requests.get(
                transition_url, headers=self.headers, auth=self.auth
            ).json()

            target_transition = None
            for t in transitions.get("transitions", []):
                if t["name"].lower() == status.lower():
                    target_transition = t["id"]
                    break

            if target_transition:
                transition_payload = {"transition": {"id": target_transition}}
                requests.post(
                    transition_url,
                    json=transition_payload,
                    headers=self.headers,
                    auth=self.auth
                )

        # Update labels if provided
        if labels:
            update_url = f"{self.url}/rest/api/3/issue/{ticket_id}"
            update_payload = {"update": {"labels": [{"add": label} for label in labels]}}
            requests.put(
                update_url, json=update_payload, headers=self.headers, auth=self.auth
            )

        return {"success": True, "ticket_id": ticket_id}

    def format_bug_info(self, bug_data: Dict) -> str:
        """Format bug data into readable text"""
        fields = bug_data.get("fields", {})
        return f"""
Ticket ID: {bug_data.get('key')}
Summary: {fields.get('summary')}
Description: {fields.get('description', {}).get('content', [{}])[0].get('content', [{}])[0].get('text', 'N/A')}
Status: {fields.get('status', {}).get('name')}
Priority: {fields.get('priority', {}).get('name')}
Reporter: {fields.get('reporter', {}).get('displayName')}
Assignee: {fields.get('assignee', {}).get('displayName', 'Unassigned')}
Created: {fields.get('created')}
Labels: {', '.join(fields.get('labels', []))}
"""


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Get bug: python jira_client.py get TICKET-123")
        print("  Search bugs: python jira_client.py search 'project=PROJ AND type=Bug'")
        print("  Update bug: python jira_client.py update TICKET-123 'Fixed the issue'")
        sys.exit(1)

    client = JiraClient()
    action = sys.argv[1]

    try:
        if action == "get" and len(sys.argv) >= 3:
            ticket_id = sys.argv[2]
            bug = client.get_bug(ticket_id)
            print(client.format_bug_info(bug))

        elif action == "search" and len(sys.argv) >= 3:
            jql = sys.argv[2]
            bugs = client.search_bugs(jql)
            for bug in bugs:
                print(client.format_bug_info(bug))
                print("-" * 80)

        elif action == "update" and len(sys.argv) >= 4:
            ticket_id = sys.argv[2]
            comment = sys.argv[3]
            status = sys.argv[4] if len(sys.argv) >= 5 else None
            result = client.update_bug(ticket_id, comment, status)
            print(f"Updated {result['ticket_id']} successfully")

        else:
            print("Invalid arguments")
            sys.exit(1)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
