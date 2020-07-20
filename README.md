=======
Share Ride API

## Group-bounded, invite-only, carpooling platform

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

## This project


This that are missing right now:

* [ ] Add tests and coverage implementations
* [ ] Remove weak Token Authorization system
* [ ] Implement more async and periodic tasks to improve the rating system
* [ ] A UI!


## Development



To start working on this project I highly recommend you to check
[pydanny's](https://github.com/pydanny) [Django Cookiecutter](https://github.com/pydanny/cookiecutter-django) [documentation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally-docker.html) on how to get this project up and running locally.
If you don't want to do so, just run:

```bash
docker-compose -f local.yml build
docker-compose -f local.yml up
```

## Want to use this project as yours?

Please stick to the [**LICENSE**](LICENSE), you can read a TL;DR
[here](https://tldrlegal.com/license/mit-license).

Again, this is a project I liked a lot and I will love to see it live
again. Feel free to modify, distribute, use privately, etc (READ THE [**LICENSE**](LICENSE)) as
you please just include the Copyright and the [**LICENSE**](LICENSE).

## Contributors

- [Pablo Trinidad](https://github.com/pablotrinidad)
  | CS Student at UNAM's Faculty of Science | <pablotrinidad@ciencias.unam.mx>
- [Johan suarez Largo](https://github.com/jadry92) | <johan@blognotes.dev>
