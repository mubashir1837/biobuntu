# API Reference

Complete API documentation for BioBuntu's REST endpoints.

## Base URL
```
http://localhost:5000/api
```

## Authentication
Currently no authentication required (for development). Add authentication headers for production use.

## Projects

### List Projects
```http
GET /api/projects
```

**Response:**
```json
[
  {
    "name": "myproject",
    "description": "RNA-seq analysis",
    "created": "2024-01-13T10:00:00",
    "status": "created"
  }
]
```

### Create Project
```http
POST /api/projects
Content-Type: application/json

{
  "name": "newproject",
  "description": "New analysis project"
}
```

**Response:**
```json
{
  "status": "success",
  "project_dir": "/home/user/biobuntu/projects/newproject"
}
```

### Get Project
```http
GET /api/projects/{name}
```

**Response:**
```json
{
  "name": "myproject",
  "description": "RNA-seq analysis",
  "created": "2024-01-13T10:00:00",
  "status": "created"
}
```

### Delete Project
```http
DELETE /api/projects/{name}
```

**Response:**
```json
{
  "status": "success"
}
```

## Workflows

### List Workflows
```http
GET /api/workflows
```

**Response:**
```json
[
  {
    "name": "RNA-seq Pipeline",
    "file": "rnaseq.yaml",
    "description": "Complete RNA-seq analysis"
  }
]
```

## Pipelines

### List Pipelines
```http
GET /api/pipelines
```

**Response:**
```json
[
  {
    "name": "RNA-seq Pipeline",
    "file": "rnaseq.yaml",
    "steps": 3
  }
]
```

### Run Pipeline Locally
```http
POST /api/run
Content-Type: application/json

{
  "workflow": "rnaseq.yaml",
  "input_files": ["sample.fastq"],
  "project": "myproject"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Pipeline completed"
}
```

## Remote Execution

### Submit Remote Job
```http
POST /api/remote/run
Content-Type: application/json

{
  "workflow": "rnaseq.yaml",
  "project": "myproject",
  "input_files": ["sample.fastq"],
  "callback_url": "https://myapp.com/webhook"
}
```

**Response:**
```json
{
  "job_id": "abc123",
  "status": "queued",
  "message": "Job submitted for remote execution"
}
```

### Get Job Status
```http
GET /api/remote/status/{job_id}
```

**Response:**
```json
{
  "job_id": "abc123",
  "status": "running",
  "workflow": "rnaseq.yaml",
  "project": "myproject"
}
```

### List Remote Jobs
```http
GET /api/remote/jobs
```

**Response:**
```json
[
  {
    "job_id": "abc123",
    "status": "completed",
    "workflow": "rnaseq.yaml",
    "project": "myproject",
    "result": "success"
  }
]
```

## Downloads

### Download File
```http
GET /api/download/{project}/{path}
```

Downloads the specified file from the project directory.

## System

### Get Status
```http
GET /api/status
```

**Response:**
```json
{
  "status": "online",
  "version": "0.1.0",
  "uptime": "N/A"
}
```

## Error Responses

All endpoints return errors in this format:
```json
{
  "error": "Error message",
  "status": "error"
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad Request
- `404`: Not Found
- `500`: Internal Server Error

## Rate Limiting

No rate limiting implemented (for development). Add rate limiting for production use.

## Versioning

API version is included in the base path. Current version: v1 (implied).

## Examples

### Python Client
```python
import requests

# List projects
projects = requests.get('http://localhost:5000/api/projects').json()

# Create project
new_project = {
    'name': 'analysis1',
    'description': 'RNA-seq analysis'
}
response = requests.post('http://localhost:5000/api/projects', json=new_project)

# Run pipeline
job = {
    'workflow': 'rnaseq.yaml',
    'project': 'analysis1',
    'input_files': ['sample.fastq']
}
result = requests.post('http://localhost:5000/api/run', json=job)
```

### JavaScript Client
```javascript
// Fetch projects
fetch('/api/projects')
    .then(response => response.json())
    .then(projects => console.log(projects));

// Submit remote job
fetch('/api/remote/run', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        workflow: 'rnaseq.yaml',
        project: 'myproject',
        input_files: ['sample.fastq']
    })
})
.then(response => response.json())
.then(result => console.log('Job ID:', result.job_id));
```