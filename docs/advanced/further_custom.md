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