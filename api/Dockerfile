FROM python:3.9

WORKDIR /app

RUN apt-get update && \
	apt-get install -y ffmpeg libsqlite3-mod-spatialite

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "flask", "run", "--no-reload", "--host", "0.0.0.0", "-p", "5000" ]
