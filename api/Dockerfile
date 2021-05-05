FROM python:3

WORKDIR /app

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install ffmpeg libsqlite3-mod-spatialite -y

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD [ "flask", "run", "--host", "0.0.0.0", "-p", "5000" ]
