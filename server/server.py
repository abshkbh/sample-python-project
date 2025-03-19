import threading
import time
from datetime import datetime
from typing import Dict, List, Optional, Any


class Task:
    """Represents a task in the system."""
    
    def __init__(self, name: str, description: str, priority: str = "", due_date: str = ""):
        self.name = name
        self.description = description
        self.status = "pending"
        self.priority = priority
        self.due_date = due_date
        self.assignee = ""
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.comments: List[str] = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary for JSON serialization."""
        return {
            "taskName": self.name,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "dueDate": self.due_date,
            "assignee": self.assignee if self.assignee else None,
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat(),
            "comments": self.comments
        }


class TaskServer:
    """Server that manages tasks."""
    
    def __init__(self, config):
        self.config = config
        self.tasks: Dict[str, Task] = {}
        self.lock = threading.RLock()
    
    def create_task(self, task_name: str, description: str, priority: str = "", due_date: str = "") -> Dict[str, Any]:
        """Create a new task."""
        with self.lock:
            if task_name in self.tasks:
                raise ValueError(f"Task '{task_name}' already exists")
            
            task = Task(
                name=task_name,
                description=description,
                priority=priority,
                due_date=due_date
            )
            self.tasks[task_name] = task
            
            return task.to_dict()
    
    def delete_task(self, task_name: str) -> Dict[str, Any]:
        """Delete a task by name."""
        with self.lock:
            if task_name not in self.tasks:
                raise ValueError(f"Task '{task_name}' not found")
            
            task = self.tasks.pop(task_name)
            return task.to_dict()
    
    def delete_all_tasks(self) -> Dict[str, List[Dict[str, Any]]]:
        """Delete all tasks."""
        with self.lock:
            tasks = [task.to_dict() for task in self.tasks.values()]
            self.tasks.clear()
            return {"tasks": tasks}
    
    def list_all_tasks(self) -> Dict[str, List[Dict[str, Any]]]:
        """Return a list of all tasks."""
        with self.lock:
            return {"tasks": [task.to_dict() for task in self.tasks.values()]}
    
    def get_task(self, task_name: str) -> Dict[str, Any]:
        """Get a specific task by name."""
        with self.lock:
            if task_name not in self.tasks:
                raise ValueError(f"Task '{task_name}' not found")
            
            return self.tasks[task_name].to_dict()
    
    def update_task_status(self, task_name: str, status: str) -> Dict[str, Any]:
        """Update the status of a task."""
        with self.lock:
            if task_name not in self.tasks:
                raise ValueError(f"Task '{task_name}' not found")
            
            task = self.tasks[task_name]
            task.status = status
            task.updated_at = datetime.now()
            
            return task.to_dict()
    
    def assign_task(self, task_name: str, assignee: str) -> Dict[str, Any]:
        """Assign a task to a person."""
        with self.lock:
            if task_name not in self.tasks:
                raise ValueError(f"Task '{task_name}' not found")
            
            task = self.tasks[task_name]
            task.assignee = assignee
            task.updated_at = datetime.now()
            
            return task.to_dict()
    
    def add_task_comment(self, task_name: str, comment: str) -> Dict[str, Any]:
        """Add a comment to a task."""
        with self.lock:
            if task_name not in self.tasks:
                raise ValueError(f"Task '{task_name}' not found")
            
            task = self.tasks[task_name]
            task.comments.append(comment)
            task.updated_at = datetime.now()
            
            return task.to_dict()
    
    def get_task_comments(self, task_name: str) -> Dict[str, List[str]]:
        """Get all comments for a task."""
        with self.lock:
            if task_name not in self.tasks:
                raise ValueError(f"Task '{task_name}' not found")
            
            return {"comments": self.tasks[task_name].comments}
