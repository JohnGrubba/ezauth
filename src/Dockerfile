FROM python:3.12-slim

WORKDIR /src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /src/app/requirements.txt
RUN apt update
RUN apt install git -y
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /src/app/requirements.txt

COPY . /src/app

RUN chmod +x /src/app/start.sh

CMD ["/src/app/start.sh"]
