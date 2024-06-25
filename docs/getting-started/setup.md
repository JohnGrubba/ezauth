# Setup / Installation

## Install Docker and Docker Compose

To install and use EZAuth you need to have Docker and Docker Compose installed on your system. If you don't have Docker and Docker Compose installed you can follow the official installation guides for [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).

!!! Info "Docker compose install"
    EZAuth documentation assumes the use of Docker desktop (or the docker compose plugin).  
    While the docker-compose standalone installation still works, it will require changing all `docker compose` commands from `docker compose` to `docker-compose` to work (e.g. `docker compose up -d` will become `docker-compose up -d`).

??? Warning "Docker on windows"
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
For an explanation of the configuration options, see the [Configuration](configuration.md) page.

### Running the service
After you have configured the service you can start it by running the following command:

``` bash
docker compose up -d
```
The service should now be running and you can access the API by navigating to <a href="http://localhost:3250">`http://localhost:3250`</a> in your browser. The API Documentation is available at <a href="http://localhost:3250/docs">`http://localhost:3250/docs`</a>.

### Further Customization
If you want to further customize the service you can take a look at the `docker-compose.yml` file in the root directory of the repository. This file contains all the configuration options for the service. You can change the port on which the service is running, the volume mounts, and the environment variables.

#### API Configuration
The Prefix for all Parameters here is `services.api`.
The Following Environment Variables can be set in the `docker-compose.yml` file to configure the API:


|  Parameter | Description |
|------------|-------------|
| `ports` | **Datatype:** String <br> **Default:** `"3250:80"` <br> Only change the left (host) side of the ports. The API will always run on Port 80 internally, and can be forwarded to any port on the host system. In this example `3250`. |
| `volumes` | **Datatype:** String <br> **Default:** `"./config:/app/config"` <br> The volume mount for the configuration file. Only change the left (host) side of the configuration folder directory. In this example `./config`. |

#### Database Configuration
The Prefix for all Parameters here is `services.db.environment`.
When changing the database configuration, make sure to also change the `api` section in the `docker-compose.yml` file to reflect the new database connection.
The following environment variables can be set in the `docker-compose.yml` file to configure the database connection:

|  Parameter | Description |
|------------|-------------|
| `MONGO_INITDB_ROOT_USERNAME` | **Datatype:** String <br> **Default:** `"admin"` <br> The Root Username for the Database. |
| `MONGO_INITDB_ROOT_PASSWORD` | **Datatype:** String <br> **Default:** `"admin"` <br> The Root Password for the Database. |
| `MONGO_INITDB_DATABASE` | **Datatype:** String <br> **Default:** `"ezauth"` <br> The Database Name. |

You can also change the location of the database data by changing the `volumes` section of the `db` section in the `docker-compose.yml` file.