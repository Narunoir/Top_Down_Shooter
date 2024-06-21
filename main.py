import pygame as pg, pygame
import sys
from os import path
from settings import *
from sprites import*
from tilemap import *
from story import *               
import os


## HUD Functions ##
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(int(x), int(y), int(fill), BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

def draw_boss_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 800
    BAR_HEIGHT = 40
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(int(x), int(y), int(fill), BAR_HEIGHT)
    if pct > 0.7:
        col = GREEN
    elif pct > 0.4:
        col = YELLOW
    elif pct > 0.1:
        col = ORANGE
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


class Game:
    def __init__(self):
        # initialize game window, ect
        pg.mixer.pre_init(44100, -16, 1, 2048)
        pygame.init()
        pygame.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        pg.key.set_repeat(50, 10)
        self.clock = pygame.time.Clock()
        self.load_data()
        
        


    def load_data(self):
        game_folder = path.dirname(sys.argv[0])
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')
        self.map_folder = path.join(game_folder, 'maps')
        wall_folder = path.join(game_folder, 'img')
        mob_folder  = path.join(game_folder, 'img')
        self.title_font = path.join(game_folder, 'img', TITLE_FONT)
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.img_folder = img_folder
        self.running = True
        self.font_name = pg.font.match_font(DEFAULT_FONT_NAME)
        self.current_level = 1
        self.fighting_boss = False
        self.score = 0
        self.go_fast_timer = 0
        self.camera_x = 0
        self.camera_y = 0
        #self.player_img = {}
        #self.player_img['pistol'] = pg.image.load(path.join(img_folder, PLAYER_IMG['pistol'])).convert_alpha()
        #self.player_img['shotgun']= pg.image.load(path.join(img_folder, PLAYER_IMG['pistol'])).convert_alpha()
        #self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.player_img_gun = pg.image.load(path.join(img_folder, PLAYER_IMG['pistol'])).convert_alpha()
        self.player_img = self.player_img_gun
        self.player_img_shotgun = pg.image.load(path.join(img_folder, PLAYER_IMG['shotgun'])).convert_alpha()
        self.player_img_flamethrower = pg.image.load(path.join(img_folder, PLAYER_IMG['flamethrower'])).convert_alpha()
        self.player_img_bazooka = pg.image.load(path.join(img_folder, PLAYER_IMG['bazooka'])).convert_alpha()
        
        self.mob_img = pg.image.load(path.join(mob_folder, MOB_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(wall_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))

        self.bullet_images = {}
        self.bullet_images['lg'] = pg.image.load(path.join(img_folder, BULLET_IMG['pistol'])).convert_alpha()
        self.bullet_images['sm'] = pg.transform.scale(self.bullet_images['lg'], (10, 10))
        self.bullet_images['fl'] = pg.image.load(path.join(img_folder, BULLET_IMG['flamethrower'])).convert_alpha()
        self.bullet_images['grenade'] = pg.image.load(path.join(img_folder, BULLET_IMG['grenade'])).convert_alpha()
        self.grenade_img = pg.image.load(path.join(img_folder, 'grenade.png')).convert_alpha()

        self.cutscene_images = {}
        for key, images in CUTSCENE_IMAGES.items():
            self.cutscene_images[key] = []
            for image in images:
                image_path = path.join(img_folder, 'Cutscene_images', image)
                loaded_image = pg.image.load(image_path).convert_alpha()
                loaded_image = pg.transform.scale(loaded_image, (WIDTH, HEIGHT))
                self.cutscene_images[key].append(loaded_image)
    
        self.boss_image = {}
        self.boss_image[1] = pg.image.load(path.join(img_folder, BOSS[1]['boss_image'])).convert_alpha()
        self.boss_image[1] = pg.transform.scale(self.boss_image[1], (100, 100))
        self.boss_image[2] = pg.image.load(path.join(img_folder, BOSS[2]['boss_image'])).convert_alpha()
        self.boss_image[2] = pg.transform.scale(self.boss_image[2], (250, 250))
        self.boss_image[3] = pg.image.load(path.join(img_folder, BOSS[3]['boss_image'])).convert_alpha()
        self.boss_image[4] = pg.image.load(path.join(img_folder, BOSS[4]['boss_image'])).convert_alpha()
        self.boss_image[5] = pg.image.load(path.join(img_folder, BOSS[5]['boss_image'])).convert_alpha()
        self.boss_image[6] = pg.image.load(path.join(img_folder, BOSS[6]['boss_image'])).convert_alpha()
        self.boss_image[7] = pg.image.load(path.join(img_folder, BOSS[7]['boss_image'])).convert_alpha()
        self.boss_image[8] = pg.image.load(path.join(img_folder, BOSS[8]['boss_image'])).convert_alpha()
        self.boss_image[9] = pg.image.load(path.join(img_folder, BOSS[9]['boss_image'])).convert_alpha()
        self.boss_image[10] = pg.image.load(path.join(img_folder, BOSS[10]['boss_image'])).convert_alpha()



        self.splat = pg.image.load(path.join(img_folder, SPLAT)).convert_alpha()
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
        ### Sound loading
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))
        self.weapon_sounds = {}
        
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(path.join(snd_folder, snd))
                s.set_volume(.05)
                self.weapon_sounds[weapon].append(s)
        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.25)
            self.zombie_moan_sounds.append(s)
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            phs = pg.mixer.Sound(path.join(snd_folder, snd))
            phs.set_volume(1)
            self.player_hit_sounds.append(phs)
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            zhs = pg.mixer.Sound(path.join(snd_folder, snd))
            zhs.set_volume(.15)
            self.zombie_hit_sounds.append(zhs)

    def next_level(self):
        if self.current_level <=4:
            self.next_lvl_screen()
            self.current_level += 1
            self.new()
        else:
            self.end_game_screen()
            self.current_level = 1
            self.score = 0
            self.show_start_screen()
            self.new()

    def new(self):
        # starts a new game
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.boss = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.dot_effects = pygame.sprite.Group()
        self.draw_text
        self.fighting_boss = False
        self.player_img = self.player_img_gun
        self.z_count = len(self.mobs)
        self.map = TiledMap(path.join(self.map_folder, LEVEL[self.current_level]))
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width // 2,
                            tile_object.y + tile_object.height // 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'zombie':
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,
                        tile_object.width, tile_object.height)
            if tile_object.name in ['health_pack', 'shotgun', 'flamethrower', 'bazooka', 'grenade']:
                Item(self, obj_center, tile_object.name)

        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False
        self.effects_sounds['level_start'].set_volume(.25)
        self.effects_sounds['level_start'].play()


    def run(self):
        # Game Loop
        self.playing = True
        pg.mixer.music.play(loops = -1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()


    def update(self):
        # Updates the whole general loop
        self.all_sprites.update()
        self.camera.update(self.player)
        self.check_rects()
        # Update DotEffect instances
        for dot_effect in self.dot_effects:  # Assuming self.dot_effects is the list of DotEffect instances
            dot_effect.update()
        ## level over ##########################################################################
        z_count = len(self.mobs)
        if z_count == 0 and self.fighting_boss == True:
            z_count += 1
            self.next_level()
        if z_count == 0 and self.fighting_boss == False:
            self.fighting_boss = True
            for tile_object in self.map.tmxdata.objects:
                obj_center = vec(tile_object.x + tile_object.width / 2,
                                tile_object.y + tile_object.height / 2)
                if tile_object.name == 'boss':
                    Boss(self, obj_center.x, obj_center.y)


        ######  Go Fast Timer   #########
        now = pg.time.get_ticks()
        if now - self.go_fast_timer > 30000 and self.score > 50:
            self.go_fast_timer = now
            self.score -= 10
            


        ## Player item pick up ##
            
        hits = pg.sprite.spritecollide(self.player, self.items, False, collide_hit_rect)
        for hit in hits:
            if hit.type == 'health_pack' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.effects_sounds['health_up'].play()
                self.player.add_health(HEALTH_PACK_AMOUNT)
            if hit.type == 'shotgun':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'shotgun'
                self.player_img = self.player_img_shotgun
                self.player.has_shotgun = True
            if hit.type == 'flamethrower':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'flamethrower'
                self.player_img = self.player_img_flamethrower
                self.player.has_flamethrower = True
            if hit.type == 'bazooka':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'bazooka'
                self.player_img = self.player_img_bazooka
                self.player.has_bazooka = True
            if hit.type == 'grenade':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.grenade_count += 1
                
        ## Mobs Hit Player  ##
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            if random.random() < 0.7:
                choice(self.player_hit_sounds).play()
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
            #if self.score >=50:
                
                #self.score -= 50
        if hits:
            self.player.got_hit()
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        ##### Boss hits player  ####
        hits = pg.sprite.spritecollide(self.player, self.boss, False, collide_hit_rect)
        for hit in hits:
            self.player.health -= BOSS[self.current_level]['boss_damage']
        ## Bullets hit Mobs  ##
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, False)
        for mob in hits:
            for bullet in hits[mob]:
                mob.health -= bullet.damage
                # Check if the bullet is a Rocket
                if isinstance(bullet, Flame):
                    # Create an explosion at the mob's position
                    explosion_size = bullet.explosion_size 
                    Explosion(self, mob.pos, explosion_size, 0)
                    # Apply DoT effect to the mob
                    dot_effect = DotEffect(self, mob, 2, 30000, 1)  # Create a DotEffect instance
                    mob.apply_dot(dot_effect)
                    bullet.kill()
                elif isinstance(bullet, Rocket):
                    explosion_size = bullet.explosion_size      
                    Explosion(self, mob.pos, explosion_size, 50)
                    bullet.kill()
                elif isinstance(bullet, Grenade):
                    explosion_size = bullet.explosion_size                    
                elif isinstance(bullet, Bullet):
                    bullet.kill()
            mob.vel = vec(0,0)

    def events(self):
        # events that need to be stored like actions and movement
        for event in pygame.event.get():
            keys = pg.key.get_pressed()   # Get the state of all keyboard buttons
            # closeing Windows
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_p:
                    self.paused = not self.paused
                if keys[pg.K_p] and [pg.K_o] and [pg.K_i] and [pg.K_LSHIFT]:
                    self.next_level()
                if event.key == pg.K_0:
                    # Then, you can iterate over the mapping and call each cutscene
                    self.cutscene(STORY_SCRIPT[0], self.img_folder, self.cutscene_images[0])
                if event.key == pg.K_9:
                    self.fighting_boss = True
                    for tile_object in self.map.tmxdata.objects:
                        if tile_object.name == 'boss':
                            obj_center = vec(tile_object.x + tile_object.width / 2,
                                            tile_object.y + tile_object.height / 2)
                            # Fetch and call the lambda function to instantiate the boss
                            boss_creator = LEVEL_BOSS.get(self.current_level)
                            if boss_creator:
                                boss_creator(self, obj_center.x, obj_center.y)


    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (int(x), int(y))
        self.screen.blit(text_surface, text_rect)
        
    def display_player_position(self, player_pos):
        font = pg.font.Font(None, 36)  # Define the font for the text
        pos_text = f'Player Position: {player_pos}'
        text_surface = font.render(pos_text, True, (255, 255, 255))  # Create a surface with the text
        text_rect = text_surface.get_rect()  # Get the rectangle of the text surface
        text_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)  # Position the text rectangle at the center of the screen
        self.screen.blit(text_surface, text_rect)  # Blit the text surface onto the screen
    def check_rects(self):
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]  # Different colors for outlining
        color_index = 0
        font = pg.font.Font(None, 36)  # Define the font for the text
        player_pos = None
        self.mouse_center = pygame.mouse.get_pos()

        for sprite in self.all_sprites:
            # Print the details of the sprite's rect
            print(f'Sprite: {sprite}, Rect: {sprite.rect}')

            # Outline the sprite in a different color
            outline_color = colors[color_index]
            pg.draw.rect(self.screen, outline_color, self.camera.apply_rect(sprite.rect), 1)

            # Update the color index for the next color
            color_index = (color_index + 1) % len(colors)

            # Store the player's position
            if isinstance(sprite, Player):
                player_pos = sprite.pos

        mouse_center_x, mouse_center_y = self.mouse_center  # Get mouse center position
        square_size = 20  # Define the size of the square
        square_color = (0, 0, 0)  # Define the color of the square (black)

        # Calculate the top left corner of the square
        top_left_x = mouse_center_x - square_size // 2
        top_left_y = mouse_center_y - square_size // 2

        # Draw the square
        pg.draw.rect(self.screen, square_color, (top_left_x, top_left_y, square_size, square_size))

        # Display the player's position
        if player_pos is not None:
            pos_text = f'Player Position: {player_pos}'
            text_surface = font.render(pos_text, True, (255, 255, 255))  # Create a surface with the text
            text_rect = text_surface.get_rect()  # Get the rectangle of the text surface
            text_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)  # Position the text rectangle at the center of the screen
            self.screen.blit(text_surface, text_rect)  # Blit the text surface onto the screen
    def check_rects_with_mouse(self):
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]  # Different colors for outlining
        color_index = 0
        mouse_pos = pg.mouse.get_pos()  # Get the current mouse position
        mouse_rect = None  # This will store the rectangle that the mouse is over

        for sprite in self.all_sprites:
            # Print the details of the sprite's rect
            print(f'Sprite: {sprite}, Rect: {sprite.rect}')

            # Outline the sprite in a different color
            outline_color = colors[color_index]
            pg.draw.rect(self.screen, outline_color, self.camera.apply_rect(sprite.rect), 1)

            # If the mouse is inside this sprite's rectangle, store it
            if sprite.rect.collidepoint(mouse_pos):
                mouse_rect = sprite.rect

            # Update the color index for the next color
            color_index = (color_index + 1) % len(colors)

        # If the mouse is over a rectangle, draw a square at its center
        if mouse_rect is not None:
            mouse_center_x, mouse_center_y = mouse_rect.center  # Get mouse rect center position
            square_size = 20  # Define the size of the square
            square_color = (0, 0, 0)  # Define the color of the square (black)

            # Calculate the top left corner of the square
            top_left_x = mouse_center_x - square_size // 2
            top_left_y = mouse_center_y - square_size // 2

            # Draw the square
            pg.draw.rect(self.screen, square_color, (top_left_x, top_left_y, square_size, square_size))

            # Create a font object
            font = pg.font.Font(None, 36)

            # Create a surface with the details of the rectangle
            text_surface = font.render(f'Rect: {mouse_rect}', True, (255, 255, 255))

            # Draw the surface on the screen
            self.screen.blit(text_surface, (50, 50))  # Draw at position (10, 10)


    def mouse_rect(self):
        mouse_pos = pg.mouse.get_pos()
        mouse_rect = pg.Rect(mouse_pos[0], mouse_pos[1], 10, 10)
        pg.draw.rect(self.screen, (255, 0, 0), mouse_rect)
        player_rect = self.player.rect
        pg.draw.rect(self.screen, (0, 255, 0), self.camera.apply_rect(player_rect), 2)
        self.display_player_position(self.player.pos)
        # always last to view changes

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    
    def find_boss(self):
        for sprite in self.mobs.sprites():
            if hasattr(sprite, 'boss_level') and sprite.is_boss:
                return sprite
        return None  # Return None if no boss is found

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        
        ### Draws everything ###
        self.screen.blit(self.map_img, self.camera.apply(self.map))
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)
        ## HUD  ##
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        if self.fighting_boss:
            try:
                boss_instance = self.find_boss()
                draw_boss_health(self.screen, 10, 40, boss_instance.health / BOSS[self.current_level]['boss_health'])
            except:
                draw_boss_health(self.screen, 10, 40, 0)
        ##Zombie counter ##
        self.draw_text('Zombies: {}'.format(len(self.mobs)),self.font_name, 30, WHITE, WIDTH / 2, 15, 'center')
        self.draw_text('Score: {}'.format(self.score),self.font_name, 30, WHITE, WIDTH / 4, 15, 'center')
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 205, RED, WIDTH / 2, HEIGHT / 2, 'center')
        ### Grenade count indicator ###        
        grenade_width, grenade_height = self.grenade_img.get_size()
        grenade_spacing = 5
        max_grenades = 5
        for i in range(max_grenades):
            x = i * (grenade_width + grenade_spacing) + 1200
            y = 10  # adjust the y position to move the indicator up or down
            

            if i < self.player.grenade_count:
                self.screen.blit(self.grenade_img, (x, y))
            else:
                # Draw an empty slot (optional)
                pg.draw.rect(self.screen, (255, 255, 255), (x, y, grenade_width, grenade_height), 1)
        #self.check_rects()
        #self.mouse_rect()
        # always last to view changes
        pygame.display.flip()


    def show_start_screen(self):
        # opens a start screen
        # opens a game over screen
        self.screen.fill(BLACK)
        self.draw_text('ZOMBIES ATE MY BLOCKS', self.title_font, 100, RED, WIDTH / 2, HEIGHT / 2 - 300, align='center')
        self.draw_text('Press The Enter Key to Begin',self.title_font, 75, WHITE, WIDTH / 2, HEIGHT /2 - 200, align='center')
        self.draw_text('Move with your left mouse button, or the W key',self.title_font, 75, WHITE, WIDTH / 2, HEIGHT /2 + 240, align='center')
        self.draw_text('Switch weapons with keys 1, 2, 3, 4',self.title_font, 75, WHITE, WIDTH / 2, HEIGHT /2 + 340, align='center')
        pg.display.flip()
        self.wait_for_key()
    
    
    '''def next_lvl_screen(self):
        # opens a Next Level screen
        self.screen.fill(BLACK)
        self.draw_text('Next Level, Get Ready', self.title_font, 100, RED, WIDTH / 2, HEIGHT / 2, align='center')
        self.draw_text('Score {}'.format(self.score), self.title_font, 100, WHITE, WIDTH / 3, HEIGHT / 4, align='center')
        self.draw_text('Press The Enter Key To Start',self.title_font, 75, WHITE,
                        WIDTH / 2, HEIGHT /2 + 140, align='center')
        pg.display.flip()
        self.wait_for_key()'''
    
    def next_lvl_screen(self):
        # opens a Next Level screen
        self.screen.fill(BLACK)
        text = 'Next Level, Get Ready'
        words = text.split(' ')
        for i in range(len(words)):
            self.screen.fill(BLACK)  # Clear the screen
            self.draw_text(' '.join(words[:i+1]), self.title_font, 100, RED, WIDTH / 2, HEIGHT / 2, align='center')
            pg.display.flip()
            self.wait_for_a_short_time(250)  # wait for a short time before drawing the next word
        self.draw_text('Score {}'.format(self.score), self.title_font, 100, WHITE, WIDTH / 3, HEIGHT / 4, align='center')
        self.draw_text('Press The Enter Key To Start', self.title_font, 75, WHITE, WIDTH / 2, HEIGHT / 2 + 140, align='center')
        pg.display.flip()
        self.wait_for_key()
    def wait_for_a_short_time(self, delay_time):
        # wait for a short time (e.g. 0.5 seconds)
        pg.time.delay(delay_time)

    def cutscene(self, text, image_folder, image_files, zoom=False):
        title_font = pg.font.SysFont('arial', 100)       
        current_stage = 0       
        zoom_level = 1
        zoom_speed = 0.1
        max_zoom = 2

        for image in image_files:
            # Zoom the image if zoom is True
            if zoom:
                image = pygame.transform.scale(image, (int(image.get_width() * zoom_level), int(image.get_height() * zoom_level)))

            self.screen.blit(image, (0, 0))  # Draw the image at position (x, y)

            # Split the text into words
            words = STORY_SCRIPT[current_stage].split(' ')
            # Display the images one at a time               
            x_position = 200  # Start from the left of the screen
            y_position = HEIGHT / 2  # Start from the middle of the screen
            for word in words:
                # Render and blit each word separately
                word_surface = title_font.render(word, True, WHITE)
                word_rect = word_surface.get_rect(topleft=(x_position, y_position))
                self.screen.blit(word_surface, word_rect.topleft)
                pg.display.flip()
                self.wait_for_a_short_time(200)
                x_position += (word_surface.get_width() + 100)

                # Check if the word goes off the screen
                if x_position + word_surface.get_width() > WIDTH:
                    x_position = 200  # Reset x position to start from the left
                    y_position += word_surface.get_height() + 20  # Move up to fit longer paragraphs
                if y_position + word_surface.get_height() > HEIGHT:
                    x_position = 200  # Reset x position to start from the left
                    y_position -= word_surface.get_height() + 20  # Move up to fit longer paragraphs
                
                # Zoom in or out if zoom is True
                if zoom:
                    zoom_level += zoom_speed
                    zoom_level = min(max(zoom_level, 1), max_zoom)  # Limit zoom level
            # Check for escape key press to exit the cut scene
            '''for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                        return'''
            current_stage += 1
            #self.wait_for_key()
        # Display the final message
        self.draw_text('Press The Enter Key To Continue', self.title_font, 75, WHITE, WIDTH / 2, HEIGHT / 2 + 140, align='center')
        pg.display.flip()
        self.wait_for_key()
        self.paused = not self.paused


    def end_game_screen(self):
        # opens a Next Level screen
        self.screen.fill(BLACK)
        self.draw_text('You Beat The Game, GREAT JOB!!!', self.title_font, 100, RED, WIDTH / 2, HEIGHT / 2, align='center')
        self.draw_text('Score {}'.format(self.score), self.title_font, 250, WHITE, WIDTH / 3, HEIGHT / 4, align='center')
        self.draw_text('Press The Enter Key To Start',self.title_font, 75, WHITE,
                        WIDTH / 2, HEIGHT /2 + 140, align='center')
        pg.display.flip()
        self.wait_for_key()


    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            keys = pg.key.get_pressed()
            pg.event.clear()
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP and keys[pg.K_RETURN]:
                    waiting = False



g = Game()

g.show_start_screen()
while g.running:
    g.new()
    g.run()
    g.show_game_over_screen()

pygame.quit()