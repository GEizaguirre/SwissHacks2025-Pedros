# Frontend Swisshack
Implementation of Python-in-browser WASM frontend using Marimo.

## How to launch it
1. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. You can edit Marimo code via:
    ```bash
    marimo edit
    ```

3. You can run the app (local Marimo server -not Python-in-browser-)
    ```bash
    marimo use-case.py
    ```

4. For export the use case to WASM runtime: 
    ```bash
    marimo export html-wasm use-case.py -o out/use-case.wasm.html
    ```
    and you'll find generated assets in `out/` folder.

## Remote access to frontend
[cloudlab.urv.cat/swisshacks](http://swisshacks-1.s3-website.eu-central-1.amazonaws.com/)