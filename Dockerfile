FROM python:3.13.2-slim

WORKDIR /factorydash

# Install dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    locales \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Set up locale
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8

ENV LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /factorydash/app/factorydash/logs && \
    python app/factorydash/manage.py collectstatic --noinput

EXPOSE 8000

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["sh", "-c", "python app/factorydash/manage.py migrate && supervisord -c /etc/supervisor/conf.d/supervisord.conf"]


# EOF
