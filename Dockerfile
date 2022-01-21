FROM nginx:stable
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3.9 python3-pip
COPY app/ .
RUN pip install -r requirements.txt
COPY default.conf /etc/nginx/conf.d/
CMD ["gunicorn", "-b", "127.0.0.1:5000", "app:app"]
