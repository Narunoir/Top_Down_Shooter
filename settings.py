import pygame as pg, pygame
vec = pg.math.Vector2

## Game Options / Settings
TITLE  = "Game Name"
WIDTH  = 1920
HEIGHT = 1024
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



 ## Player Settings
PLAYER_SPEED     = 10
PLAYER_ROT_SPEED = .5

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
                      'kickback': 5,
                      'gun_spread': 2,
                      'bullet_damage': 35,
                      'bullet_size': 'lg',
                      'bullet_count': 1,
                      'grenade_lifetime': 1000,
                      'grenade_damage': 0}

WEAPONS['shotgun'] = {'bullet_speed': 400,
                      'bullet_lifetime': 500,
                      'fireing_rate': 900,
                      'kickback': 200,
                      'gun_spread': 20,
                      'bullet_damage': 8,
                      'bullet_size': 'sm',
                      'bullet_count': 12,
                      'grenade_lifetime': 1000,
                      'grenade_damage': 0}

WEAPONS['flamethrower'] = {'bullet_speed': 600,
                      'bullet_lifetime': 300,
                      'fireing_rate': 100,
                      'kickback': 0,
                      'gun_spread': 9,
                      'bullet_damage': 2,
                      'bullet_size': 'fl',
                      'bullet_count': 6,
                      'grenade_lifetime': 1000,
                        'grenade_damage': 0}

WEAPONS['bazooka'] =  {'bullet_speed': 950,
                      'bullet_lifetime': 10000,
                      'fireing_rate': 1050,
                      'kickback': 10,
                      'gun_spread': .25,
                      'bullet_damage': 800,
                      'bullet_size': 'grenade',
                      'bullet_count': 1,
                       'grenade_lifetime': 1000,
                       'grenade_damage': 0}

WEAPONS['grenade'] =  {'bullet_speed': 750,
                      'bullet_lifetime': 1000,
                      'fireing_rate': 450,
                      'kickback': 0,
                      'gun_spread': 0,
                      'bullet_damage': 0,
                      'bullet_size': 'grenade',
                      'bullet_count': 1,
                      'grenade_lifetime': 1000,
                       'grenade_damage': 500}


####Not Needed Anymore  ###
#BULLET_SPEED    = 700
#BULLET_LIFETIME = 750
#BULLET_RATE     = 150  ##  How often the bullets come out.  ##
#KICKBACK        = 0
#GUN_SPREAD      = 5
#BULLET_DAMAGE   = 10

### Map Floors ###
LEVEL = {}
LEVEL[1] = 'floor1.tmx'
LEVEL[2] = 'floor2.tmx'
LEVEL[3] = 'floor3.tmx'
LEVEL[4] = 'floor4.tmx'
LEVEL[5] = 'floor5.tmx'
#LEVEL[6] = 'floor1.tmx'
#LEVEL[7] = 'floor2.tmx'
#LEVEL[8] = 'floor3.tmx'
#LEVEL[9] = 'floor4.tmx'
#LEVEL[10] = 'floor5.tmx'

### Boss Images and Settings  ###
BOSS = {}
BOSS[1] = {'boss_image':'zoimbie1_hold.png',
            'boss_speed':100,
            'boss_health':800,
            'boss_damage': 40,
            'boss_hit_rect': pg.Rect(0, 0, 50, 50)
            }
BOSS[2] = {'boss_image':'scorpion.png',
            'boss_speed':300,
            'boss_health':2600,
            'boss_damage': 50,
            'boss_hit_rect': pg.Rect(0, 0, 128, 128)
            }
BOSS[3] = {'boss_image':'Robot_Boss_1.png',
            'boss_speed':100,
            'boss_health':500,
            'boss_damage': 45,
            'boss_hit_rect': pg.Rect(0, 0, 50, 50)
            }
BOSS[4] = {'boss_image':'Airport_Bot.png',
            'boss_speed':100,
            'boss_health':500,
            'boss_damage': 45,
            'boss_hit_rect': pg.Rect(0, 0, 50, 50)
            }
BOSS[5] = {'boss_image':'Bus_Driver.png',
            'boss_speed':100,
            'boss_health':500,
            'boss_damage': 40,
            'boss_hit_rect': pg.Rect(0, 0, 50, 50)
            }
BOSS[6] = {'boss_image':'scorpion.png',
            'boss_speed':100,
            'boss_health':500,
            'boss_damage': 40,
            'boss_hit_rect': pg.Rect(0, 0, 50, 50)
            }
BOSS[7] = {'boss_image':'scorpion.png',
            'boss_speed':100,
            'boss_health':500,
            'boss_damage': 40,
            'boss_hit_rect': pg.Rect(0, 0, 50, 50)
            }
BOSS[8] = {'boss_image':'scorpion.png',
            'boss_speed':100,
            'boss_health':500,
            'boss_damage': 40,
            'boss_hit_rect': pg.Rect(0, 0, 50, 50)
            }
BOSS[9] = {'boss_image':'scorpion.png',
            'boss_speed':100,
            'boss_health':500,
            'boss_damage': 40,
            'boss_hit_rect': pg.Rect(0, 0, 50, 50)
            }
BOSS[10] = {'boss_image':'scorpion.png',
            'boss_speed':100,
            'boss_health':500,
            'boss_damage': 40,
            'boss_hit_rect': pg.Rect(0, 0, 50, 50)
            }
 ## Mob settings
MOB_IMG       = 'zoimbie1_hold.png'
MOB_SPEEDS    = [100, 125, 150, 175, 200]
MOB_HIT_RECT  = pg.Rect(0, 0, 30, 30)
MOB_HEALTH    = 100
MOB_DAMAGE    = 2
MOB_KNOCKBACK = 20
AVOID_RADIUS  = 50
ENGAGE_RADIUS = 550

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
