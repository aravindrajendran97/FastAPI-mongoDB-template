FROM python:3.8.6-buster
USER root
RUN apt-get update
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
COPY . /app
EXPOSE 8080
CMD ["uvicorn", "app:app",  "--host", "0.0.0.0", "--port", "8080"]
