FROM python:3.9

WORKDIR /app

COPY ./src/main.py /app/src

COPY ./model /app/model

COPY requirements.txt /app

RUN pip3 install -r requirements.txt

CMD ["uvicorn", "src.main:app", "--host=0.0.0.0"]