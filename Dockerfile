# Base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libpq-dev \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copy only the dependency files for efficient layer caching
COPY pyproject.toml poetry.lock /app/

# Install project dependencies
RUN poetry install --no-root --no-interaction --no-ansi --without dev

# Copy project files
COPY . /app/ would be nice, but I don't want to copy the working directory arbitrarily

# Generate static files, which aren't currently source-controlled
RUN poetry run python ./manage.py collectstatic

# Run the application
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

