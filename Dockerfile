FROM python:3-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Create directories if they don't exist
RUN mkdir -p /app/characters /app/attachments /app/configurations /app/channels

# Copy initial files
COPY initial_data/characters/* /app/characters/
COPY initial_data/attachments/* /app/attachments/
COPY initial_data/configurations/* /app/configurations/

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD ["python", "bot.py"]
