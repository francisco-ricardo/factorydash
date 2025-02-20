# Use Python official image
FROM python:latest

# Set the working directory inside the container
WORKDIR /workspace

# Install system dependencies
RUN apt update && apt install -y \
    git \
    curl \
    openssh-client \
    postgresql-client \
    vim \
    locales \
    && rm -rf /var/lib/apt/lists/*

# Set up locale correctly
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8

# Set environment variables for locale
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

# Copy requirements.txt from the root of the project
COPY requirements.txt /workspace/requirements.txt

# Install Django dependencies
RUN pip install --no-cache-dir -r /workspace/requirements.txt

# Expose Django's default port
EXPOSE 8000

# Set default command
ENTRYPOINT ["/workspace/docker-entrypoint-dev.sh"]
CMD ["/workspace/docker-cmd-script-dev.sh"]

# EOF
