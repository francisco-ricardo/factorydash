# Use Python official image
FROM python:3.13.2-slim

# Set the working directory inside the container
WORKDIR /factorydash

# Install system dependencies
RUN apt update && apt install -y \
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
ENV PYTHONPATH /factorydash/app/factorydash
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Django dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create log directory
RUN mkdir -p /factorydash/app/factorydash/logs

# Run the Django development server
CMD ["python", "/factorydash/app/factorydash/manage.py", "runserver", "0.0.0.0:8000"]

# Health check example (adjust as needed)
#HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    #CMD curl -f http://0.0.0.0:8000/ || exit 1