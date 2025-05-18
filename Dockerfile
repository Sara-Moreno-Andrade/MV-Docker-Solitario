FROM python:3.10-slim

RUN apt-get update && apt-get install -y tk

COPY . /app
WORKDIR /app

CMD ["python", "solitario/solitario.py"]
