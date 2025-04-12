# WASM Frontend
Implementation of Python-in-browser WASM frontend using Marimo.

## How to launch it
1. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. You can edit Marimo code via:
    ```bash
    marimo edit use-case.py
    ```

3. You can run the app (local Marimo server -not Python-in-browser-)
    ```bash
    marimo run use-case.py
    ```

4. For export the use case to WASM runtime: 
    ```bash
    marimo export html-wasm use-case.py -o out/use-case.wasm.html
    ```
    and you'll find generated assets in `out/` folder.

5. Run local web server

    ```bash
    cd out
    python3 -m http.server -d . 8080
    ```

    You can access it at http://localhost:8080/use-case.wasm.html
    
    (needs mysql database and flask server deployed).

## Remote access to frontend
[cloudlab.urv.cat/swisshacks](http://swisshacks-1.s3-website.eu-central-1.amazonaws.com/)