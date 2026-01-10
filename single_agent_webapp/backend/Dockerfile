# Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy backend code and project dependencies
COPY single_agent_webapp/backend/requirements.txt .
COPY requirements.txt ./project-requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r project-requirements.txt

# Copy the entire project (needed for imports)
COPY . .

# Copy entrypoint script
COPY single_agent_webapp/backend/docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

WORKDIR /app/single_agent_webapp/backend

# Expose port
EXPOSE 8000

# Run the application
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
