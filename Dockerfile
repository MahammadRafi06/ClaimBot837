# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy dependencies file and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

ENV PYTHONPATH=/app

# Expose the application port (if needed, e.g., Flask)
EXPOSE 5000

LABEL maintainer="NeuroClaim Team" \
      version="1.0.0" \
      description="NeuroClaim - Intelligent Healthcare Claims Processing"

# Set the command to run the app
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
