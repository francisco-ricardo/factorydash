# Use Python official image
FROM python:latest

# Set the working directory inside the container
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y curl

# Copy requirements.txt from the root of the project
COPY requirements.txt /workspace/requirements.txt

# Install Django dependencies
RUN pip install --no-cache-dir -r /workspace/requirements.txt

# Expose Django's default port
EXPOSE 8000

# Set default command
CMD ["bash"]

