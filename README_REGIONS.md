# Geographic Distribution Architecture

This document explains the geographic distribution setup for the CGCG API.

## Overview

The API now supports geographic distribution across multiple regions:
- **US East** (`us-east`) - Primary region with full features
- **EU West** (`eu-west`) - GDPR-compliant region with selective features  
- **Asia Pacific** (`asia-pacific`) - Localized region with Japanese language support

## Architecture

### Region Resolution
Requests are automatically routed to appropriate regions using:

1. **X-Region Header**: `X-Region: eu-west`
2. **Subdomain**: `eu-west.api.example.com`
3. **Path Prefix**: `/api/v1/regions/eu-west/...`
4. **IP Geolocation**: Automatic detection (simplified implementation)
5. **Default Fallback**: `us-east`

### Regional Configuration

Each region has its own:
- Database connections
- External API endpoints
- Feature flags
- Performance settings
- Compliance requirements

### Regional Services

Each region provides:
- Deadline API integration
- Media Shuttle synchronization
- Notification services
- Region-specific business logic

## Usage Examples

### Basic Region Detection
```bash
# Default region (us-east)
curl http://localhost:8000/api/v1/regions/current

# Specific region via header
curl -H "X-Region: eu-west" http://localhost:8000/api/v1/regions/current
```

### Region-Aware Deadline Jobs
```bash
# Get jobs from current region
curl http://localhost:8000/api/v1/deadline/jobs

# Get jobs from EU West region
curl -H "X-Region: eu-west" http://localhost:8000/api/v1/deadline/jobs

# Cross-region access (requires advanced_analytics feature)
curl -H "X-Region: us-east" http://localhost:8000/api/v1/deadline/jobs/region/eu-west
```

### Feature-Based Access Control
```bash
# Check region features
curl http://localhost:8000/api/v1/regions/us-east/config

# This will fail if region doesn't have required feature
curl -H "X-Region: eu-west" http://localhost:8000/api/v1/deadline/jobs/region/us-east
```

## Configuration

### Environment Variables
```bash
# Global settings
DEFAULT_REGION=us-east
MULTI_REGION_ENABLED=true
REGION_OVERRIDE=us-east  # Force specific region for testing

# Region-specific database URLs
US_EAST_DATABASE_URL=postgresql://...
EU_WEST_DATABASE_URL=postgresql://...
APAC_DATABASE_URL=postgresql://...
```

### Regional Features

| Feature | US East | EU West | Asia Pacific |
|---------|---------|---------|--------------|
| Advanced Analytics | ✅ | ❌ | ❌ |
| Real-time Sync | ✅ | ❌ | ✅ |
| Beta Features | ✅ | ❌ | ❌ |
| GDPR Compliance | ❌ | ✅ | ❌ |

## Development

### Adding New Regions
1. Create region directory: `app/regions/new_region/`
2. Add config: `config.py` with region-specific settings
3. Add services: `services.py` with region-specific integrations
4. Update resolver: Add region to `RegionResolver.regions`

### Testing Regions
```bash
# Run region-specific tests
pytest tests/test_regions.py

# Test with specific region
X_REGION=eu-west pytest tests/test_regions.py::test_deadline_jobs_specific_region
```

### Deployment Considerations

1. **Database Isolation**: Each region should have its own database
2. **Service Discovery**: External APIs should be region-specific
3. **Monitoring**: Track performance per region
4. **Compliance**: Ensure data residency requirements are met

## Response Headers

All responses include regional context:
```
X-Region: us-east
X-Region-Name: US East
X-Timezone: America/New_York
```

This architecture provides scalable geographic distribution while maintaining code organization and feature flexibility per region.