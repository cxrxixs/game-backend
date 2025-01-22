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



### Game Matching API

Detailed request/response schema is also available at `/api/docs/`

#### Match

* Create new match

        Endpoint: /game/match/
        Method: POST
        Request parameters:
            host_id  - ID of player


* List all matches

        Endpoint: /game/match/
        Method: GET


* Fetch match details

        Endpoint: /game/match/<match_id>/
        Method: GET


* Add player to the match

        Endpoint: /game/match/<match_id>/player/
        Method: POST
        Request parameters:
            player_id  - ID of player


* Fetch player's ongoing match

        Endpoint: /game/match/ongoing/?player_id=<player_id>/
        Method: GET
        Query params:
            player_id - ID of player


* Update match status

        Endpoint: /game/match/<match_id>/
        Method: PUT
        Request parameters:
            player_id - ID of player that is member of the match
               status - Must be one of this choices `ongoing`, `expired`, `finsihed`


* Delete match

        Endpoint: /game/match/<match_id>/
        Method: DELETE


#### Round

* Create round

        Endpoint: /game/round/
        Method: POST
        Request parameters:
            match_id - ID of the match
            question_content - Question for the round


* List all rounds

        Endpoint: /game/round/
        Method: GET


* Fetch round details

        Endpoint: /game/round/<round_id>/
        Method: GET


#### Answer

* Create answer

        Endpoint: /game/answer/
        Method: POST
        Request parameters:
                player_id - ID of the player
            game_round_id - ID of the match round
             answer_index - Index of the answer
                   answer - Answer (text)
                     time - Time took the player to answer

* List all answers

        Endpoint: /game/answer/
        Method: GET
