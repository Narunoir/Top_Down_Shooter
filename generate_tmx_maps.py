"""
TMX Map Generator for Top Down Shooter
Creates levels 8-20 with proper spawn points, walls, and tile layouts
"""
import random
import os

# Level specifications from LEVEL_CREATION_GUIDE.md
LEVEL_SPECS = {
    8: {
        'name': 'Frozen Wasteland',
        'mobs': [('zombie_dog', 35), ('zombie', 8)],
        'theme_tiles': [7, 8, 9, 10],  # Ice/snow themed tiles
    },
    9: {
        'name': 'Graveyard',
        'mobs': [('zombie', 45)],
        'theme_tiles': [1, 2, 3, 4],  # Dark grass tiles
    },
    10: {
        'name': 'Toxic Waste Facility',
        'mobs': [('scorpion', 28), ('robot', 17)],
        'theme_tiles': [1, 2, 3, 4, 7, 8, 9, 10],
    },
    11: {
        'name': 'Underground Lab',
        'mobs': [('robot', 33), ('scorpion', 17)],
        'theme_tiles': [7, 8, 9, 10],
    },
    12: {
        'name': 'Volcano Cavern',
        'mobs': [('zombie', 33), ('mantis', 17)],
        'theme_tiles': [1, 2, 3, 4],
    },
    13: {
        'name': 'Arctic Research Station',
        'mobs': [('zombie_dog', 33), ('robot', 22)],
        'theme_tiles': [7, 8, 9, 10],
    },
    14: {
        'name': 'Shadow Realm',
        'mobs': [('mantis', 53)],
        'theme_tiles': [1, 2, 3, 4],
    },
    15: {
        'name': 'Mutant Stronghold',
        'mobs': [('zombie', 38), ('scorpion', 22)],
        'theme_tiles': [1, 2, 3, 4, 7, 8, 9, 10],
    },
    16: {
        'name': 'Plague Hospital',
        'mobs': [('zombie', 43), ('scorpion', 17)],
        'theme_tiles': [7, 8, 9, 10],
    },
    17: {
        'name': 'Military Base',
        'mobs': [('robot', 43), ('zombie_dog', 22)],
        'theme_tiles': [7, 8, 9, 10],
    },
    18: {
        'name': 'Gothic Castle',
        'mobs': [('zombie', 43), ('mantis', 22)],
        'theme_tiles': [1, 2, 3, 4],
    },
    19: {
        'name': 'Dragon\'s Lair',
        'mobs': [('zombie', 25), ('robot', 20), ('scorpion', 15), ('mantis', 10)],
        'theme_tiles': [1, 2, 3, 4],
    },
    20: {
        'name': 'Final Citadel',
        'mobs': [('zombie', 25), ('robot', 20), ('scorpion', 15), ('mantis', 10), ('zombie_dog', 10)],
        'theme_tiles': [1, 2, 3, 4, 7, 8, 9, 10],
    },
}

def generate_tile_layer(width=100, height=100, theme_tiles=None):
    """Generate a CSV layer of random ground tiles."""
    if theme_tiles is None:
        theme_tiles = [1, 2, 3, 4, 7, 8, 9, 10]

    tiles = []
    for y in range(height):
        row = []
        for x in range(width):
            # Add variety with weighted random selection
            tile_id = random.choice(theme_tiles)
            row.append(str(tile_id))
        tiles.append(','.join(row))

    return ',\n'.join(tiles)

def generate_walls(width=100, height=100, num_walls=50):
    """Generate random wall obstacles."""
    walls = []
    obj_id = 200  # Start ID for walls

    # Border walls
    walls.append(f'  <object id="{obj_id}" name="wall" x="0" y="0" width="{width * 64}" height="64"/>')
    obj_id += 1
    walls.append(f'  <object id="{obj_id}" name="wall" x="0" y="0" width="64" height="{height * 64}"/>')
    obj_id += 1
    walls.append(f'  <object id="{obj_id}" name="wall" x="{(width - 1) * 64}" y="0" width="64" height="{height * 64}"/>')
    obj_id += 1
    walls.append(f'  <object id="{obj_id}" name="wall" x="0" y="{(height - 1) * 64}" width="{width * 64}" height="64"/>')
    obj_id += 1

    # Random interior walls for variety
    for i in range(num_walls):
        x = random.randint(5, width - 10) * 64
        y = random.randint(5, height - 10) * 64
        w = random.randint(1, 8) * 64
        h = random.randint(1, 8) * 64
        walls.append(f'  <object id="{obj_id}" name="wall" x="{x}" y="{y}" width="{w}" height="{h}"/>')
        obj_id += 1

    return walls, obj_id

def generate_mob_spawns(mob_types, start_id, width=100, height=100):
    """Generate mob spawn points scattered across the map."""
    spawns = []
    obj_id = start_id

    for mob_name, count in mob_types:
        for i in range(count):
            # Avoid spawning too close to edges or starting area
            x = random.randint(10, width - 10) * 64 + random.randint(-20, 20)
            y = random.randint(10, height - 10) * 64 + random.randint(-20, 20)
            spawns.append(f'  <object id="{obj_id}" name="{mob_name}" x="{x}" y="{y}" width="32" height="32"/>')
            obj_id += 1

    return spawns, obj_id

def generate_items(start_id, health_packs=5, weapons=2, width=100, height=100):
    """Generate item pickups."""
    items = []
    obj_id = start_id
    weapon_types = ['shotgun', 'flamethrower', 'bazooka', 'grenade']

    # Health packs
    for i in range(health_packs):
        x = random.randint(8, width - 8) * 64
        y = random.randint(8, height - 8) * 64
        items.append(f'  <object id="{obj_id}" name="health_pack" x="{x}" y="{y}" width="32" height="32"/>')
        obj_id += 1

    # Weapons
    for i in range(weapons):
        weapon = random.choice(weapon_types)
        x = random.randint(8, width - 8) * 64
        y = random.randint(8, height - 8) * 64
        items.append(f'  <object id="{obj_id}" name="{weapon}" x="{x}" y="{y}" width="32" height="32"/>')
        obj_id += 1

    return items, obj_id

def generate_tmx_file(level_num, spec):
    """Generate a complete TMX file for a level."""
    width = 100
    height = 100
    tilesize = 64

    # Generate tile layer
    tile_data = generate_tile_layer(width, height, spec['theme_tiles'])

    # Generate walls
    walls, next_id = generate_walls(width, height, num_walls=60)

    # Player spawn (always near start area)
    player_spawn = f'  <object id="1" name="player" x="384" y="576" width="32" height="32"/>'

    # Boss spawn (center of map)
    boss_x = (width // 2) * 64
    boss_y = (height // 2) * 64
    boss_spawn = f'  <object id="2" name="boss" x="{boss_x}" y="{boss_y}" width="128" height="128"/>'

    # Mob spawns
    mob_spawns, next_id = generate_mob_spawns(spec['mobs'], next_id, width, height)

    # Items
    items, next_id = generate_items(next_id, health_packs=6, weapons=3, width=width, height=height)

    # Build TMX content
    tmx_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<map version="1.9" tiledversion="1.9.2" orientation="orthogonal" renderorder="right-down" width="{width}" height="{height}" tilewidth="{tilesize}" tileheight="{tilesize}" infinite="0" nextlayerid="11" nextobjectid="{next_id}">
 <tileset firstgid="1" source="Kenny Topdown Tiles 1.tsx"/>
 <tileset firstgid="541" source="Buss 1.tsx"/>
 <tileset firstgid="607" source="BBQ2.tsx"/>
 <layer id="1" name="Ground" width="{width}" height="{height}">
  <data encoding="csv">
{tile_data}
  </data>
 </layer>
 <objectgroup id="10" name="Obstacles">
{player_spawn}
{boss_spawn}
'''

    # Add all walls
    for wall in walls:
        tmx_content += wall + '\n'

    # Add all mob spawns
    for spawn in mob_spawns:
        tmx_content += spawn + '\n'

    # Add all items
    for item in items:
        tmx_content += item + '\n'

    tmx_content += ''' </objectgroup>
</map>
'''

    return tmx_content

def main():
    """Generate all missing TMX files."""
    maps_folder = 'maps'

    # Ensure maps folder exists
    if not os.path.exists(maps_folder):
        os.makedirs(maps_folder)

    # Generate each level
    for level_num in range(8, 21):
        if level_num not in LEVEL_SPECS:
            print(f"Warning: No spec for level {level_num}, skipping...")
            continue

        spec = LEVEL_SPECS[level_num]
        filename = os.path.join(maps_folder, f'floor{level_num}.tmx')

        print(f"Generating {filename} - {spec['name']}...")

        # Generate TMX content
        tmx_content = generate_tmx_file(level_num, spec)

        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(tmx_content)

        print(f"  [OK] Created {filename} with {sum(count for _, count in spec['mobs'])} mobs")

    print("\n[SUCCESS] All TMX files generated successfully!")
    print("Maps are located in the 'maps' folder")

if __name__ == '__main__':
    main()
