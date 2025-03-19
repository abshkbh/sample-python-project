import os
import logging
import json
from datetime import datetime
from flask import Flask, request, jsonify, abort
from werkzeug.exceptions import HTTPException

from config import load_config
from server.server import TaskServer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load configuration
config_file = os.environ.get('CONFIG_FILE', 'config.yaml')
try:
    config = load_config(config_file)
    logger.info(f"Loaded configuration from {config_file}")
except Exception as e:
    logger.error(f"Failed to load configuration: {e}")
    config = load_config('config.yaml')

# Create task server
task_server = TaskServer(config)

# Create Flask app
app = Flask(__name__)


class JSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles datetime objects."""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


app.json_encoder = JSONEncoder


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    response = {
        "error": {
            "message": e.description
        }
    }
    return jsonify(response), e.code


@app.errorhandler(ValueError)
def handle_value_error(e):
    """Handle ValueError exceptions."""
    response = {
        "error": {
            "message": str(e)
        }
    }
    return jsonify(response), 400


@app.errorhandler(Exception)
def handle_generic_exception(e):
    """Handle all other exceptions."""
    logger.exception("Unhandled exception")
    response = {
        "error": {
            "message": f"Internal server error: {str(e)}"
        }
    }
    return jsonify(response), 500


@app.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task."""
    logger.info("API: create_task")
    start_time = datetime.now()
    
    data = request.json
    if not data:
        return jsonify({"error": {"message": "Invalid request format"}}), 400
    
    task_name = data.get('taskName')
    if not task_name:
        return jsonify({"error": {"message": "Empty task name"}}), 400
    
    description = data.get('description', '')
    priority = data.get('priority', '')
    due_date = data.get('dueDate', '')
    
    try:
        task = task_server.create_task(task_name, description, priority, due_date)
        elapsed_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"Task '{task_name}' created successfully in {elapsed_time:.2f}s")
        return jsonify(task)
    except Exception as e:
        logger.error(f"Failed to create task '{task_name}': {e}")
        raise


@app.route('/tasks/<name>', methods=['DELETE'])
def delete_task(name):
    """Delete a task by name."""
    logger.info(f"API: delete_task - {name}")
    
    try:
        task = task_server.delete_task(name)
        logger.info(f"Task '{name}' deleted successfully")
        return jsonify(task)
    except Exception as e:
        logger.error(f"Failed to delete task '{name}': {e}")
        raise


@app.route('/tasks', methods=['DELETE'])
def delete_all_tasks():
    """Delete all tasks."""
    logger.info("API: delete_all_tasks")
    
    try:
        result = task_server.delete_all_tasks()
        logger.info("All tasks deleted successfully")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Failed to delete all tasks: {e}")
        raise


@app.route('/tasks', methods=['GET'])
def list_all_tasks():
    """List all tasks."""
    logger.info("API: list_all_tasks")
    
    try:
        tasks = task_server.list_all_tasks()
        return jsonify(tasks)
    except Exception as e:
        logger.error(f"Failed to list all tasks: {e}")
        raise


@app.route('/tasks/<name>', methods=['GET'])
def get_task(name):
    """Get a specific task by name."""
    logger.info(f"API: get_task - {name}")
    
    try:
        task = task_server.get_task(name)
        return jsonify(task)
    except Exception as e:
        logger.error(f"Failed to get task '{name}': {e}")
        raise


@app.route('/tasks/<name>', methods=['PATCH'])
def update_task_status(name):
    """Update the status of a task."""
    logger.info(f"API: update_task_status - {name}")
    
    data = request.json
    if not data:
        return jsonify({"error": {"message": "Invalid request format"}}), 400
    
    status = data.get('status')
    if not status:
        return jsonify({"error": {"message": "Status not provided"}}), 400
    
    if status not in ['completed', 'in-progress', 'pending']:
        return jsonify({"error": {"message": f"Invalid status value: {status}"}}), 400
    
    try:
        task = task_server.update_task_status(name, status)
        logger.info(f"Task '{name}' status updated to '{status}'")
        return jsonify(task)
    except Exception as e:
        logger.error(f"Failed to update task '{name}' status: {e}")
        raise


@app.route('/tasks/<name>/assign', methods=['POST'])
def assign_task(name):
    """Assign a task to a person."""
    logger.info(f"API: assign_task - {name}")
    
    data = request.json
    if not data:
        return jsonify({"error": {"message": "Invalid request format"}}), 400
    
    assignee = data.get('assignee')
    if not assignee:
        return jsonify({"error": {"message": "Assignee not provided"}}), 400
    
    try:
        task = task_server.assign_task(name, assignee)
        logger.info(f"Task '{name}' assigned to '{assignee}'")
        return jsonify(task)
    except Exception as e:
        logger.error(f"Failed to assign task '{name}': {e}")
        raise


@app.route('/tasks/<name>/comments', methods=['POST'])
def add_task_comment(name):
    """Add a comment to a task."""
    logger.info(f"API: add_task_comment - {name}")
    
    data = request.json
    if not data:
        return jsonify({"error": {"message": "Invalid request format"}}), 400
    
    comment = data.get('comment')
    if not comment:
        return jsonify({"error": {"message": "Comment not provided"}}), 400
    
    try:
        task = task_server.add_task_comment(name, comment)
        logger.info(f"Comment added to task '{name}'")
        return jsonify(task)
    except Exception as e:
        logger.error(f"Failed to add comment to task '{name}': {e}")
        raise


@app.route('/tasks/<name>/comments', methods=['GET'])
def get_task_comments(name):
    """Get all comments for a task."""
    logger.info(f"API: get_task_comments - {name}")
    
    try:
        comments = task_server.get_task_comments(name)
        return jsonify(comments)
    except Exception as e:
        logger.error(f"Failed to get comments for task '{name}': {e}")
        raise


if __name__ == '__main__':
    # Create data directory if it doesn't exist
    os.makedirs(config.data_dir, exist_ok=True)
    
    # Set log level
    log_level = getattr(logging, config.log_level.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    logger.info(f"Starting server on {config.host}:{config.port}")
    app.run(host=config.host, port=config.port, debug=True)
