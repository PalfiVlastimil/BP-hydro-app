# Use a minimal and secure base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install dependencies
RUN python -m venv venv 

# Activate virtual environment and set the PATH
ENV PATH="/app/venv/bin:$PATH"

# Install system dependencies and security updates
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies first (better caching)
COPY requirements.txt .

# Install dependencies in the virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port (optional since Docker Compose handles networking)
EXPOSE 5001

# Use Gunicorn as the WSGI server
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "app:app"]