# Instalation

1. Make sure you have python 3.X installed and upgrade pip
    ```
    pip install --upgrade pip
    ```
1. Install the virtual env and pipenv
    ```
    pip3 install pipenv
    ```
1. (Optional) Create and activate the virtualenv
    ```
    pipenv shell
    ```
1. Install project with pipenv
    ```
    pipenv install 
    ```

# Running server

```
python3 app.py 
```

# Virbe integration

## Local development

To make sure Virbe platform is able to connect to your local server use `ngrok`

```
ngrok http 9000
```