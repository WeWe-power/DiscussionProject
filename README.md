# Demo project 

____
*Practicing celery, docker, restframework*

*Description*: Forum-like project for discussions;

*How to run*: First docker-compose up -d --build, then docker-compose up

+ *Urls*:
  + localhost:1337 - website
  + localhost:1337/admin - admin
  + localhost:8888 - flower
  + localhost:5050 - pgadmin

* *How to connect postgres*:
   1. Get pgdb container id with docker ps -a
   2. Get pgdb ip: docker inspect  'pgdb_iid' | grep "IPAddress"
   3. Enter pgadmin page  
   4. Press create a server on pgadmin page and enter data
