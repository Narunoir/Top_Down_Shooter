# Level Creation Guide - Top Down Shooter
## 20 Levels with Bosses and Enemies

This guide explains what TMX files you need to create in Tiled Map Editor for all 20 levels.

---

## Level 1: Suburban Neighborhood
**File**: `floor1.tmx` (Already exists)
- **Mobs**: 15-20 zombies
- **Boss**: Zombie King (already implemented)
- **Theme**: Residential area with houses, yards, fences

---

## Level 2: City Streets
**File**: `floor2.tmx` (Already exists)
- **Mobs**: 20-25 mixed (zombies + scorpions)
- **Boss**: Giant Scorpion (already implemented)
- **Theme**: Urban streets, buildings, cars

---

## Level 3: Industrial Zone
**File**: `floor3.tmx` (Already exists)
- **Mobs**: 25-30 robots
- **Boss**: Robot Commander (already implemented)
- **Theme**: Factories, warehouses, machinery

---

## Level 4: Airport Terminal
**File**: `floor4.tmx` (Already exists)
- **Mobs**: 20-25 mixed (robots + zombies)
- **Boss**: Airport Security Bot (already implemented)
- **Theme**: Airport terminal, gates, luggage areas

---

## Level 5: Highway/Bus Depot
**File**: `floor5.tmx` (Already exists)
- **Mobs**: 25-30 zombies
- **Boss**: Zombie Bus Driver (already implemented)
- **Theme**: Highway, buses, parking lots

---

## Level 6: Sewers
**File**: `floor6.tmx` (Already exists)
- **Mobs**: 30-35 scorpions + zombies
- **Boss**: Sewer Monster (needs implementation)
- **Theme**: Dark sewers, pipes, water channels
- **Boss Moves**: Poison spray, summon rats, acid pool, toxic cloud

---

## Level 7: Mountain Pass
**File**: `floor7.tmx` (Already exists)
- **Mobs**: 30-35 zombie dogs + mantis
- **Boss**: Mountain Troll (needs implementation)
- **Theme**: Rocky mountain path, cliffs, boulders
- **Boss Moves**: Boulder throw, ground slam, rock armor, avalanche

---

## Level 8: Frozen Wasteland
**File**: `floor8.tmx` (CREATE THIS)
- **Mobs**: 35-40 zombie dogs + zombies
- **Boss**: Direwolf Alpha (already started)
- **Theme**: Snow, ice, frozen trees
- **Objects to place**:
  - 35-40 `zombie_dog` spawn points scattered around map
  - 5-8 `zombie` spawn points
  - 1 `boss` spawn point (center or end area)
  - 1 `player` spawn point (start area)
  - Walls: ice barriers, frozen trees
  - Items: 3-4 health_pack, 1-2 weapon pickups
- **Boss Moves**: Pack summon, howling buff, leap attack, frost bite

---

## Level 9: Graveyard
**File**: `floor9.tmx` (CREATE THIS)
- **Mobs**: 40-45 zombies
- **Boss**: Necromancer
- **Theme**: Tombstones, crypts, dead trees, fog
- **Objects to place**:
  - 40-45 `zombie` spawn points among tombstones
  - 1 `boss` spawn point (central crypt)
  - 1 `player` spawn point (cemetery entrance)
  - Walls: crypts, mausoleums, iron fences
  - Items: 4-5 health_pack, 1-2 weapon pickups
- **Boss Moves**: Summon zombies, life drain, dark curse, soul explosion

---

## Level 10: Toxic Waste Facility
**File**: `floor10.tmx` (CREATE THIS)
- **Mobs**: 40-45 scorpions + robots
- **Boss**: Toxic Abomination
- **Theme**: Chemical tanks, radioactive waste, industrial pipes
- **Objects to place**:
  - 25-30 `scorpion` spawn points
  - 15-20 `robot` spawn points
  - 1 `boss` spawn point (main tank area)
  - 1 `player` spawn point
  - Walls: toxic barrels, tanks, pipes
  - Items: 4-5 health_pack, 2 weapon pickups
- **Boss Moves**: Toxic cloud, mutation surge, poison wave, sludge bomb

---

## Level 11: Underground Lab
**File**: `floor11.tmx` (CREATE THIS)
- **Mobs**: 45-50 robots + new cyber spider enemies
- **Boss**: Cyber Spider Queen
- **Theme**: High-tech laboratory, computers, test chambers
- **Objects to place**:
  - 30-35 `robot` spawn points
  - 15-20 `scorpion` spawn points (reuse for spiders)
  - 1 `boss` spawn point (main lab)
  - 1 `player` spawn point
  - Walls: lab equipment, computer servers, glass walls
  - Items: 5 health_pack, 2-3 weapon pickups
- **Boss Moves**: Web trap, electric shock, spawn spiderlings, cyber hack

---

## Level 12: Volcano Cavern
**File**: `floor12.tmx` (CREATE THIS)
- **Mobs**: 45-50 fire-themed zombies + mantis (recolor for fire theme)
- **Boss**: Fire Elemental Lord
- **Theme**: Lava pools, volcanic rock, steam vents
- **Objects to place**:
  - 30-35 `zombie` spawn points
  - 15-20 `mantis` spawn points
  - 1 `boss` spawn point (lava center)
  - 1 `player` spawn point
  - Walls: lava rocks, obsidian walls
  - Items: 5-6 health_pack, 2 weapon pickups
- **Boss Moves**: Fireball barrage, lava eruption, flame aura, meteor strike

---

## Level 13: Arctic Research Station
**File**: `floor13.tmx` (CREATE THIS)
- **Mobs**: 50-55 zombie dogs + robots
- **Boss**: Ice Golem Titan
- **Theme**: Research buildings, ice walls, snow drifts
- **Objects to place**:
  - 30-35 `zombie_dog` spawn points
  - 20-25 `robot` spawn points
  - 1 `boss` spawn point (research dome)
  - 1 `player` spawn point
  - Walls: ice blocks, frozen buildings
  - Items: 6 health_pack, 3 weapon pickups
- **Boss Moves**: Ice spikes, blizzard storm, freeze ray, glacier crash

---

## Level 14: Shadow Realm
**File**: `floor14.tmx` (CREATE THIS)
- **Mobs**: 50-55 mantis (shadow themed)
- **Boss**: Shadow Assassin Lord
- **Theme**: Dark void, shadows, mysterious pillars
- **Objects to place**:
  - 50-55 `mantis` spawn points
  - 1 `boss` spawn point (void center)
  - 1 `player` spawn point
  - Walls: shadow pillars, dark barriers
  - Items: 6 health_pack, 3 weapon pickups (glow in dark)
- **Boss Moves**: Shadow step (teleport), blade dance, darkness cloak, assassination strike

---

## Level 15: Mutant Stronghold
**File**: `floor15.tmx` (CREATE THIS)
- **Mobs**: 55-60 zombies + scorpions (mutant variants)
- **Boss**: Mutant Brute King
- **Theme**: Destroyed military base, rubble, barricades
- **Objects to place**:
  - 35-40 `zombie` spawn points
  - 20-25 `scorpion` spawn points
  - 1 `boss` spawn point (command center)
  - 1 `player` spawn point
  - Walls: concrete barriers, destroyed tanks
  - Items: 7 health_pack, 3-4 weapon pickups
- **Boss Moves**: Berserker rage, ground pound, throw debris, regeneration

---

## Level 16: Plague Hospital
**File**: `floor16.tmx` (CREATE THIS)
- **Mobs**: 55-60 zombies + scorpions
- **Boss**: Plague Doctor Prime
- **Theme**: Abandoned hospital, quarantine zone, medical equipment
- **Objects to place**:
  - 40-45 `zombie` spawn points (infected patients)
  - 15-20 `scorpion` spawn points
  - 1 `boss` spawn point (surgery room)
  - 1 `player` spawn point
  - Walls: hospital beds, medical machines
  - Items: 7-8 health_pack, 3 weapon pickups
- **Boss Moves**: Disease cloud, infect minions, plague bomb, quarantine field

---

## Level 17: Military Base
**File**: `floor17.tmx` (CREATE THIS)
- **Mobs**: 60-65 robots + zombie dogs
- **Boss**: Mech Titan
- **Theme**: Military compound, bunkers, weapon depots
- **Objects to place**:
  - 40-45 `robot` spawn points
  - 20-25 `zombie_dog` spawn points
  - 1 `boss` spawn point (armory)
  - 1 `player` spawn point
  - Walls: concrete bunkers, sandbags, vehicles
  - Items: 8 health_pack, 4 weapon pickups
- **Boss Moves**: Missile barrage, energy cannon, force shield, orbital strike

---

## Level 18: Gothic Castle
**File**: `floor18.tmx` (CREATE THIS)
- **Mobs**: 60-65 zombies + mantis (vampire theme)
- **Boss**: Vampire Lord
- **Theme**: Gothic architecture, castle halls, blood altars
- **Objects to place**:
  - 40-45 `zombie` spawn points (vampire thralls)
  - 20-25 `mantis` spawn points (bat creatures)
  - 1 `boss` spawn point (throne room)
  - 1 `player` spawn point
  - Walls: castle walls, pillars, altars
  - Items: 8 health_pack, 4 weapon pickups
- **Boss Moves**: Life drain, summon bats, blood strike, mist form

---

## Level 19: Dragon's Lair
**File**: `floor19.tmx` (CREATE THIS)
- **Mobs**: 65-70 mixed (all types)
- **Boss**: Ancient Dragon
- **Theme**: Massive cave, treasure piles, dragon bones
- **Objects to place**:
  - 25 `zombie` spawn points
  - 20 `robot` spawn points
  - 15 `scorpion` spawn points
  - 10 `mantis` spawn points
  - 1 `boss` spawn point (treasure hoard)
  - 1 `player` spawn point
  - Walls: cave walls, treasure piles, columns
  - Items: 10 health_pack, 5 weapon pickups
- **Boss Moves**: Fire breath, tail sweep, wing buffet, dragon roar

---

## Level 20: Final Citadel
**File**: `floor20.tmx` (CREATE THIS)
- **Mobs**: 70-80 all enemy types
- **Boss**: Apocalypse Overlord (Final Boss)
- **Theme**: Massive fortress, apocalyptic throne room
- **Objects to place**:
  - 25 `zombie` spawn points
  - 20 `robot` spawn points
  - 15 `scorpion` spawn points
  - 10 `mantis` spawn points
  - 10 `zombie_dog` spawn points
  - 1 `boss` spawn point (throne platform)
  - 1 `player` spawn point
  - Walls: fortress walls, dark pillars, platforms
  - Items: 12 health_pack, 6 weapon pickups, all weapons
- **Boss Moves**: Ultimate barrage, summon champions, reality tear, apocalypse

---

## General TMX Creation Tips

1. **Map Size**: Keep maps between 3000x3000 to 5000x5000 pixels (depends on TILESIZE=64)
2. **Object Layer**: All spawns must be in an object layer
3. **Naming**:
   - `player` - Player spawn (1 per map)
   - `zombie` - Zombie mob
   - `robot` - Robot mob
   - `scorpion` - Scorpion mob
   - `mantis` - Mantis mob
   - `zombie_dog` - Zombie dog mob
   - `boss` - Boss spawn (1 per map)
   - `wall` - Obstacles
   - `health_pack`, `shotgun`, `flamethrower`, `bazooka`, `grenade` - Items

4. **Progressive Difficulty**: Later levels should have:
   - More mobs
   - Tougher mob combinations
   - Less health pickups relative to mob count
   - More complex layouts

5. **Boss Arena**: Create a larger open space for boss fights

---

## Implementation Status
- ✅ Levels 1-5: Fully implemented with bosses
- ✅ Level 8: Direwolf (implemented with 4 moves)
- ✅ Levels 6-7, 9-20: Boss classes created, need TMX files

All boss classes are now implemented in `sprites.py` with 4 special moves each!
