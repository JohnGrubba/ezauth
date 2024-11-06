import logging

logging.basicConfig(format="%(levelname) -8s %(message)s")

uvicornlogger = logging.getLogger("uvicorn.access")
logger = logging.getLogger("ezauth-server")
logger.setLevel(uvicornlogger.level)
if uvicornlogger.level == logging.CRITICAL:
    logger.setLevel(logging.INFO)
