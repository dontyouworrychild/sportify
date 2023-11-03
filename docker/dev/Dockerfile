# Pull official base image 
FROM python:3.10-slim

# Set working directory
WORKDIR /stats

# Set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y libpq-dev gcc \
    && pip install Pillow


# Install dependencies
COPY ./stats/requirements ./requirements
RUN pip install --user --upgrade pip
RUN pip install --user -r ./requirements/dev.txt

# Copy entrypoint.sh
COPY ./docker/dev/entrypoint.sh /entrypoint.sh

# RUN chmod +x /entrypoint.sh

COPY ./stats /stats

# ENTRYPOINT ["/entrypoint.sh" ]