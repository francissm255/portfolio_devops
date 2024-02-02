TR_Speedrunning
a totally real speedrunning website

hosts users, games, and runs. runs are associated with one user and one game. allows users to like runs and games.

| Endpoint Path | HTTP Method | Description             | Request Parameters                            | Response Format |
|---------------|-------------|-------------------------|-----------------------------------------------|------------------|
| `/users`      | POST        | create a new user       | `name`(body)`profile_id`(body)                | JSON             |
| `/users/{id}` | GET         | Get user by ID          | `id` (path)                                   | JSON             |
| `/users/{id}` | PATCH, PUT  | Update user by ID       | `id` (path) `name`(body)                      | JSON             |
| `/users/{id}` | DELETE      | Delete user by ID       | `id` (path)                                   | JSON             |
| `/users/{id}` | POST        | Like game or run by ID  | `id` (path) `gam_id`(body) OR `run_id`(body)  | JSON             |

