# Use Python 3.11 base image along with a small Debian buster OS image
FROM python:3.11-slim 

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of application code
COPY . .

# Expose the application port
EXPOSE 8000

# Command to start FastAPI application
# this host is the IP address of the host machine which is important for Docker networking 
# to accept request from any IP address
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

