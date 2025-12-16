FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1
# Make the Django project root the working directory so `python manage.py` works
WORKDIR /app/AGHAMazingQuestMobile

# Install system build deps needed for some Python packages (psycopg2, etc.)
RUN apt-get update && \
	apt-get install -y --no-install-recommends \
		build-essential \
		gcc \
		libpq-dev \
	&& rm -rf /var/lib/apt/lists/*

# Copy nested requirements file from the Django project folder
COPY AGHAMazingQuestMobile/requirements.txt ./requirements.txt

# Upgrade pip tools and install Python wheels before installing requirements
RUN pip install --upgrade pip setuptools wheel \
	&& pip install --no-cache-dir -r requirements.txt

# Copy only the Django project files (outer folder contents) into the workdir
COPY AGHAMazingQuestMobile/ .
# Copy the entrypoint into the project dir
COPY docker-entrypoint.sh ./docker-entrypoint.sh
RUN chmod +x ./docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["gunicorn", "AGHAMazingQuestMobile.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
