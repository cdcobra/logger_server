docker rm -f logger

docker build -t logger .

docker run -d \
 --restart always \
 --name logger \
 -p 8000:8000 \
 --env-file .env \
 --network analizy \
 --log-driver json-file \
 --log-opt max-size=100m \
 --log-opt max-file=2 \
 logger