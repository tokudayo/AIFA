# Installation
## Docker
### Prerequisites
To deploy the software on Docker, you need to have the following installed:
* WSL 2
* Docker 20.10.17

### Installation
To get the software running, follow these steps:
1. Clone the repo
   ```sh
   git clone https://github.com/tokudayo/AIFA.git
   ```
2. Rename all ```.env.example``` to ```.env``` and fill in the required information.
3. Build the images and run the container.
    ```sh
    docker-compose up -d
    ```

## Local
### Prerequisites
To run locally, user should have the following prerequisites:
* Python 3.10
* NodeJs 16.17.1

### Installation
To get the software running locally, follow these steps:
1. Clone the repo
   ```sh
   git clone https://github.com/tokudayo/AIFA.git
   ```

2. Get the frontend running
    ```sh
    cd frontend
    cp .env.example .env
    yarn install
    yarn start
    ``` 

3. Get the backend running
    ```sh
    cd backend
    cp .env.example .env
    yarn install
    yarn start
    ```

4. Get the AI running
    ```sh
    cd ai
    pip install -r requirements.txt
    python run.py
    ```
