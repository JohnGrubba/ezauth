Since the Goal of EZAuth is to be as extensive as possible, it is possible to create your own extensions to add functionality to EZAuth.

## Preparation

To allow Extensions, you need to create a new folder called `extensions/` in the `src/` directory, if it doesn't already exist. This folder is not tracked by git, so you can safely add your own extensions without the risk of losing them when updating the repository.

```sh
mkdir -p src/extensions
```

!!! Tip "EZAuth Developer Mode"
    To also enjoy a greater developement experience, you can start EZAuth in [Development Mode](https://github.com/JohnGrubba/ezauth?tab=readme-ov-file#developement). This will allow you to see changes in your extensions without restarting the server.
    It will also show you more detailed error messages, which can be helpful when developing extensions.



## Creating an Extension

!!! Danger "Extensions can break **EVERYTHING (including all your userdata)**"
    Since Extensions are a really advanced feature, they are not recommended to be developed by beginners. However, if you are an experienced developer, you can create your own extensions.

1. New Folder for the Extension

    Inside the `extensions/` directory, create a new folder for your extension. The name of the folder should be the name of your extension. We force a folder, to make it easier for you to structure your extension and keep an overview of all the installed extensions. We use the name `my_extension` for this example.

    ```sh
    mkdir src/extensions/my_extension
    ```

2. Make the Extension Loadable

    To make EZAuth recognize your extension as a valid one, add a `__init__.py` file to your newly created extension folder. This file **must** be there and export a `router` which is a FastAPI Router.

    Depending on the structure of your Extension, you can either write the whole extension into the `__init__.py` file or import only the router from another file.
    
    !!! Tip "Imports in Extension Files"
        Be careful when doing imports in extensions, as by just importing other files using `.myextension` won't work (importlib can't find the module). You have to use the full import path to the file starting with `extensions.my_extension.` -> E.g. `extensions.my_extension.myextension`

    ```python title="src/extensions/my_extension/myextension.py"
    from fastapi import APIRouter

    router = APIRouter(
        prefix="/test",
        tags=["Test Extension"]
    )

    @router.get("")
    async def test():
        """
        # Test Endpoint
        """
        pass

    ```

    ```python title="src/extensions/my_extension/__init__.py"
    from extensions.my_extension.myextension import router
    ```

3. Provide some information about the Extension

    To make it easier for users to understand what your extension does, you can provide a `README.md` file in your extension folder. This file can contain information about the extension, how to use it, and what it does.

    ```md title="src/extensions/my_extension/README.md"
    # My Extension

    This is a test extension for EZAuth.
    ```

    This is especially useful if you want to share your extension with others.


## Downloading Extensions

If you want to use an extension that someone else has created, you can download it from a repository and place it in the `extensions/` directory. The extension should be structured as described above.

!!! Tip "Extension Repository"
    If you want to share your extension with others, you can create a repository on GitHub or any other platform and share the link with others. This way, others can easily download your extension and use it in their EZAuth instance. If you want to share your extension with the community, you can also create a Pull Request to add your extension to the [official EZAuth Extension Repository](https://github.com/JohnGrubba/ezauth-extensions).