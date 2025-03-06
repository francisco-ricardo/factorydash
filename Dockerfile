# Use Python official image
FROM python:latest

# Set the working directory inside the container
WORKDIR /factorydash

# Install system dependencies
RUN apt update && apt install -y \
    curl \
    postgresql-client \
    locales \
    && rm -rf /var/lib/apt/lists/*

# Set up locale correctly
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8

# Set environment variables
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

# Copy project
COPY . /factorydash/

# Ensure logs directory exists
RUN mkdir -p /factorydash/app/factorydash/logs

# Install Django dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /factorydash/requirements.txt

# Run the Django development server
CMD ["python", "/factorydash/app/factorydash/manage.py", "runserver", "0.0.0.0:8000"]
