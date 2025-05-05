# Aetherhaven

Aetherhaven is a chill, top-down city builder focused on growth, exploration, and empire-building.  

You start small on a fixed size map, gathering wood, gold, and food.  From there, expand outward — no enemies, no combat (for now).  Just terrain, resources, and how far you can push your little civilization before it collapses.

## The Game Running So Far
![New Game GIF](new_game_example.gif)

## Flowchart
See [flow_diagram.md](flow_diagram.md)

## Setup

1. Install [Python](https://www.python.org/downloads/release/python-3130/).  The requirements are specifically for 3.13.2.

2. Clone the Repo

```
git clone https://github.com/cleverNamesAreHard/Aetherhaven.git
```

3. Download the Assets [here](https://drive.google.com/drive/folders/1ay2fpUbLDSlYntcqhPshA07vCQpJmvQD?usp=sharing) and place them into the `assets` folder in the repo.

Currently, I don't want to host them on the GitHub due to using a few AI-generated assets, so they're up in Google Drive.  They're folders you can download directly (and verify are real).  They contain some logos, backgrounds, and a font.

4. Create the Virtual Environment

```
cd Aetherhaven
python -m venv venv
```

5. Activate the Virtual Environment

Windows:

```
.\venv\Scripts\activate
```

Mac/Linux:

```
./venv/bin/activate
```

6. Install Requirements

```
pip install -r requirements.txt
```

7. Run it

```
python run.py
```

## Contributing

Wanna help? Fork it and open a pull request when you're ready for review. Try to keep things clean and modular. No giant god-files, please.

If you're adding a new system, try to keep function separated: UI where UI goes, utils where utils go, etc. If you're fixing a bug, you're a real one.

**Important:** Commits to the `master` branch in this repo must be **SSH-signed**.  If your pull request includes unsigned commits, GitHub will block the merge.  Make sure to [set up SSH commit signing](https://stackoverflow.com/questions/72844616/how-do-i-sign-git-commits-using-my-existing-ssh-key) before opening a pull request.

I recommend you use **autopep8**. I will be going through and doing this myself soon on the whole repo.

## TO-DO

1. ~~Basic PyGame window and main loop~~  
2. ~~Main menu UI (with dynamic resume + new game flow)~~  
3. ~~Procedural world generation (Voronoi + Simplex noise)~~  
4. ~~Tile-based map display with biomes and resources~~  
5. Add camera controls (pan & zoom)  
6. Build out unit system (worker, warrior, etc)  
7. UI elements: resource counters, build menu, tile info  
8. Add initial buildings (town center, farm, lumber camp, mine)  
9. Resource gathering & production logic  
10. Procedural map expansion (infinite scrolling world)  
11. Partial save/load system (auto-saves on new game, load support TBD)  
12. Replace placeholder assets with custom art  
13. Add ambient sound & background music  
14. Optimize rendering performance  
15. UI polish and animation  
16. Build packaging (standalone executable/installer)
