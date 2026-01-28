from settings import WEAPONS
import copy

def build_weapons():
    """Build weapon stats with talent modifiers applied."""
    weapons = copy.deepcopy(WEAPONS)

    # Apply talents to each weapon
    for node_id, rank in PLAYER_TALENTS.items():
        if rank > 0:
            node = TALENT_NODES.get(node_id)
            if node:
                weapon_name = node['weapon']
                if weapon_name in weapons:
                    node["effect"](rank, weapons[weapon_name])

    return weapons


# Define all 40 talent nodes (5 weapons x 8 talents each)
TALENT_NODES = {
    # PISTOL TALENTS (8 total)
    "pistol_1": {
        "name": "Damage+",
        "weapon": "pistol",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"bullet_damage": stats["bullet_damage"] + 3 * rank}
        )
    },
    "pistol_2": {
        "name": "Fire Rate",
        "weapon": "pistol",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"fireing_rate": max(50, stats["fireing_rate"] - 20 * rank)}
        )
    },
    "pistol_3": {
        "name": "Range+",
        "weapon": "pistol",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"bullet_lifetime": int(stats["bullet_lifetime"] * (1 + 0.15 * rank))}
        )
    },
    "pistol_4": {
        "name": "Speed+",
        "weapon": "pistol",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"bullet_speed": int(stats["bullet_speed"] * (1 + 0.1 * rank))}
        )
    },
    "pistol_5": {
        "name": "Spread-",
        "weapon": "pistol",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"gun_spread": max(0.1, stats["gun_spread"] - 0.3 * rank)}
        )
    },
    "pistol_6": {
        "name": "Kickback-",
        "weapon": "pistol",
        "max_rank": 3,
        "effect": lambda rank, stats: stats.update(
            {"kickback": max(0, stats["kickback"] - 5 * rank)}
        )
    },
    "pistol_7": {
        "name": "Multi-Shot",
        "weapon": "pistol",
        "max_rank": 3,
        "effect": lambda rank, stats: stats.update(
            {"bullet_count": 1 + rank}
        )
    },
    "pistol_8": {
        "name": "Mega Dmg",
        "weapon": "pistol",
        "max_rank": 3,
        "effect": lambda rank, stats: stats.update(
            {"bullet_damage": int(stats["bullet_damage"] * (1 + 0.25 * rank))}
        )
    },

    # SHOTGUN TALENTS (8 total)
    "shotgun_1": {
        "name": "Damage+",
        "weapon": "shotgun",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"bullet_damage": stats["bullet_damage"] + 2 * rank}
        )
    },
    "shotgun_2": {
        "name": "Fire Rate",
        "weapon": "shotgun",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"fireing_rate": max(400, stats["fireing_rate"] - 50 * rank)}
        )
    },
    "shotgun_3": {
        "name": "Range+",
        "weapon": "shotgun",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"bullet_lifetime": int(stats["bullet_lifetime"] * (1 + 0.2 * rank))}
        )
    },
    "shotgun_4": {
        "name": "Pellets+",
        "weapon": "shotgun",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"bullet_count": 12 + 2 * rank}
        )
    },
    "shotgun_5": {
        "name": "Spread-",
        "weapon": "shotgun",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"gun_spread": max(5, stats["gun_spread"] - 2 * rank)}
        )
    },
    "shotgun_6": {
        "name": "Kickback-",
        "weapon": "shotgun",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"kickback": max(0, stats["kickback"] - 8 * rank)}
        )
    },
    "shotgun_7": {
        "name": "Speed+",
        "weapon": "shotgun",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"bullet_speed": int(stats["bullet_speed"] * (1 + 0.15 * rank))}
        )
    },
    "shotgun_8": {
        "name": "Mega Pellets",
        "weapon": "shotgun",
        "max_rank": 3,
        "effect": lambda rank, stats: stats.update(
            {"bullet_count": stats["bullet_count"] + 5 * rank}
        )
    },

    # FLAMETHROWER TALENTS (8 total)
    "flamethrower_1": {
        "name": "Damage+",
        "weapon": "flamethrower",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"bullet_damage": stats["bullet_damage"] + 1 * rank}
        )
    },
    "flamethrower_2": {
        "name": "Fire Rate",
        "weapon": "flamethrower",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"fireing_rate": max(30, stats["fireing_rate"] - 10 * rank)}
        )
    },
    "flamethrower_3": {
        "name": "Range+",
        "weapon": "flamethrower",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"bullet_lifetime": int(stats["bullet_lifetime"] * (1 + 0.25 * rank))}
        )
    },
    "flamethrower_4": {
        "name": "Jets+",
        "weapon": "flamethrower",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"bullet_count": 6 + rank}
        )
    },
    "flamethrower_5": {
        "name": "Spread+",
        "weapon": "flamethrower",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"gun_spread": stats["gun_spread"] + 1.5 * rank}
        )
    },
    "flamethrower_6": {
        "name": "DoT Time",
        "weapon": "flamethrower",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"dot_duration": 30000 + 5000 * rank}
        )
    },
    "flamethrower_7": {
        "name": "DoT Damage",
        "weapon": "flamethrower",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"dot_damage": 1.25 + 0.5 * rank}
        )
    },
    "flamethrower_8": {
        "name": "Inferno",
        "weapon": "flamethrower",
        "max_rank": 3,
        "effect": lambda rank, stats: stats.update(
            {"bullet_damage": int(stats["bullet_damage"] * (1 + 0.5 * rank)),
             "bullet_count": stats["bullet_count"] + 2 * rank}
        )
    },

    # BAZOOKA TALENTS (8 total)
    "bazooka_1": {
        "name": "Damage+",
        "weapon": "bazooka",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"bullet_damage": stats["bullet_damage"] + 100 * rank}
        )
    },
    "bazooka_2": {
        "name": "Fire Rate",
        "weapon": "bazooka",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"fireing_rate": max(500, stats["fireing_rate"] - 75 * rank)}
        )
    },
    "bazooka_3": {
        "name": "Speed+",
        "weapon": "bazooka",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"bullet_speed": int(stats["bullet_speed"] * (1 + 0.1 * rank))}
        )
    },
    "bazooka_4": {
        "name": "Blast Size",
        "weapon": "bazooka",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"explosion_size": 200 + 30 * rank}
        )
    },
    "bazooka_5": {
        "name": "Spread-",
        "weapon": "bazooka",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"gun_spread": max(0.05, stats["gun_spread"] - 0.03 * rank)}
        )
    },
    "bazooka_6": {
        "name": "Kickback-",
        "weapon": "bazooka",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"kickback": max(0, stats["kickback"] - 2 * rank)}
        )
    },
    "bazooka_7": {
        "name": "Multi-Shot",
        "weapon": "bazooka",
        "max_rank": 3,
        "effect": lambda rank, stats: stats.update(
            {"bullet_count": 1 + rank}
        )
    },
    "bazooka_8": {
        "name": "Nuke",
        "weapon": "bazooka",
        "max_rank": 3,
        "effect": lambda rank, stats: stats.update(
            {"bullet_damage": int(stats["bullet_damage"] * (1 + 0.3 * rank)),
             "explosion_size": int((stats.get("explosion_size", 200)) * (1 + 0.2 * rank))}
        )
    },

    # GRENADE TALENTS (8 total)
    "grenade_1": {
        "name": "Damage+",
        "weapon": "grenade",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"grenade_damage": stats["grenade_damage"] + 75 * rank}
        )
    },
    "grenade_2": {
        "name": "Throw Rate",
        "weapon": "grenade",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"fireing_rate": max(200, stats["fireing_rate"] - 40 * rank)}
        )
    },
    "grenade_3": {
        "name": "Fuse Time",
        "weapon": "grenade",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"grenade_lifetime": int(stats["grenade_lifetime"] * (1 + 0.15 * rank))}
        )
    },
    "grenade_4": {
        "name": "Blast Size",
        "weapon": "grenade",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"explosion_size": 500 + 50 * rank}
        )
    },
    "grenade_5": {
        "name": "Throw Speed",
        "weapon": "grenade",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"bullet_speed": int(stats["bullet_speed"] * (1 + 0.1 * rank))}
        )
    },
    "grenade_6": {
        "name": "Multi-Nade",
        "weapon": "grenade",
        "max_rank": 3,
        "effect": lambda rank, stats: stats.update(
            {"bullet_count": 1 + rank}
        )
    },
    "grenade_7": {
        "name": "Shrapnel",
        "weapon": "grenade",
        "max_rank": 5,
        "effect": lambda rank, stats: stats.update(
            {"grenade_damage": int(stats["grenade_damage"] * (1 + 0.2 * rank))}
        )
    },
    "grenade_8": {
        "name": "Cluster Bomb",
        "weapon": "grenade",
        "max_rank": 3,
        "effect": lambda rank, stats: stats.update(
            {"bullet_count": stats["bullet_count"] + 2 * rank,
             "explosion_size": int(stats.get("explosion_size", 500) * (1 + 0.15 * rank))}
        )
    },
}

# Initialize player talents - all start at rank 0
PLAYER_TALENTS = {
    # Pistol talents
    "pistol_1": 0, "pistol_2": 0, "pistol_3": 0, "pistol_4": 0,
    "pistol_5": 0, "pistol_6": 0, "pistol_7": 0, "pistol_8": 0,

    # Shotgun talents
    "shotgun_1": 0, "shotgun_2": 0, "shotgun_3": 0, "shotgun_4": 0,
    "shotgun_5": 0, "shotgun_6": 0, "shotgun_7": 0, "shotgun_8": 0,

    # Flamethrower talents
    "flamethrower_1": 0, "flamethrower_2": 0, "flamethrower_3": 0, "flamethrower_4": 0,
    "flamethrower_5": 0, "flamethrower_6": 0, "flamethrower_7": 0, "flamethrower_8": 0,

    # Bazooka talents
    "bazooka_1": 0, "bazooka_2": 0, "bazooka_3": 0, "bazooka_4": 0,
    "bazooka_5": 0, "bazooka_6": 0, "bazooka_7": 0, "bazooka_8": 0,

    # Grenade talents
    "grenade_1": 0, "grenade_2": 0, "grenade_3": 0, "grenade_4": 0,
    "grenade_5": 0, "grenade_6": 0, "grenade_7": 0, "grenade_8": 0,
}

# Cost in EXP to upgrade a talent
TALENT_COST_BASE = 5
def get_talent_cost(current_rank):
    """Calculate the exp cost for the next rank."""
    return TALENT_COST_BASE * (current_rank + 1)
