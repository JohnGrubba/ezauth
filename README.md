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

1) Clone EZAuth Repository (`git clone https://github.com/JohnGrubba/ezauth`)
2) `cd ezauth`
3) `cp config/configtemplate.json config/config.json`
4) Edit Configuration under (`config/config.json`) [Config Documentation](https://johngrubba.github.io/ezauth/configuration/configuration/)
5) `mkdir config/email && cp config/emailtemplate/* config/email/`
6) Edit E-Mails under (`config/email/*`)
7) Start EZAuth

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
