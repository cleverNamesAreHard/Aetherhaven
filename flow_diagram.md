## Flowchart
Flowchart made with [Mermaid.js](https://mermaid.live)
![Game Flowchart](https://i.imgur.com/6uZZnha.png)

## Theme
```
{
  "theme": "dark",
  "themeVariables": {
      "lineColor": "#000000",
      "primaryColor": "#000000",
      "primaryBorderColor": "#000000",
      "fontSize": "24px"
    }
}
```

## Flow
```
flowchart TD
A[run.py] --> B[core/main.py]
B --> C[startup/main_menu.py]

%% Startup menu options
C --> D[services/new_game.py]
C --> E[services/save_load.py]

%% Game state init
D --> F[core/game_state.py]
E --> F

%% Asset loading
B --> G[services/asset_loader.py]

%% Game state dependencies
F --> H[world/world_map.py]
F --> I[player/player_controller.py]
F --> J[economy/resource_manager.py]
F --> K[buildings/building.py]
F --> L[ui/hud.py]
F --> M[ui/build_menu.py]
F --> N[ui/ui_elements.py]

%% World logic
H --> O[world/tile.py]
H --> P[world/expansion.py]

%% Player tools
I --> Q[player/selection_tool.py]

%% Building types
K --> R[buildings/farm.py]
K --> S[buildings/lumber_camp.py]
K --> T[buildings/house.py]
K --> U[buildings/gold_mine.py]
K --> V[buildings/granary.py]
K --> W[buildings/warehouse.py]

%% UI dependencies
M --> K
M --> N
```