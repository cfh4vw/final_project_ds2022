FROM python:3.10-slim

# Create app directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src
COPY assets/ ./assets

EXPOSE 5000

# Run the app
CMD ["python", "src/app.py"]

