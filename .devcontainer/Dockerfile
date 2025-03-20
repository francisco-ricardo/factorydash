FROM python:3.13.2-slim

# Set the working directory inside the container
WORKDIR /factorydash

# Install system dependencies
RUN apt update && apt install -y \
    postgresql-client \
    vim \
    locales \
    supervisor \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Set up locale correctly
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8

# Set some environment variables
ENV LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install python requirements
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy scripts for the container startup
COPY .devcontainer .

# Set default command
ENTRYPOINT ["/factorydash/.devcontainer/docker-entrypoint-dev.sh"]
CMD ["/factorydash/.devcontainer/docker-cmd-script-dev.sh"]

# EOF
