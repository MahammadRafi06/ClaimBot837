# Use the official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy dependencies file and install
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app .

# Expose the application port (if needed, e.g., Flask)
EXPOSE 5000

# Set the command to run the app
CMD ["python", "app.py", "--host=0.0.0.0", "--port=5000"]
