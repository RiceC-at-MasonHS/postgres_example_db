FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
# Uncomment the next line if using PostgreSQL with psycopg2
# RUN pip3 install --no-cache-dir psycopg2-binary
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set PYTHONPATH to include the app directory
ENV PYTHONPATH=/app:$PYTHONPATH

# Postgres configuration only
ENV DATABASE_URL=postgresql://postgres:postgres@db:5432/learning_map

EXPOSE 5432

CMD ["/bin/bash"]
