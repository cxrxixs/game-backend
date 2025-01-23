# game-backend

## Deployment

### Local Deployment

This project requires Docker and Docker Compose.

1.  Navigate to the `docker` directory:

    ```bash
    cd docker
    ```

2.  Run the following command to build and start the application:

    ```bash
    docker compose --env-file .env.dev up --build
    ```

3.  The application will be accessible at `localhost:8000`.

4.  An admin user is automatically created with the following credentials:

    *   Username: `admin`
    *   Password: `admin123`

5.  The admin interface is available at `localhost:8000/admin`.

6.  The main API endpoint is `localhost:8000/api/questions/`.

## API Documentation

### Detailed request/response schemas are available at `/api/docs/`.

### Match API (`/game/match`)

#### Create a new match (`POST`)

*   Endpoint: `/game/match/`
*   Request parameters:
    *   `host_id`: ID of the player hosting the match.

#### List all matches (`GET`)

*   Endpoint: `/game/match/`

#### Fetch match details (`GET`)

*   Endpoint: `/game/match/<match_id>/`

#### Add player to the match (`POST`)

*   Endpoint: `/game/match/<match_id>/player/`
*   Request parameters:
    *   `player_id`: ID of the player joining the match.

#### Fetch player's ongoing match (`GET`)

*   Endpoint: `/game/match/ongoing/?player_id=<player_id>/`
*   Query parameters:
    *   `player_id`: ID of the player.

#### Update match status (`PUT`)

*   Endpoint: `/game/match/<match_id>/`
*   Request parameters:
    *   `player_id`: ID of a player in the match.
    *   `status`: Must be one of: `ongoing`, `expired`, or `finished`.

#### Delete match (`DELETE`)

*   Endpoint: `/game/match/<match_id>/`

### Round API (`/game/round`)

#### Create a round (`POST`)

*   Endpoint: `/game/round/`
*   Request parameters:
    *   `match_id`: ID of the match.
    *   `question_content`: The question for the round.

#### List all rounds (`GET`)

*   Endpoint: `/game/round/`

#### Fetch round details (`GET`)

*   Endpoint: `/game/round/<round_id>/`

### Answer API (`/game/answer`)

#### Create an answer (`POST`)

*   Endpoint: `/game/answer/`
*   Request parameters:
    *   `player_id`: ID of the player.
    *   `game_round_id`: ID of the round.
    *   `answer_index`: Index of the answer.
    *   `answer`: The answer text.
    *   `time`: Time taken to answer.

#### List all answers (`GET`)

*   Endpoint: `/game/answer/`

## Summary of the game match is also available at `/game/summary/`
