FROM nginx:stable
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3.9 python3-pip
COPY app/ .
RUN pip install -r requirements.txt
COPY default.conf /etc/nginx/conf.d/
ENV FLASK_DEBUG=1
ENV FLASK_ENV=development
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
