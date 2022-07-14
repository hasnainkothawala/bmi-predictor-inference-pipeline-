FROM ubuntu:18.04
ENV TZ=Europe/Dublin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update
RUN apt-get install -y python3.8 python3-pip python3.8-dev build-essential
RUN apt update && apt install -y libsm6 libxext6
RUN python3.8 -m pip install --upgrade pip

WORKDIR /
COPY requirements.txt /app/requirements.txt
RUN python3.8 -m pip install -r /app/requirements.txt
COPY /app /app

WORKDIR /
ENTRYPOINT ["python3.8", "app/main.py"]