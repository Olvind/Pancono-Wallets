# Base image
FROM python:3.10-slim

# Install dependencies
RUN pip install python-telegram-bot==13.15 requests

# Copy repo
WORKDIR /app
COPY . .

# Default command (overridden by compose)
CMD ["python", "rpc_server.py"]
