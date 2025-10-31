# API Separation: REST vs Tools

This document explains the separation between REST API endpoints (for humans) and Tools API endpoints (for AI agents).

## Architecture Overview

```
app/modules/deadline/
├── rest/                   # Human-friendly REST API
│   ├── __init__.py
│   └── cruds.py           # CRUD operations with filtering, pagination
├── tools/                  # AI-friendly Tools API  
│   ├── __init__.py
│   └── ai_tools.py        # Structured data, bulk operations
├── routers.py             # Combines both APIs
├── service.py             # Shared business logic
└── schemas.py             # Shared data models
```

## REST API (`/api/v1/deadline/rest/`)

**Purpose**: Human users, web interfaces, mobile apps

**Characteristics**:
- User-friendly responses with descriptions
- Pagination and filtering
- Error messages in natural language
- Statistics and summaries for dashboards
- Individual resource access patterns

### Endpoints

```bash
GET /api/v1/deadline/rest/jobs              # List jobs with filtering
GET /api/v1/deadline/rest/jobs/{job_id}     # Get single job details
GET /api/v1/deadline/rest/users             # List all users
GET /api/v1/deadline/rest/status            # Service status with statistics
```

### Example REST Response
```json
{
  "service_available": true,
  "message": "Deadline service is running",
  "statistics": {
    "total_jobs": 5,
    "status_breakdown": {
      "Completed": 2,
      "Rendering": 3
    },
    "user_breakdown": {
      "lynloveyounever": 5
    },
    "active_users": 1
  }
}
```

## Tools API (`/api/v1/deadline/tools/`)

**Purpose**: AI agents, automation systems, integrations

**Characteristics**:
- Structured data optimized for programmatic consumption
- Bulk operations for efficiency
- Machine-readable status indicators
- Analysis and insights for decision making
- Batch processing capabilities

### Endpoints

```bash
POST /api/v1/deadline/tools/query-jobs           # Structured job queries
GET  /api/v1/deadline/tools/job-summary          # Aggregated data summary
GET  /api/v1/deadline/tools/analyze-workload     # Workload analysis
GET  /api/v1/deadline/tools/job-status-check/{id} # Detailed status check
POST /api/v1/deadline/tools/bulk-status-check    # Check multiple jobs
```

### Example Tools Response
```json
{
  "total_jobs": 5,
  "jobs_by_status": {
    "Completed": 2,
    "Rendering": 3
  },
  "jobs_by_user": {
    "lynloveyounever": 5
  },
  "recent_activity": [
    "Job job-001 (Scene_01_Render) is Completed",
    "Job job-002 (Scene_02_Render) is Rendering"
  ]
}
```

## Key Differences

| Aspect | REST API | Tools API |
|--------|----------|-----------|
| **Target Users** | Humans | AI Agents |
| **Response Format** | User-friendly | Machine-optimized |
| **Error Messages** | Natural language | Structured codes |
| **Data Access** | Individual resources | Bulk operations |
| **Filtering** | Query parameters | Structured requests |
| **Analysis** | Basic statistics | Deep insights |

## Usage Examples

### Human User (Web Interface)
```javascript
// Get jobs for dashboard
fetch('/api/v1/deadline/rest/jobs?status=Rendering&limit=10')
  .then(response => response.json())
  .then(jobs => {
    // Display in user interface
    jobs.forEach(job => displayJob(job));
  });

// Get service statistics
fetch('/api/v1/deadline/rest/status')
  .then(response => response.json())
  .then(status => {
    document.getElementById('total-jobs').textContent = 
      status.statistics.total_jobs;
  });
```

### AI Agent (Automation)
```python
import httpx

# Query jobs with structured parameters
query = {
    "status_filter": "Rendering",
    "include_metadata": True
}
response = await client.post("/api/v1/deadline/tools/query-jobs", json=query)
jobs = response.json()

# Analyze workload for decision making
analysis = await client.get("/api/v1/deadline/tools/analyze-workload")
workload_data = analysis.json()

if "resource constraints" in workload_data["bottlenecks"]:
    # Take automated action
    await scale_render_nodes()
```

## Benefits

1. **Optimized User Experience**: Each API is tailored for its intended audience
2. **Performance**: Tools API can use bulk operations, REST API focuses on individual resources
3. **Maintainability**: Clear separation of concerns
4. **Scalability**: Different caching and rate limiting strategies per API type
5. **Security**: Different authentication/authorization rules if needed

## Testing

Run the separation tests:
```bash
pytest tests/test_deadline_separation.py -v
```

This architecture ensures both human users and AI agents get the optimal experience for their specific use cases.