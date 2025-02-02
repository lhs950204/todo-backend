docker pull lhs950204/todo
docker rm -f todo

docker run -itd\
 --name todo\
 -p 8000:8000\
 -e SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7\
 -e DB_URI=sqlite:///./db/db.db\
 -e MEDIA_ROOT=/media\
 -v $(pwd)/s3-buckets/media:/media\
 -v $(pwd)/db:/db\
 lhs950204/todo