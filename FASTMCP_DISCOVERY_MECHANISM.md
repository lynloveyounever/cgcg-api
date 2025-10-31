# How FastMCP Discovers Tools, Resources, and Prompts

## FastMCP Discovery Logic

FastMCP analyzes your FastAPI application and automatically categorizes endpoints based on their characteristics:

### 1. **Tools** (Function Calls)
FastMCP converts endpoints to **tools** when they:
- Have **GET/POST** methods
- Accept **parameters** (path, query, body)
- Return **structured data** (JSON)
- Are **action-oriented** (verbs like get, check, create, update)

### 2. **Resources** (Data Access)
FastMCP converts endpoints to **resources** when they:
- Are **GET** methods only
- Return **static or semi-static data**
- Have **resource-like URLs** (nouns like `/users`, `/files`)
- Provide **read-only access** to data

### 3. **Prompts** (Templates)
FastMCP converts endpoints to **prompts** when they:
- Return **text/string content**
- Have **template-like behavior**
- Accept **parameters for customization**
- Generate **human-readable output**

## Your Deadline Tools Analysis

Let's analyze how FastMCP categorizes your endpoints:

### ✅ **Classified as TOOLS** (All your endpoints)

```python
# 1. GET with parameters → TOOL
@tools_router.get("/get_jobs_by_status/{status}")
async def get_jobs_by_status(status: str):
    # Action: "get jobs by status"
    # Parameter: status
    # Returns: structured data (List[DeadlineJobInfo])
    # → TOOL: get_jobs_by_status

# 2. GET with path parameter → TOOL  
@tools_router.get("/check_job_status/{job_id}")
async def check_job_status(job_id: str):
    # Action: "check status"
    # Parameter: job_id
    # Returns: structured data (JobStatusResult)
    # → TOOL: check_job_status

# 3. GET returning structured data → TOOL
@tools_router.get("/get_workload_summary")
async def get_workload_summary():
    # Action: "get summary"
    # Returns: structured data (WorkloadSummary)
    # → TOOL: get_workload_summary
```

## FastMCP Classification Rules

### Tools Classification
```python
# These become TOOLS:
GET  /api/v1/deadline/tools/get_all_jobs           → get_all_jobs
GET  /api/v1/deadline/tools/check_job_status/{id}  → check_job_status  
POST /api/v1/deadline/tools/query_jobs             → query_jobs
PUT  /api/v1/deadline/tools/update_job/{id}        → update_job
```

### Resources Classification  
```python
# These would become RESOURCES:
GET  /api/v1/deadline/jobs                         → deadline_jobs
GET  /api/v1/deadline/users                        → deadline_users
GET  /api/v1/deadline/config                       → deadline_config
```

### Prompts Classification
```python
# These would become PROMPTS:
GET  /api/v1/deadline/report/{job_id}              → job_report_template
GET  /api/v1/deadline/summary_text                 → workload_summary_text
POST /api/v1/deadline/generate_report              → generate_report_prompt
```

## How FastMCP Reads Your Endpoints

### 1. **Function Name** → Tool Name
```python
async def get_all_jobs():  # → Tool: "get_all_jobs"
async def check_job_status():  # → Tool: "check_job_status"
```

### 2. **Docstring** → Tool Description
```python
async def get_all_jobs():
    """
    Get all deadline jobs.
    
    Returns a list of all jobs in the system with basic information.
    Use this function to get an overview of all current jobs.
    """
    # FastMCP uses this docstring as tool description
```

### 3. **Parameters** → Tool Input Schema
```python
async def get_jobs_by_status(status: str):
    # FastMCP creates input schema:
    # {
    #   "type": "object",
    #   "properties": {
    #     "status": {"type": "string"}
    #   },
    #   "required": ["status"]
    # }
```

### 4. **Response Model** → Tool Output Schema
```python
@tools_router.get("/get_all_jobs", response_model=List[DeadlineJobInfo])
async def get_all_jobs():
    # FastMCP creates output schema from DeadlineJobInfo model
```

## Configuration Control

### Include Only Specific Tags
```python
mcp = FastApiMCP(
    app,
    include_tags=["Deadline AI Tools"]  # Only these become tools
)
```

### Include Only Specific Operations
```python
mcp = FastApiMCP(
    app,
    include_operations=[
        "get_all_jobs",      # This becomes a tool
        "check_job_status"   # This becomes a tool
    ]
    # Everything else is ignored
)
```

### Exclude Specific Operations
```python
mcp = FastApiMCP(
    app,
    include_tags=["Deadline AI Tools"],
    exclude_operations=[
        "internal_debug_endpoint"  # This won't become a tool
    ]
)
```

## Why Your Endpoints Become Tools

All your deadline endpoints become **tools** because they:

1. **Have Action Names**: `get_all_jobs`, `check_job_status`, `get_workload_summary`
2. **Accept Parameters**: `status`, `job_id`, `username`
3. **Return Structured Data**: Pydantic models with clear schemas
4. **Are Function-Like**: They perform actions and return results
5. **Have Clear Descriptions**: Docstrings explain what they do

## Example: What Would Be Resources

If you had these endpoints, they'd become **resources**:

```python
# These would be RESOURCES (data access):
@app.get("/api/v1/deadline/jobs")           # Resource: all jobs data
@app.get("/api/v1/deadline/users")          # Resource: all users data  
@app.get("/api/v1/deadline/config")         # Resource: configuration data

# These are TOOLS (actions):
@app.get("/api/v1/deadline/tools/get_jobs") # Tool: action to get jobs
@app.post("/api/v1/deadline/tools/create")  # Tool: action to create
```

## Example: What Would Be Prompts

If you had these endpoints, they'd become **prompts**:

```python
# These would be PROMPTS (text generation):
@app.get("/api/v1/deadline/report/{job_id}")
async def generate_job_report(job_id: str) -> str:
    return f"Job {job_id} report: ..."  # Returns text → PROMPT

@app.post("/api/v1/deadline/summary")  
async def generate_summary(template: str) -> str:
    return f"Summary: {template}..."  # Text template → PROMPT
```

## Summary

FastMCP automatically determines the MCP type based on:

- **Tools**: Action-oriented endpoints with parameters and structured responses
- **Resources**: Data-oriented endpoints that provide read access to information  
- **Prompts**: Text-oriented endpoints that generate human-readable content

Your deadline endpoints are perfectly designed as **tools** because they perform actions and return structured data that AI agents can use for decision-making!