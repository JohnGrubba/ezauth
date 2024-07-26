#!/bin/sh

if [ -f "/src/app/config/ssl/key.pem" ] && [ -f "/src/app/config/ssl/cert.pem" ]; then
    uvicorn api.main:app --host 0.0.0.0 --port 80 --log-level critical --ssl-keyfile /src/app/config/ssl/key.pem --ssl-certfile /src/app/config/ssl/cert.pem
else
    uvicorn api.main:app --host 0.0.0.0 --port 80 --log-level critical
fi