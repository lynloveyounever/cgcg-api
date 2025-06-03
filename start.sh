#!/bin/bash

script_dir=$(dirname "$0")
echo "The directory of this script is: $script_dir"

# Change to the project directory if necessary
cd $script_dir

# Activate the virtual environment if you are using one
source $script_dir/.venv/bin/activate

# Start the FastAPI application with Uvicorn
uvicorn main:app --reload