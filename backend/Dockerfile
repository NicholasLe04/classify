FROM python:3.10.2-slim-buster

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./ /app

WORKDIR /app

EXPOSE 6969

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6969"]