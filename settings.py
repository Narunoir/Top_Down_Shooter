import pygame as pg, pygame
vec = pg.math.Vector2

## Game Options / Settings
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
TITLE  = "Game Name"
WIDTH  = SCREEN.get_width()
HEIGHT = SCREEN.get_height()
FPS    = 60
DEFAULT_FONT_NAME  = 'arial'
TITLE_FONT = 'ZOMBIE.TTF'


# Define colors
WHITE     = (255, 255, 255)
BLACK     = (0, 0, 0)
DARKGREY  = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
RED       = (255, 0, 0)
GREEN     = (0, 255, 0)
BLUE      = (0, 0, 255)
YELLOW    = (255, 255, 0)
BROWN     = (106, 55, 5)
ORANGE    = (245, 78, 16)
CYAN      = (255, 20, 255)

BGCOLOR   = BROWN


# The Size Of the Tiles you will be using
# They should divide evenly into your screen height and width
TILESIZE   = 64
GRIDWIDTH  = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE


WALL_IMG = 'tile_304.png'

# Talent Colors
BG_COLOR = (30, 30, 30)
BOX_COLOR = (255, 100, 50)
HIGHLIGHT_COLOR = (255, 215, 0)
TALENT_BG_COLOR = (10, 10, 60)  # Deep blue for contrast
TEXT_COLOR = (255, 255, 255)






 ## Player Settings
PLAYER_SPEED     = 300
PLAYER_ROT_SPEED = .5
ROTATE_DEADZONE  = 5

PLAYER_IMG = {}
PLAYER_IMG['pistol']  = 'manBlue_gun.png'
PLAYER_IMG['shotgun'] = 'manBlue_shotgun.png'
PLAYER_IMG['flamethrower'] = 'manBlue_flamethrower.png'
PLAYER_IMG['bazooka'] = 'manBlue_Bazooka.png'

#PLAYER_IMG = 'manBlue_shotgun.png'

PLAYER_HIT_RECT  = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET    = vec(25, 8)
PLAYER_HEALTH    = 100


  ## Weapon Settings ##
BULLET_IMG = {}
BULLET_IMG['pistol']          = 'tile_187_2.png'
BULLET_IMG['flamethrower']    = 'flame_bullet.png'
BULLET_IMG['grenade']    = 'grenade_bullet.png'

WEAPONS = {}
WEAPONS['pistol'] =  {'bullet_speed': 500,
                      'bullet_lifetime': 1000,
                      'fireing_rate': 250,
                      'kickback': 0,
                      'gun_spread': 2,
                      'bullet_damage': 20,
                      'bullet_image': 'lg_bullet',
                      'bullet_count': 1,
                      'grenade_lifetime': 1000,
                      'grenade_damage': 0}

WEAPONS['shotgun'] = {'bullet_speed': 400,
                      'bullet_lifetime': 500,
                      'fireing_rate': 900,
                      'kickback': 50,
                      'gun_spread': 20,
                      'bullet_damage': 20,
                      'bullet_image': 'sm_bullet',
                      'bullet_count': 12,
                      'grenade_lifetime': 1000,
                      'grenade_damage': 0}

WEAPONS['flamethrower'] = {'bullet_speed': 600,
                      'bullet_lifetime': 300,
                      'fireing_rate': 100,
                      'kickback': 0,
                      'gun_spread': 9,
                      'bullet_damage': 3,
                      'bullet_image': 'flame_bullet',
                      'bullet_count': 6,
                      'grenade_lifetime': 1000,
                        'grenade_damage': 0}

WEAPONS['bazooka'] =  {'bullet_speed': 950,
                      'bullet_lifetime': 10000,
                      'fireing_rate': 1050,
                      'kickback': 10,
                      'gun_spread': .25,
                      'bullet_damage': 800,
                      'bullet_image': 'grenade',
                      'bullet_count': 1,
                       'grenade_lifetime': 1000,
                       'grenade_damage': 0}

WEAPONS['grenade'] =  {'bullet_speed': 750,
                      'bullet_lifetime': 1000,
                      'fireing_rate': 450,
                      'kickback': 0,
                      'gun_spread': 0,
                      'bullet_damage': 0,
                      'bullet_image': 'grenade',
                      'bullet_count': 1,
                      'grenade_lifetime': 1000,
                       'grenade_damage': 500}

 # Mob Images
MOB_IMG       = 'zoimbie1_hold.png'
SCORPION_MOB_IMG = '2d_scorpion.png'
ROBOT_MOB_IMG = 'robot_mob.png'
MANTIS_MOB_IMG = 'mantis_1.png'
MANTIS_MOB_CAMOUFLAGED_IMG = 'mantis_camo.png'
ZOMBIE_DOG_MOB_IMG = 'zombie_dog.png'
ZOMBIE_BEAR_IMG = 'zombie_dog.png'  # Placeholder brown square


 ## Mob settings
MOB_SPEEDS    = [75, 80, 50, 90, 65]
MOB_HIT_RECT  = pg.Rect(0, 0, 30, 30)
MOB_HEALTH    = 100
MOB_DAMAGE    = 2
MOB_KNOCKBACK = 20
MOB_EXP       = 2  # Experience gained per mob kill
AVOID_RADIUS  = 50
ENGAGE_RADIUS = 750
DISENGAGE_RADIUS = 2000

### Mob Weapons  ###
MOB_BULLET_KNOCKBACK = 20
POISON_BALL_SPEED = 500
POISON_PUDDLE = 'poison_puddle.png'
POISON_DAMAGE = 3
POISON_PUDDLE_DAMAGE = .25
ELECTRO_SHOCK_SPEED = 500
ELECTRO_SHOCK_DAMAGE = 8



MOB_WEAPON_IMAGE = {}
MOB_WEAPON_IMAGE['poison_ball'] = 'poison_ball.png'
MOB_WEAPON_IMAGE['electro_shock'] = 'electro_shock.png'
MOB_WEAPON_IMAGE['poison_puddle'] = 'poison_puddle.png'

MOB_WEAPONS = {}
MOB_WEAPONS['poison_ball'] = {'bullet_speed': 500,
                        'bullet_lifetime': 1000,
                        'fireing_rate': 250,
                        'kickback': 0,
                        'gun_spread': 2,
                        'bullet_damage': 20,
                        'bullet_image': 'poison_ball',
                        'bullet_count': 1,
                        'grenade_lifetime': 1000,
                        'grenade_damage': 0}
MOB_WEAPONS['electro_shock'] = {'bullet_speed': 500,
                        'bullet_lifetime': 1000,
                        'fireing_rate': 250,
                        'kickback': 0,
                        'gun_spread': 2,
                        'bullet_damage': 20,
                        'bullet_image': 'electro_bolt',
                        'bullet_count': 1,
                        'grenade_lifetime': 1000,
                        'grenade_damage': 0}

####Not Needed Anymore  ###
#BULLET_SPEED    = 700
#BULLET_LIFETIME = 750
#BULLET_RATE     = 150  ##  How often the bullets come out.  ##
#KICKBACK        = 0
#GUN_SPREAD      = 5
#BULLET_DAMAGE   = 10

### Map Floors ###
LEVEL = {}
LEVEL[1] = 'floor1.tmx'      # Suburban Neighborhood - 15-20 zombies
LEVEL[2] = 'floor2.tmx'      # City Streets - 20-25 mixed mobs
LEVEL[3] = 'floor3.tmx'      # Industrial Zone - 25-30 robots
LEVEL[4] = 'floor4.tmx'      # Airport Terminal - 20-25 robots + zombies
LEVEL[5] = 'floor5.tmx'      # Highway/Bus Depot - 25-30 zombies
LEVEL[6] = 'floor6.tmx'      # Sewers - 30-35 scorpions + zombies
LEVEL[7] = 'floor7.tmx'      # Mountain Pass - 30-35 zombie dogs + mantis
LEVEL[8] = 'floor8.tmx'      # Frozen Wasteland - 35-40 wolves + zombies
LEVEL[9] = 'floor9.tmx'      # Graveyard - 40-45 zombies + ghosts
LEVEL[10] = 'floor10.tmx'    # Toxic Waste Facility - 40-45 mutants
LEVEL[11] = 'floor11.tmx'    # Underground Lab - 45-50 cyber spiders + robots
LEVEL[12] = 'floor12.tmx'    # Volcano Cavern - 45-50 fire creatures
LEVEL[13] = 'floor13.tmx'    # Arctic Research Station - 50-55 ice golems
LEVEL[14] = 'floor14.tmx'    # Shadow Realm - 50-55 shadow creatures
LEVEL[15] = 'floor15.tmx'    # Mutant Stronghold - 55-60 brutes + mutants
LEVEL[16] = 'floor16.tmx'    # Plague Hospital - 55-60 infected + plague doctors
LEVEL[17] = 'floor17.tmx'    # Military Base - 60-65 mechs + robots
LEVEL[18] = 'floor18.tmx'    # Gothic Castle - 60-65 vampires + bats
LEVEL[19] = 'floor19.tmx'    # Dragon's Lair - 65-70 dragonlings + minions
LEVEL[20] = 'floor20.tmx'    # Final Citadel - 70-80 all enemy types

### Boss Images and Settings  ###
BOSS_EXP = 20  # Default experience gained per boss kill

BOSS = {}
BOSS[1] = {'boss_image':'zoimbie1_hold.png',
            'boss_speed':100,
            'boss_health':8000,
            'boss_damage': 40,
            'boss_hit_rect': pg.Rect(0, 0, 50, 50),
            'boss_exp': 20
            }
BOSS[2] = {'boss_image':'scorpion.png',
            'boss_speed':300,
            'boss_health':5600,
            'boss_damage': 50,
            'boss_hit_rect': pg.Rect(0, 0, 130, 150),
            'boss_exp': 20
            }
BOSS[3] = {'boss_image':'Robot_Boss_1.png',
            'boss_speed':100,
            'boss_health':10000,
            'boss_damage': 45,
            'boss_hit_rect': pg.Rect(0, 0, 50, 50),
            'boss_exp': 20
            }
BOSS[4] = {'boss_image':'Airport_Bot.png',
            'boss_speed':100,
            'boss_health':5000,
            'boss_damage': 45,
            'boss_hit_rect': pg.Rect(0, 0, 50, 50),
            'boss_exp': 20
            }
BOSS[5] = {'boss_image':'Bus_Driver.png',
            'boss_speed':100,
            'boss_health':5000,
            'boss_damage': 40,
            'boss_hit_rect': pg.Rect(0, 0, 50, 50),
            'boss_exp': 20
            }
BOSS[6] = {'boss_image':'scorpion.png',
            'boss_speed':100,
            'boss_health':500,
            'boss_damage': 40,
            'boss_hit_rect': pg.Rect(0, 0, 50, 50),
            'boss_exp': 20
            }
BOSS[7] = {'boss_image':'scorpion.png',
            'boss_speed':100,
            'boss_health':500,
            'boss_damage': 40,
            'boss_hit_rect': pg.Rect(0, 0, 50, 50),
            'boss_exp': 20
            }
BOSS[8] = {'boss_image':'zombie_dog.png',  # Direwolf Alpha
            'boss_speed':200,
            'boss_health':12000,
            'boss_damage': 60,
            'boss_hit_rect': pg.Rect(0, 0, 80, 80),
            'boss_exp': 20
            }
BOSS[9] = {'boss_image':'zoimbie1_hold.png',  # Necromancer
            'boss_speed':80,
            'boss_health':15000,
            'boss_damage': 50,
            'boss_hit_rect': pg.Rect(0, 0, 60, 60),
            'boss_exp': 20
            }
BOSS[10] = {'boss_image':'zoimbie1_hold.png',  # Toxic Abomination
            'boss_speed':90,
            'boss_health':18000,
            'boss_damage': 55,
            'boss_hit_rect': pg.Rect(0, 0, 70, 70),
            'boss_exp': 20
            }
BOSS[11] = {'boss_image':'scorpion.png',  # Cyber Spider Queen
            'boss_speed':120,
            'boss_health':20000,
            'boss_damage': 65,
            'boss_hit_rect': pg.Rect(0, 0, 100, 100),
            'boss_exp': 20
            }
BOSS[12] = {'boss_image':'zoimbie1_hold.png',  # Fire Elemental Lord
            'boss_speed':110,
            'boss_health':22000,
            'boss_damage': 70,
            'boss_hit_rect': pg.Rect(0, 0, 80, 80),
            'boss_exp': 20
            }
BOSS[13] = {'boss_image':'robot_mob.png',  # Ice Golem Titan
            'boss_speed':70,
            'boss_health':25000,
            'boss_damage': 75,
            'boss_hit_rect': pg.Rect(0, 0, 90, 90),
            'boss_exp': 20
            }
BOSS[14] = {'boss_image':'mantis_1.png',  # Shadow Assassin Lord
            'boss_speed':180,
            'boss_health':20000,
            'boss_damage': 90,
            'boss_hit_rect': pg.Rect(0, 0, 70, 70),
            'boss_exp': 20
            }
BOSS[15] = {'boss_image':'zoimbie1_hold.png',  # Mutant Brute King
            'boss_speed':100,
            'boss_health':30000,
            'boss_damage': 85,
            'boss_hit_rect': pg.Rect(0, 0, 100, 100),
            'boss_exp': 20
            }
BOSS[16] = {'boss_image':'zoimbie1_hold.png',  # Plague Doctor Prime
            'boss_speed':90,
            'boss_health':28000,
            'boss_damage': 60,
            'boss_hit_rect': pg.Rect(0, 0, 70, 70),
            'boss_exp': 20
            }
BOSS[17] = {'boss_image':'Robot_Boss_1.png',  # Mech Titan
            'boss_speed':80,
            'boss_health':35000,
            'boss_damage': 100,
            'boss_hit_rect': pg.Rect(0, 0, 120, 120),
            'boss_exp': 20
            }
BOSS[18] = {'boss_image':'zoimbie1_hold.png',  # Vampire Lord
            'boss_speed':150,
            'boss_health':32000,
            'boss_damage': 80,
            'boss_hit_rect': pg.Rect(0, 0, 80, 80),
            'boss_exp': 20
            }
BOSS[19] = {'boss_image':'scorpion.png',  # Ancient Dragon
            'boss_speed':130,
            'boss_health':40000,
            'boss_damage': 120,
            'boss_hit_rect': pg.Rect(0, 0, 150, 150),
            'boss_exp': 20
            }
BOSS[20] = {'boss_image':'Robot_Boss_1.png',  # Apocalypse Overlord
            'boss_speed':120,
            'boss_health':50000,
            'boss_damage': 100,
            'boss_hit_rect': pg.Rect(0, 0, 150, 150),
            'boss_exp': 20
            }
THROW_RANGE = 1500
THROW_SPEED = 750


### Effects  ###
MUZZLE_FLASHES = ['explosion00.png','explosion01.png','explosion02.png','explosion03.png',
                'explosion04.png','explosion05.png','explosion06.png','explosion07.png',
                'explosion08.png',]
FLASH_DURATION = 40
EXPLOSION_DURATION = 80
SPLAT          = 'green_splat.png'
DAMAGE_ALPHA   = [i for i in range(0, 250, 50)]


### Layers  ###
WALL_LAYER    = 1
PLAYER_LAYER  = 2
BULLET_LAYER  = 3
MOB_LAYER     = 2
EFFECTS_LAYER = 4
ITEMS_LAYER   = 1

### Items  ###
ITEM_IMAGES        = {'health_pack': 'med_pack_icon.png',
                      'shotgun': 'obj_shotgun.png',
                      'flamethrower': 'flamethrower_icon.png',
                      'bazooka': 'bazooka.png',
                      'grenade': 'grenade.png'}
HEALTH_PACK_AMOUNT = PLAYER_HEALTH
BOB_RANGE = 20
BOB_SPEED = 0.6

### Sounds ###
BG_MUSIC           = 'espionage.ogg'
PLAYER_HIT_SOUNDS  = ['pain/8.wav','pain/9.wav','pain/10.wav','pain/11.wav',]
ZOMBIE_MOAN_SOUNDS = ['brains2.wav','brains3.wav','zombie-roar-1.wav','zombie-roar-2.wav',
                    'zombie-roar-3.wav','zombie-roar-5.wav','zombie-roar-6.wav','zombie-roar-7.wav']
ZOMBIE_HIT_SOUNDS  =['splat-15.wav']
#WEAPON_SOUNDS_GUN  =['sfx_weapon_singleshot2.wav']   ### Replaced by dictionary
WEAPON_SOUNDS = {'pistol': ['pistol_1.wav'],
                'shotgun': ['shotgun.wav'],
                'flamethrower': ['flamethrower.wav'],
                'bazooka':['shotgun.wav'],
                 'grenade':['pistol_1.wav']}

EFFECTS_SOUNDS     ={'level_start': 'level_start.wav',
                    'health_up': 'health_pack.wav',
                    'gun_pickup': 'gun-pickup.wav'}

CUTSCENE_IMAGES = {}
CUTSCENE_IMAGES[0] = ['Jake_morning_1.png',
                      'Jake_morning_2.png',
                      'Jake_walking_sidewalk_1.png'
                      ]


CUTSCENE_IMAGES[1] = ['jake_by_pool.png',
                      'zombie_pool_attack.png',
                      'zombie_pool_attack_2.png',
                      'zombie_pool_attack_3.png']

'''STORY_SCRIPT = [
    'Trial 1 test words',
    'Trial 2 test words',
    'Trial 3 test words',
    'Trial 4 test words',
    'Trial 5 test words',
    'Trial 6 test words',
    'Trial 7 test words',
    'Trial 8 test words',
    'Trial 9 test words',
]'''
