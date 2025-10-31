#!/usr/bin/env python3

# Test script to find the correct MCP decorators
from mcp.server.fastmcp import FastMCP

# Create FastMCP instance
mcp = FastMCP("test-server")

# Check available methods
print("FastMCP methods:")
methods = [method for method in dir(mcp) if not method.startswith('_')]
for method in methods:
    print(f"  {method}")

# Check if there are decorators
print("\nLooking for decorators...")
try:
    # Try to find tool decorator
    if hasattr(mcp, 'tool'):
        print("Found: mcp.tool")
    if hasattr(mcp, 'resource'):
        print("Found: mcp.resource") 
    if hasattr(mcp, 'prompt'):
        print("Found: mcp.prompt")
        
    # Check for decorator methods
    for attr in dir(mcp):
        if 'tool' in attr.lower() or 'resource' in attr.lower() or 'prompt' in attr.lower():
            print(f"Found attribute: {attr}")
            
except Exception as e:
    print(f"Error: {e}")