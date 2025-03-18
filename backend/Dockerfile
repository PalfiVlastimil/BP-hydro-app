# Use a minimal and secure base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install dependencies
RUN python -m venv venv --system-site-packages


# Install system dependencies and security updates
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# install nano for file editing
RUN apt-get update && apt-get install -y nano
RUN apt-get update && apt-get install -y i2c-tools
# Copy dependencies first (better caching)
COPY requirements.txt .

# Install dependencies in the virtual environment
#--no-cache-dir
RUN pip3 install --no-cache-dir -r requirements.txt
# Use curl to download the installation script and run it (for example, for grove.py)
# Copy the application code
COPY . .

# Expose the API port
EXPOSE 5000

# Use Gunicorn as the WSGI server for Flask
CMD ["gunicorn", "-w", "4", "--preload" , "-b", "0.0.0.0:5000", "app:app"]