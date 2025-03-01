# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN apt-get update && apt-get install -y build-essential
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Create directories if they don't exist
RUN mkdir -p /app/characters /app/attachments /app/configurations /app/channels

# Copy initial files
COPY initial_data/characters/* /app/characters/
COPY initial_data/attachments/* /app/attachments/
COPY initial_data/configurations/* /app/configurations/

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "bot.py"]
