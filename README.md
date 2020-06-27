Share Ride API
=============

Group-bounded, invite-only, carpooling platform

### Basic commands

Run docker image
```shell script
docker-compose -f local.yml up
```
 
Stop Django process
```shell script
docker kill $id_django
```

Run django image only 
```shell script
docker-compose -f local.yml run --rm --service-ports django
```

Run manage.py command
```shell script
docker-compose -f local.yml run --rm django python manage.py $command
```

Delete DB volumes
```shell script
docker volume rm cride-platzi_local_postgres_data
```
