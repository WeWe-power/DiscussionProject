# Demo project 

____
*Practicing celery, docker, restframework*

*Description*: Forum-like project for discussions;

+ *How to run*: 
  + rename .env.example and .env.dev.example to .env and .env.db, also setting your own parametrs there
  + docker-compose up -d --build
  + docker-compose up

+ *Urls*:
  + localhost:1337 - website
  + localhost:1337/admin - admin
  + localhost:8888 - flower
  + localhost:5050 - pgadmin
  + localhost:1337/api/docs/swagger/ - API docs

* *How to connect postgres*:
   1. Get pgdb container id with docker ps -a
   2. Get pgdb ip: docker inspect  'pgdb_id' | grep "IPAddress"
   3. Enter pgadmin page  
   4. Press create a server on pgadmin page and enter data
