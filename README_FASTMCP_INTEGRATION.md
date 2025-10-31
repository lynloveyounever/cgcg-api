# FastMCP Integration with Deadline Tools

## How It Works

FastMCP automatically discovers your FastAPI endpoints and exposes them as MCP tools. No decorators needed - it uses the existing FastAPI route information!

## Configuration

### main.py Setup
```python
from fastapi_mcp import FastApiMCP

mcp = FastApiMCP(
    app,
    include_tags=["Deadline AI Tools"]  # Only include AI tools endpoints in MCP
)
mcp.mount()  # Creates MCP server at /mcp
```

### What Gets Exposed

All endpoints with the tag `"Deadline AI Tools"` become MCP tools:

| HTTP Endpoint | MCP Tool Name | Description |
|---------------|---------------|-------------|
| `GET /api/v1/deadline/tools/get_all_jobs` | `get_all_jobs` | Get all deadline jobs |
| `GET /api/v1/deadline/tools/check_job_status/{job_id}` | `check_job_status` | Check specific job status |
| `GET /api/v1/deadline/tools/get_workload_summary` | `get_workload_summary` | Get workload summary |
| `GET /api/v1/deadline/tools/get_failed_jobs` | `get_failed_jobs` | Get failed jobs |
| `GET /api/v1/deadline/tools/get_running_jobs` | `get_running_jobs` | Get running jobs |
| `GET /api/v1/deadline/tools/count_jobs_by_status` | `count_jobs_by_status` | Count jobs by status |
| `GET /api/v1/deadline/tools/list_active_users` | `list_active_users` | List active users |
| `GET /api/v1/deadline/tools/is_system_busy` | `is_system_busy` | Check system load |
| `GET /api/v1/deadline/tools/get_jobs_by_status/{status}` | `get_jobs_by_status` | Get jobs by status |
| `GET /api/v1/deadline/tools/get_jobs_by_user/{username}` | `get_jobs_by_user` | Get jobs by user |

## Dual Protocol Access

### HTTP Access (Testing & Direct Integration)
```bash
# Test endpoints directly
curl http://localhost:8000/api/v1/deadline/tools/get_all_jobs
curl http://localhost:8000/api/v1/deadline/tools/get_workload_summary
curl http://localhost:8000/api/v1/deadline/tools/check_job_status/job-001
```

### MCP Access (AI Agents)
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

Response:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "get_all_jobs",
        "description": "Get all deadline jobs.",
        "inputSchema": {
          "type": "object",
          "properties": {}
        }
      },
      {
        "name": "check_job_status",
        "description": "Check the status of a specific job.",
        "inputSchema": {
          "type": "object",
          "properties": {
            "job_id": {
              "type": "string",
              "description": "The unique identifier of the job to check"
            }
          },
          "required": ["job_id"]
        }
      }
    ]
  }
}
```

## Benefits

### ✅ **Automatic Discovery**
- No manual tool registration needed
- FastMCP reads FastAPI route metadata
- Pydantic models become MCP schemas automatically

### ✅ **Zero Code Changes**
- Your existing functions work as-is
- No decorators or modifications needed
- Same business logic serves both protocols

### ✅ **Type Safety**
- Pydantic models provide schema validation
- FastAPI type hints become MCP parameter types
- Automatic request/response validation

### ✅ **Easy Configuration**
- Filter by tags: `include_tags=["Deadline AI Tools"]`
- Filter by operations: `include_operations=["get_all_jobs"]`
- Exclude endpoints: `exclude_tags=["Internal"]`

## Advanced Configuration Options

### Include Specific Operations
```python
mcp = FastApiMCP(
    app,
    include_operations=[
        "get_all_jobs",
        "check_job_status", 
        "get_workload_summary"
    ]
)
```

### Exclude Internal Endpoints
```python
mcp = FastApiMCP(
    app,
    include_tags=["Deadline AI Tools"],
    exclude_operations=["internal_debug_endpoint"]
)
```

### Enhanced Descriptions
```python
mcp = FastApiMCP(
    app,
    include_tags=["Deadline AI Tools"],
    describe_all_responses=True,  # Include response schemas
    describe_full_response_schema=True  # Full JSON schema details
)
```

## Testing MCP Integration

### 1. Start the Server
```bash
uvicorn main:app --reload
```

### 2. Check MCP Endpoint
```bash
# MCP server is available at:
http://localhost:8000/mcp
```

### 3. Test Tool Discovery
Use an MCP client to connect to `http://localhost:8000/mcp` and list available tools.

### 4. Test HTTP Endpoints
```bash
# These still work for direct testing:
curl http://localhost:8000/api/v1/deadline/tools/get_all_jobs
curl http://localhost:8000/api/v1/deadline/tools/get_workload_summary
```

## AI Agent Integration

### Claude Desktop
```json
{
  "mcpServers": {
    "cgcg-deadline": {
      "command": "curl",
      "args": ["-X", "POST", "http://localhost:8000/mcp"]
    }
  }
}
```

### OpenAI Compatible
Your tools are now accessible via MCP protocol to any MCP-compatible AI system.

## Result

You now have:
- **HTTP endpoints** for testing and direct integration
- **MCP tools** for AI agents
- **Same functions** serving both protocols
- **Automatic discovery** with no code changes
- **Type-safe** parameter validation

This gives you the best of both worlds: easy testing via HTTP and AI agent compatibility via MCP!