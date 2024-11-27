# Use the official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy dependencies file and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the application port (if needed, e.g., Flask)
EXPOSE 5000

# Set the command to run the app
CMD ["python", "main.py"]
