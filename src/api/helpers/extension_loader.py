import os
from fastapi import FastAPI
import importlib.util
from api.helpers.log import logger
import logging

modules = []

EXTENSIONS_DIR = "/src/app/extensions/"


def load_extensions(app: FastAPI):
    global modules
    # Extension Loading
    if not os.path.exists(EXTENSIONS_DIR):
        return
    for item in os.listdir(EXTENSIONS_DIR):
        item_path = os.path.join(EXTENSIONS_DIR, item)
        init_file = os.path.join(item_path, "__init__.py")
        if os.path.isdir(item_path) and os.path.isfile(init_file):
            readme_file = None
            try:
                readme_file = open(os.path.join(item_path, "README.md"), "r").read()
            except FileNotFoundError:
                logger.error(f"Extension {item} is missing README.md")
            spec = importlib.util.spec_from_file_location(item, init_file)
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
            except Exception as e:
                logger.error(f"Failed to load extension {item}: {e}")
                if logger.level == logging.DEBUG:
                    raise e
                modules.append([spec, module, readme_file, False])
                continue
            modules.append([spec, module, readme_file, True])

    for spec, module, _, valid in modules:
        if valid:
            app.include_router(module.router, prefix=f"/ext/{module.__name__}")

    if len([module.__name__ for spec, module, _, lded in modules if lded]) > 0:
        logger.info(
            "\u001b[32m-> Loaded Extensions: "
            + ", ".join([module.__name__ for spec, module, _, lded in modules if lded])
            + "\u001b[0m"
        )
