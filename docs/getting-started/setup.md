# Setup / Installation

## Install Docker and Docker Compose

To install and use EZAuth you need to have Docker and Docker Compose installed on your system. If you don't have Docker and Docker Compose installed you can follow the official installation guides for [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).

!!! Info "Docker compose install"
    EZAuth documentation assumes the use of Docker desktop (or the docker compose plugin).  
    While the docker-compose standalone installation still works, it will require changing all `docker compose` commands from `docker compose` to `docker-compose` to work (e.g. `docker compose up -d` will become `docker-compose up -d`).

!!! Warning "Docker on windows"
    If you just installed docker on a windows system, make sure to reboot your system, otherwise you might encounter unexplainable Problems related to network connectivity to docker containers.

## EZAuth Docker Setup

To install EZAuth you need to clone the repository and perform an initial 
configuration. You can do this by running the following commands:


``` bash
# Clone the repository
git clone https://github.com/JohnGrubba/ezauth
cd ezauth
cp config/configtemplate.json config/config.json
```

Then you need to edit the `config/config.json` file to your needs.
For an explanation of the configuration options, see the [Configuration](../configuration/configuration.md) page.

### Running the service
!!! Warning "Configure the Service first"
    Before you can run the service you need to [configure](../configuration/configuration.md) it.

After you have configured the service you can start it by running the following command:

``` bash
docker compose up -d
```
The service should now be running and you can access the API by navigating to <a href="http://localhost:3250">`http://localhost:3250`</a> in your browser. The API Documentation is available at <a href="http://localhost:3250/docs">`http://localhost:3250/docs`</a>.