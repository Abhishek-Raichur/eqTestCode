# Build stage
FROM python:3.11-slim as builder
WORKDIR /app

# Update system packages to fix system-level vulnerabilities
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install and upgrade pip to latest version
RUN pip install --no-cache-dir -U pip

COPY requirements.txt .
# Install dependencies with version pinning for security
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir Werkzeug>=3.0.6 requests>=2.32.4

# Final stage - minimal layers with security focus
FROM python:3.11-slim

# Update system packages in final stage too
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user with specific UID/GID
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /usr/sbin/nologin -M appuser && \
    mkdir -p /app /usr/local/lib/python3.11/site-packages/ && \
    chown -R appuser:appgroup /app /usr/local/lib/python3.11/site-packages/

# Set working directory and ownership
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY app.py .

# Set proper permissions
RUN chown -R appuser:appgroup /app && \
    chmod -R 755 /app && \
    chmod 644 /app/app.py

# Switch to non-root user
USER appuser:appgroup

# Security best practices
EXPOSE 8080
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Prevent running as root
RUN if [ "$(id -u)" = "0" ]; then \
    echo "Container should not run as root" && exit 1; \
    fi

CMD ["python", "app.py"]
