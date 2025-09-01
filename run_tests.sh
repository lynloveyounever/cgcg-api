#!/bin/bash
# This script runs the pytest tests with the correct Python path.
echo "Running tests..."
PYTHONPATH=. pytest
