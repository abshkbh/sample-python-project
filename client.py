#!/usr/bin/env python3
import argparse
import json
import sys
import requests
from typing import Dict, Any, Optional
from urllib.parse import quote


class TaskClient:
    """Client for interacting with the task server."""
    
    def __init__(self, server_url: str = "http://localhost:8080"):
        self.server_url = server_url
        self.session = requests.Session()
    
    def create_task(self, name: str, description: str, priority: str = "", due_date: str = "") -> None:
        """Create a new task."""
        data = {
            "taskName": name,
            "description": description
        }
        
        if priority:
            data["priority"] = priority
        if due_date:
            data["dueDate"] = due_date
        
        response = self.session.post(f"{self.server_url}/tasks", json=data)
        self._check_response(response)
        
        print(f"Task '{name}' created successfully")
    
    def list_tasks(self) -> None:
        """List all tasks."""
        response = self.session.get(f"{self.server_url}/tasks")
        self._check_response(response)
        
        data = response.json()
        tasks = data.get("tasks", [])
        
        if not tasks:
            print("No tasks found")
            return
        
        print("Tasks:")
        print("------")
        for task in tasks:
            self._print_task(task)
    
    def get_task(self, name: str) -> None:
        """Get a specific task by name."""
        response = self.session.get(f"{self.server_url}/tasks/{quote(name)}")
        self._check_response(response)
        
        task = response.json()
        self._print_task(task)
    
    def update_task_status(self, name: str, status: str) -> None:
        """Update the status of a task."""
        data = {"status": status}
        response = self.session.patch(f"{self.server_url}/tasks/{quote(name)}", json=data)
        self._check_response(response)
        
        print(f"Task '{name}' status updated to '{status}'")
    
    def assign_task(self, name: str, assignee: str) -> None:
        """Assign a task to a person."""
        data = {"assignee": assignee}
        response = self.session.post(f"{self.server_url}/tasks/{quote(name)}/assign", json=data)
        self._check_response(response)
        
        print(f"Task '{name}' assigned to '{assignee}'")
    
    def add_comment(self, name: str, comment: str) -> None:
        """Add a comment to a task."""
        data = {"comment": comment}
        response = self.session.post(f"{self.server_url}/tasks/{quote(name)}/comments", json=data)
        self._check_response(response)
        
        print(f"Comment added to task '{name}'")
    
    def delete_task(self, name: str) -> None:
        """Delete a task by name."""
        response = self.session.delete(f"{self.server_url}/tasks/{quote(name)}")
        self._check_response(response)
        
        print(f"Task '{name}' deleted successfully")
    
    def delete_all_tasks(self) -> None:
        """Delete all tasks."""
        response = self.session.delete(f"{self.server_url}/tasks")
        self._check_response(response)
        
        print("All tasks deleted successfully")
    
    def _check_response(self, response: requests.Response) -> None:
        """Check if the response is successful, raise an exception if not."""
        if response.status_code != 200:
            error_msg = "Unknown error"
            try:
                error_data = response.json()
                if "error" in error_data and "message" in error_data["error"]:
                    error_msg = error_data["error"]["message"]
            except:
                error_msg = response.text
            
            print(f"Error: {error_msg} (Status code: {response.status_code})")
            sys.exit(1)
    
    def _print_task(self, task: Dict[str, Any]) -> None:
        """Print a task in a readable format."""
        print(f"Task: {task.get('taskName', 'Unknown')}")
        print(f"Description: {task.get('description', '')}")
        print(f"Status: {task.get('status', '')}")
        print(f"Priority: {task.get('priority', '')}")
        print(f"Due Date: {task.get('dueDate', '')}")
        
        if task.get('assignee'):
            print(f"Assignee: {task['assignee']}")
        
        print(f"Created: {task.get('createdAt', '')}")
        print(f"Updated: {task.get('updatedAt', '')}")
        
        if task.get('comments') and len(task['comments']) > 0:
            print("Comments:")
            for comment in task['comments']:
                print(f"  - {comment}")
        
        print()


def main():
    parser = argparse.ArgumentParser(description="Task Management Client")
    parser.add_argument("--server", default="http://localhost:8080", help="Server URL")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Create task command
    create_parser = subparsers.add_parser("create", help="Create a new task")
    create_parser.add_argument("name", help="Task name")
    create_parser.add_argument("description", help="Task description")
    create_parser.add_argument("--priority", help="Task priority")
    create_parser.add_argument("--due-date", help="Task due date")
    
    # List tasks command
    subparsers.add_parser("list", help="List all tasks")
    
    # Get task command
    get_parser = subparsers.add_parser("get", help="Get a specific task")
    get_parser.add_argument("name", help="Task name")
    
    # Update task status command
    update_parser = subparsers.add_parser("update", help="Update task status")
    update_parser.add_argument("name", help="Task name")
    update_parser.add_argument("status", choices=["pending", "in-progress", "completed"], help="New status")
    
    # Assign task command
    assign_parser = subparsers.add_parser("assign", help="Assign task to someone")
    assign_parser.add_argument("name", help="Task name")
    assign_parser.add_argument("assignee", help="Assignee name")
    
    # Add comment command
    comment_parser = subparsers.add_parser("comment", help="Add comment to task")
    comment_parser.add_argument("name", help="Task name")
    comment_parser.add_argument("comment", help="Comment text")
    
    # Delete task command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("name", help="Task name")
    
    # Delete all tasks command
    subparsers.add_parser("delete-all", help="Delete all tasks")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    client = TaskClient(args.server)
    
    if args.command == "create":
        client.create_task(args.name, args.description, args.priority, args.due_date)
    elif args.command == "list":
        client.list_tasks()
    elif args.command == "get":
        client.get_task(args.name)
    elif args.command == "update":
        client.update_task_status(args.name, args.status)
    elif args.command == "assign":
        client.assign_task(args.name, args.assignee)
    elif args.command == "comment":
        client.add_comment(args.name, args.comment)
    elif args.command == "delete":
        client.delete_task(args.name)
    elif args.command == "delete-all":
        client.delete_all_tasks()


if __name__ == "__main__":
    main()
