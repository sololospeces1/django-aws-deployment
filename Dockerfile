FROM python:3.10.11-alpine

ENV PYTHONUNBUFFERED 1

RUN mkdir /blog_microservice

WORKDIR /blog_microservice

COPY . .
COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8000


# CMD ["python3", "manage.py", "runserver", "8000"]
CMD ["gunicorn", "digital_magazine.wsgi:application", \
     "--bind", "0.0.0.0:8000", "--workers", \
     "3", "--timeout", "300"]
