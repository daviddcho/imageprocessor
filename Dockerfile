FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3.9 python3-pip
COPY . .
RUN pip install -r requirements.txt
ENV FLASK_DEBUG=1
ENV FLASK_ENV=development
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
