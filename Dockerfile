FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy scanner code
COPY realtime_scanner/ ./realtime_scanner/

# Set working directory to scanner
WORKDIR /app/realtime_scanner

# Run the scanner
CMD ["python", "main.py"]
