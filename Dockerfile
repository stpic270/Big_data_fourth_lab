FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /app

COPY . /app

EXPOSE 70

RUN pip install -r requirements.txt

CMD ["python", "inference.py", "-m", "SVM"]