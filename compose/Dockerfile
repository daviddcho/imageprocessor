FROM ubuntu:20.04
WORKDIR /app

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3.9 python3-pip
COPY app/ /app/
RUN pip install -r /app/requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
