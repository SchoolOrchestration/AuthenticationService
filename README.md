# Authentication Service

Service for authenticating users against our user store and getting a token from Kong


# Getting started

## Run locally:

```
docker-compose up -d
```

It's running on localhost:8000

## Run tests:

```
docker-compose run --rm web pytest .
```

## Deploy

```
sh ./deploy.sh
```

## Profit

![profit](https://i.ytimg.com/vi/tO5sxLapAts/hqdefault.jpg)

# Spec:

- [x] `GET   /health/    # health endpoint`
- [ ] `GET   /auth/      # get a login form`
- [ ] `POST  /auth/      # post a username and password, get a token back`
- [ ] `GET   /register   # get a form for registering an app`
- [ ] `POST  /register   # create a client app`

