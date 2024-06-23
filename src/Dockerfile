FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /src/app

COPY ./requirements.txt /src/app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /src/app/requirements.txt

COPY . /src/app

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80", "--log-level", "info"]
