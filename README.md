# Task Management API

A Flask-based REST API for managing tasks, similar to the Go-based sample project but implemented in Python.

## Features

- Create, read, update, and delete tasks
- Assign tasks to users
- Update task status (pending, in-progress, completed)
- Add comments to tasks
- List all tasks
- Get details for a specific task

## Project Structure

```
.
├── app.py          # Main Flask application with API routes
├── client.py       # Command-line client for interacting with the API
├── config.py       # Configuration loading and management
├── config.yaml     # Configuration file
├── requirements.txt # Python dependencies
├── server.py       # Task server implementation with business logic
```

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the server:

```bash
python app.py
```

The server will start on http://127.0.0.1:8080 by default.

## Using the Client

The `client.py` script provides a command-line interface for interacting with the API:

### Create a task

```bash
python client.py create "Task Name" "Task Description" --priority "high" --due-date "2025-04-01"
```

### List all tasks

```bash
python client.py list
```

### Get a specific task

```bash
python client.py get "Task Name"
```

### Update task status

```bash
python client.py update "Task Name" "completed"
```

### Assign a task

```bash
python client.py assign "Task Name" "John Doe"
```

### Add a comment to a task

```bash
python client.py comment "Task Name" "This is a comment"
```

### Delete a task

```bash
python client.py delete "Task Name"
```

### Delete all tasks

```bash
python client.py delete-all
```

## API Endpoints

- `POST /tasks` - Create a new task
- `GET /tasks` - List all tasks
- `GET /tasks/<name>` - Get a specific task
- `PATCH /tasks/<name>` - Update task status
- `POST /tasks/<name>/assign` - Assign a task
- `POST /tasks/<name>/comments` - Add a comment to a task
- `GET /tasks/<name>/comments` - Get all comments for a task
- `DELETE /tasks/<name>` - Delete a task
- `DELETE /tasks` - Delete all tasks

## Configuration

The server can be configured using the `config.yaml` file. Available options:

- `host` - Server host (default: 127.0.0.1)
- `port` - Server port (default: 8080)
- `log_level` - Logging level (default: info)
- `data_dir` - Directory for data storage (default: ./data)
- `max_concurrent` - Maximum concurrent requests (default: 10)
- `request_timeout` - Request timeout in seconds (default: 30)