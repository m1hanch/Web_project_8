FROM python:3.11-slim-bullseye
RUN apt update
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
RUN chmod +x run.sh
CMD ["python", "personal_assistant/manage.py", "runserver", "0.0.0.0:8000"]
