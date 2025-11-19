# Chat-auth.

The authentication microservice for the distributed chat system.

## Brief.

This microservice is generally responsible for everything that is related to
authentication process. The authentication is based on the stateless approach
using JSON web tokens. That said, we utilize both full advantage of the stateless
tokens and it's main disadvantage - unability to revoke an issued token immediately.

## Stage.
This service is in the stage of active development. Updates are released multiple times a week.

## Features.
This microservice operates with the two domain entities:

1) Session
2) User

Thus it provides all that is required to work with them.

1) Create/Refresh/Terminate sessions.
2) CRU (Deleting is not yet released) operations with User.

## Architecture.

This microservice is built using the Clean Architecture approach.
It consists of 4 layers which are:

1) Domain (entities, value objects)
2) Application layer (domain entities orchestration and business logic)
3) Interface adapters (thin transport layer that incapsulates the internal logic)
4) Infrastructure (frameworks, databases, etc.)

## Usage.

1) Clone the repository.
2) Create .env file in the backed directory using the env_example.txt as an example.
3) ```docker-compose up --build``` in the directory where docker-compose.yaml file is located.
4) The application will be available on **http://localhost:8000**

## Recent updates.

None yet released.

## Docs.

Available at the standard FastAPI docs endpoint **http://localhost:8000/docs**

## Back to Index repository of the whole chat system.

https://github.com/aleksandrshaulskyi/chat-index
