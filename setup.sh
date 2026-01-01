#!/bin/bash
set -e

# Install Python dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p uploads

# Set permissions
chmod +x app.py

# Create a default .streamlit/config.toml if it doesn't exist
mkdir -p .streamlit
echo "[server]" > .streamlit/config.toml
echo "headless = true" >> .streamlit/config.toml
echo "enableCORS = false" >> .streamlit/config.toml
echo "port = $PORT" >> .streamlit/config.toml
