# game-backend


### Deploying the application locally
Requires docker and docker compose

Go to `docker` directory
```shell
cd docker

```

While inside the docker directory run docker and build the image. 
```shell
docker compose --env-file .env.dev up --build
```

The application will be accessible via `localhost:8000`

The user `admin` is automatically created.

To access the manage page, login using the credentials
User: `admin`
Password: `admin123`


The API endpoint is on `localhost:8000/api/questions/`
