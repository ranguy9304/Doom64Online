# DOOM64 ONLINE

This project involves recreating the iconic DOOM 64-style game, while also implementing LAN-based multiplayer functionality. The primary focus of this project is to design and optimize a server-client model to facilitate seamless data transfer between multiple clients.


## Game Features

- First-person FPS Shooter Experience.
- Free For All gameplay where no winners are declared and the game continues till the server is running.
- Robust Multi-threaded Server to Accommodate Concurrent Player Logins.
- Seamless "Join and Play" Gameplay Experience.
- Assignment of Unique IDs to Each Logged-in Player.
- Client-Side Rendering for Smooth Graphics.
- Comprehensive Server Game State Management, Including Player Health, Position, and Shooting Data.
- once a player dies they will have option to spawn again or leave game.
- Dynamic player limit set after analysing network traffic.

## Design

## Client:

### Player Login
- Upon launching the client script, an initial connection request is dispatched to the server for the assignment of a unique player ID.

### Player Spawning
- Once the server acknowledges the connection request, it responds by providing the coordinates for the player's spawn location, based on available spots within the map.

### Player Control
- Player movement is controlled by the user via the W, A, S, D keys, and mouse movements influence the player's yaw. These updated position data are transmitted to the server to maintain synchronized global player positions.

### Rendering
- We use Pygame as the base library to render every animation and scene of the game.
- All game resources are preloaded on the client-side, enabling rendering to be handled locally.

### Shooting
- Whenever a shooting action (e.g., right-click) is initiated, the client communicates this action to the server for processing.

## Server:

### Multiplayer State Handling
- As described in the client-side flow, the server initially accepts connection requests from players and assigns empty spawn locations on the map where other players are not present.
- Server-side player movement data is continuously updated based on incoming data from clients.
- When a player fires a shot, a trajectory is traced from the player's position until it encounters a wall or another player. If a player is hit, their health is reduced by a specific amount, and this updated data is then broadcast to all clients for reference.

### Multiplayer Data Transfer
- All data transfers are facilitated using JSON as the foundational format for data exchange. Alternatively, objects may be pickled and transmitted over the network, both to and from clients.


## Project File System

```
DOOM64 ONLINE
│
├── resources
│   │
│   ├── sound                   # Different sound assets used in the game
│   ├── sprites                 # Different skins for the opposite players that can be renderd
│   ├── textures                # Different textures for walls, floor, and doors
│   
├── .gitignore                   # Git ignore rules to exclude unnecessary files from version control
├── LICENSE                      # Contains the licensing details for the project
├── main.py                      # Main entry point of the game. Initializes and runs the game loop
├── map.py                       # Defines the game map, its boundaries, and features
├── npc.py                       # Handles non-playable character logic and behavior
├── object_handler.py            # Manages game objects, their states, and interactions
├── object_renderer.py           # Handles rendering of game objects on the screen
├── pathfinding.py               # Pathfinding algorithms for NPC movement
├── player.py                    # Contains player class and handles player-related logic
├── raycasting.py                # Implements raycasting for rendering and player visibility
├── README.md                    # Documentation and overview of the project
├── requirements.txt             # List of Python dependencies required for the project
├── server.py                    # Manages server-side logic for multiplayer gameplay
├── settings.py                  # Configuration and settings for the game
├── sound.py                     # Handles game sound effects and background music
├── sprite_object.py             # Manages sprite-based game objects and their animations
├── team.txt                     # Information about the development team and contributors
├── weapon.py                    # Defines weapons, their behavior, and effects
└── README.md                    # (This file) Overview and documentation for the project

```

## References 

- As this project was majorly focusing on computer network side of things the resources for the GUI were referenced from this public github repo.
  [ https://github.com/StanislavPetrovV/DOOM-style-Game ] 

