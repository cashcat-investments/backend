docker build -t stocks-service .
docker run -it --env-file .env -p 8000:8000 stocks-service