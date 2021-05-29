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
1. Before running the server, make sure to create `.env' file in the root folder with your API KEY
    ```
    cp .env.sample .env
    ```   

# Running server locally

```
python3 -m server.app 
```

# Virbe integration from local server

1. To make sure Virbe platform is able to connect to your local server install and use `ngrok`
   ```
   ngrok http 9000
```

1. Once you create a proxy, go to your being dashboard and change your custom endpoint to `http://<your_ngrok_domina.ngrok.io/api/chat/`
1. You can start chatting with your being