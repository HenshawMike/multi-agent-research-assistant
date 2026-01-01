# Use Python 3.13.7 slim image
FROM python:3.13.7-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.7.1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
COPY poetry.lock pyproject.toml ./

# Install Python dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the application
COPY . .

# Create necessary directories
RUN mkdir -p uploads

# Set up Streamlit config
RUN mkdir -p /root/.streamlit/
RUN bash -c 'echo -e "[server]\nheadless = true\nport = $PORT\nenableCORS = false\n\n[browser]\nserverAddress = \"0.0.0.0\"\nserverPort = $PORT" > /root/.streamlit/config.toml'

# Make the setup script executable
RUN chmod +x setup.sh

# Expose the port the app runs on
EXPOSE $PORT

# Command to run the application
CMD ["./setup.sh"]
