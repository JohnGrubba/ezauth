<img src="docs/ezauth_banner.png" />

<h3 align="center">High performance self-hosted and fully customizable authentication service</h3>

![Last Updated](https://raw.githubusercontent.com/JohnGrubba/ezauth/badges/updated.svg)
![Lines of Code](https://raw.githubusercontent.com/JohnGrubba/ezauth/badges/lines.svg)
![Total Files](https://raw.githubusercontent.com/JohnGrubba/ezauth/badges/files.svg)

## Disclaimer

- ⚠️ The project is under **very active** development.
- ⚠️ Expect bugs and breaking changes.
- ⚠️ Make sure to always have a backup of your user data.

> [!NOTE]
> You can find the Documentation <a href="https://johngrubba.github.io/ezauth/" target="_blank">here</a>

## Quickstart

To test a Demo Setup of EZAuth quickly, go into the <a href="demo/">`demo`</a> folder and run the following command:

```sh
docker-compose up -d
```

## Developement

To enable a efficient development process, you can start the Service with hot reloading enabled. This will automatically restart the service when a file is changed.

```sh
docker compose -f .\docker-compose.dev.yml up -d --build
```

## Testing

To be able to perform tests, that represent a real environment, the following technologies are used:
- [MongoMock](https://github.com/JohnGrubba/mongomock)
- [FakeRedis](https://github.com/cunla/fakeredis-py)

Those Libraries automatically get used instead of `pymongo` and `redis` when testing, to avoid the need of an additional Redis and MongoDB instance.

To run the tests, you can use the following command:

```sh
docker exec ezauth-api pytest
```
