pip freeze > requirements.txt 
docker-compose up --build
docker-compose exec backend sh -c ''
docker exec -it backend /bin/bash