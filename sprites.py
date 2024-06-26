import pygame as pg, pygame
import random
from random import uniform, choice, randint
from settings import *
from tilemap import *
import pytweening as tween
from itertools import chain
vec = pg.math.Vector2
import math

def collide_with_walls(sprite, group, dir):

    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits:
        #tolerance = 2 # Adjusted tolerance value
        #print("Player collided with something!")
        if dir == 'x':
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.vel.x = 0
                sprite.pos.x = hits[0].rect.left  - sprite.hit_rect.width /2 -2 - 1  # Added offset
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.vel.x = 0
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width /2 +2 + 1  # Added offset
            sprite.hit_rect.centerx = sprite.pos.x
        if dir == 'y':
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.vel.y = 0
                sprite.pos.y = hits[0].rect.top    - sprite.hit_rect.height / 2 -2 - 1  # Added offset
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.vel.y = 0
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2 +2 + 1  # Added offset
            sprite.hit_rect.centery = sprite.pos.y
                    
class Player(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.last_shot = 0
        self.health = PLAYER_HEALTH
        self.weapon = 'pistol'
        self.grenade = 'grenade'
        self.damaged = False
        self.has_gun = True
        self.has_shotgun = True
        self.has_flamethrower = True
        self.has_bazooka = True
        self.has_grenade = True
        self.grenade_count = 1
        self.distance = 0


    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if self.distance > 10:
            if mouse[0] or keys[pg.K_w]:
                self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)
        if keys[pg.K_SPACE] or mouse[2]:
            self.shoot()
        # Update player's position based on velocity
        self.pos = (self.pos[0] + self.vel.x, self.pos[1] + self.vel.y)
        
        # Update rectangle's position based on player's position
        self.rect = self.image.get_rect(center=self.pos)
        self.rect = self.game.camera.apply(self)
        if keys[pg.K_1] and self.has_gun == True:
            self.weapon = 'pistol'
            self.game.player_img = self.game.player_img_gun
        if keys[pg.K_2] and self.has_shotgun == True:
            self.weapon = 'shotgun'
            self.game.player_img = self.game.player_img_shotgun
        if keys[pg.K_3] and self.has_flamethrower == True:
            self.weapon = 'flamethrower'
            self.game.player_img = self.game.player_img_flamethrower
        if keys[pg.K_4] and self.has_bazooka == True:
            self.weapon = 'bazooka'
            self.game.player_img = self.game.player_img_bazooka
        if keys[pg.K_e] or mouse[1]:
            self.last_weapon = self.weapon
            self.weapon = 'grenade'
            self.throw_grenade()
            self.weapon = self.last_weapon
            self.last_weapon = None

    def mouse_move(self):
        # Calculate mouse position relative to player position
        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - self.rect.centerx, my - self.rect.centery
        self.distance = math.sqrt(dx**2 + dy**2)       
        self.rot = (180 / math.pi) * -math.atan2(dy, dx)
        self.image = pygame.transform.rotate(self.game.player_img, int(self.rot))
        self.rect = self.image.get_rect(center=self.pos)

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > WEAPONS[self.weapon]['fireing_rate']:
            self.last_shot = now
            dir = vec(1, 0).rotate(-self.rot)
            pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
            self.vel = vec(-WEAPONS[self.weapon]['kickback'], 0).rotate(-self.rot)
            for i in range(WEAPONS[self.weapon]['bullet_count']):
                spread = uniform(-WEAPONS[self.weapon]['gun_spread'], WEAPONS[self.weapon]['gun_spread'])
                if self.weapon == 'bazooka':
                    explosion_size = 200
                    Rocket(self.game, pos, dir.rotate(spread), WEAPONS[self.weapon]['bullet_damage'], explosion_size)
                elif self.weapon == 'flamethrower':
                    explosion_size = 20
                    Flame(self.game, pos, dir.rotate(spread), WEAPONS[self.weapon]['bullet_damage'], explosion_size)
                else:
                    Bullet(self.game, pos, dir.rotate(spread), WEAPONS[self.weapon]['bullet_damage'])
                snd = choice(self.game.weapon_sounds[self.weapon])
                if snd.get_num_channels() > 2:
                    snd.stop()
            snd.play()
            MuzzleFlash(self.game, pos)

    def throw_grenade(self):
        now = pg.time.get_ticks()
        g_explosion_size = 500
        if now - self.last_shot > WEAPONS[self.weapon]['fireing_rate']:
            self.last_shot = now
            dir = vec(1, 0).rotate(-self.rot)
            pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
            self.vel = vec(-WEAPONS[self.weapon]['kickback'], 0).rotate(-self.rot)
            for i in range(WEAPONS[self.weapon]['bullet_count']):
                spread = uniform(-WEAPONS[self.weapon]['gun_spread'], WEAPONS[self.weapon]['gun_spread'])
                if self.grenade == 'grenade' and self.grenade_count > 0:
                    #self.grenade_count -= 1
                    Grenade(self.game, pos, dir.rotate(spread), WEAPONS[self.weapon]['bullet_damage'], g_explosion_size)                
                snd = choice(self.game.weapon_sounds[self.weapon])
                if snd.get_num_channels() > 2:
                    snd.stop()
            snd.play()       

    
        ### MOUSE BUTTON MOVEMENT  ###
        #for event in pg.event.get():
            #if event.type == pg.MOUSEBUTTONDOWN:
                #if event.button == 3:
                    #self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)

    def got_hit(self):
        self.damaged = True
        self.damage_alpha = chain(DAMAGE_ALPHA * 2)
    
    def update(self):
        self.get_keys()
        
        if self.damaged:
            try:
                self.image.fill((255, 0, 0, next(self.damage_alpha)), special_flags=pg.BLEND_RGBA_MULT)
            except:
                self.damaged = False

        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.mouse_move()
        self.rect.center = self.hit_rect.center

    def add_health(self, amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH



class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH
        self.speed = choice(MOB_SPEEDS)
        self.target = game.player
        self.dot_effect = []

    def apply_dot(self, dot_effect):
        self.dot_effect.append(dot_effect)

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        player_dist = self.target.pos - self.pos
        if player_dist.length_squared() < ENGAGE_RADIUS**2:
            if random.random() < 0.002:
                choice(self.game.zombie_moan_sounds).play()
            self.rot = player_dist.angle_to(vec(1, 0))
            self.image = pg.transform.rotate(self.game.mob_img, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(1, 0.01).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 *self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
        # Process DoT effects
        for dot_effect in self.dot_effect[:]:  # Iterate over a copy of the list
            damage = dot_effect.update(self.game.dt)
            if damage:
                self.health -= damage
            if dot_effect.duration <= 0:
                self.dot_effect.remove(dot_effect)  # Remove expired DoT effects
        if self.health <= 0:
            self.kill()
            
    
    def draw_health(self):
        if self.health   > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED

        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0,0, width, 7)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)



class Boss(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs, game.boss
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.boss_level = self.game.current_level
        self.image = game.boss_image[self.boss_level].copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = BOSS[self.boss_level]['boss_hit_rect'].copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.is_boss = True
        self.damaged = False
        self.health = BOSS[self.game.current_level]['boss_health']
        self.speed = BOSS[self.game.current_level]['boss_speed']
        self.target = game.player
        self.dot_effect = []
        

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()
    
    def got_hit(self):
        self.damaged = True
        self.damage_alpha = chain(DAMAGE_ALPHA * 2)

    def apply_dot(self, dot_effect):
        self.dot_effect.append(dot_effect)
    
    
    def update(self):
        player_dist = self.target.pos - self.pos
        if self.damaged:
            try:
                self.image.fill((255, 0, 0, next(self.damage_alpha)), special_flags=pg.BLEND_RGBA_MULT)
            except:
                self.damaged = False
        if player_dist.length_squared() < ENGAGE_RADIUS**20:
            if random.random() < 0.002:
                choice(self.game.zombie_moan_sounds).play()
            self.rot = player_dist.angle_to(vec(1, 0))
            #self.image = pg.transform.rotate(self.game.boss_image[self.game.current_level], self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(1, 0.01).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 *self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
        
            # Process DoT effects
        for dot_effect in self.dot_effect[:]:  # Iterate over a copy of the list
            damage = dot_effect.update(self.game.dt)
            if damage:
                self.health -= damage
            if dot_effect.duration <= 0:
                self.dot_effect.remove(dot_effect)  # Remove expired DoT effects
        
        
        if self.health <= 0:
            choice(self.game.zombie_hit_sounds).play()
            self.kill()
            self.game.map_img.blit(self.game.splat, self.pos - vec(32, 32))
            self.game.score += 200


                   
    

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, damage):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_images[WEAPONS[game.player.weapon]['bullet_size']]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        #spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir * WEAPONS[game.player.weapon]['bullet_speed'] * uniform(0.9, 1.1)
        #self.vel = dir * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()
        self.damage = damage


    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self,self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.weapon]['bullet_lifetime']:
            self.kill()

class Rocket(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, damage, explosion_size):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.explosion_size = explosion_size
        self.image = game.bullet_images[WEAPONS[game.player.weapon]['bullet_size']]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        #spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir * WEAPONS[game.player.weapon]['bullet_speed'] * uniform(0.9, 1.1)
        #self.vel = dir * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()
        self.damage = damage


    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self,self.game.walls):
            ####  ADD EXPLODE HERE   #####
            Explosion(self.game, self.pos, self.explosion_size, self.damage)
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.weapon]['bullet_lifetime']:
            self.kill()

class Flame(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, damage, explosion_size):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.explosion_size = explosion_size
        self.image = game.bullet_images[WEAPONS[game.player.weapon]['bullet_size']]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        #spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir * WEAPONS[game.player.weapon]['bullet_speed'] * uniform(0.9, 1.1)
        #self.vel = dir * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()
        self.damage = damage


    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self,self.game.walls):
            ####  ADD EXPLODE HERE   #####
            Explosion(self.game, self.pos, self.explosion_size, self.damage)
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.weapon]['bullet_lifetime']:
            self.kill()

class Grenade(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, damage, explosion_size):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.explosion_size = explosion_size
        self.image = game.bullet_images[WEAPONS[game.player.weapon]['bullet_size']]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * WEAPONS[game.player.weapon]['bullet_speed'] * uniform(0.9, 1.1)
        self.spawn_time = pg.time.get_ticks()
        self.damage = damage
        self.gravity = 2  # adjust this value to change the arc height
        self.has_exploded = False
        

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.grenade]['grenade_lifetime']:
            self.has_exploded = True
        if self.has_exploded == True:
            Explosion(self.game, self.pos, self.explosion_size, 500)
            self.kill()
            self.has_exploded = False
        self.vel.y += self.gravity  # apply gravity
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        mobs_and_walls = self.game.mobs.copy()
        mobs_and_walls.add(self.game.walls)
        hit = pg.sprite.spritecollideany(self, mobs_and_walls)
        
        if hit:
            # Check which side of the sprite/wall the grenade hit and reverse velocity
            if abs(hit.rect.left - self.rect.right) < 10 and self.vel.x > 0:
                self.vel.x *= -0.25  # reverse and halve the velocity
            if abs(hit.rect.right - self.rect.left) < 10 and self.vel.x < 0:
                self.vel.x *= -0.25  # reverse and halve the velocity
            if abs(hit.rect.top - self.rect.bottom) < 10 and self.vel.y > 0:
                self.vel.y *= -0.25  # reverse and halve the velocity
            if abs(hit.rect.bottom - self.rect.top) < 10 and self.vel.y < 0:
                self.vel.y *= -0.25 # reverse and halve the velocity
            

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class MuzzleFlash(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = randint(20, 50)
        self.image = pg.transform.scale(choice(game.gun_flashes), (size, size))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
           self.kill()

class Explosion(pg.sprite.Sprite):
    def __init__(self, game, pos, size, damage):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = pos
        self.damage = damage
        # Check the player's weapon and adjust the size accordingly
        self.size = size
        self.image = pg.transform.scale(choice(game.gun_flashes), (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > EXPLOSION_DURATION:
            self.kill()


class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self._layer = ITEMS_LAYER
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.type = type
        self.pos = pos
        self.rect.center = pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir  = 1

    def update(self):
        ## bobbing motion
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1


## Sprite Template ##   The basic outline of a sprite object.
class Name(pg.sprite.Sprite):
    def __init__(self, game, ):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface(())
        self.rect = self.image.get_rect()


class DotEffect:
    def __init__(self, game, target, damage_per_tick, duration, tick_rate):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        self.game = game
        self.damage_per_tick = damage_per_tick
        self.duration = duration
        self.tick_rate = tick_rate
        self.elapsed_time = 0
        self.time_since_last_tick = 0
        self.target = target
        

    def apply_damage(self):
        """Apply damage to the target."""
        if self.target.health > 0:  # Check if the target is alive
            self.target.health -= self.damage_per_tick  # Apply damage
            self.effect_position = self.target.rect.center
            #print(f"Applied {self.damage_per_tick} damage to {self.target}. Health is now {self.target.health}.")
            if self.target.health <= 0:  # Check if the target is dead
                pass
    def get_random_position_within_target(self):
        """Generate a random position within the target's rect."""
        random_x = random.randint(self.target.rect.left, self.target.rect.right)
        random_y = random.randint(self.target.rect.top, self.target.rect.bottom)
        return (random_x, random_y)
    
    def update(self, dt):
        """Update the dot effect, applying damage at each tick."""
        self.elapsed_time += dt
        self.time_since_last_tick += dt

        if self.elapsed_time > self.duration:
            self.kill()  # Remove the effect after its duration
        elif self.time_since_last_tick >= self.tick_rate:
            self.apply_damage()  # Apply damage
            random_pos = self.get_random_position_within_target()
            Explosion(self.game, random_pos, 12, 0)
            self.time_since_last_tick = 0  # Reset tick timer


class ZombieBoss(Boss):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.last_spawn = pg.time.get_ticks()  # Initialize last_spawn with the current time
        self.last_throw = 0  # Initialize last_throw with 0 or current time


    def spawn_zombie(self):
        ZombieMob(self.game, self.pos.x, self.pos.y)

    def spawn_zombies_based_on_health(self):
        health_pct = self.health / BOSS[self.game.current_level]['boss_health']
        now = pg.time.get_ticks()

        if health_pct > 0.7:
            if now - self.last_spawn > 8000:  # Every 8 seconds
                for _ in range(2):  # Spawn 2 zombies
                    self.spawn_zombie()
                self.last_spawn = now
        elif health_pct > 0.4:
            if now - self.last_spawn > 6000:  # Every 6 seconds
                for _ in range(3):  # Spawn 3 zombies
                    self.spawn_zombie()
                self.last_spawn = now
        elif health_pct > 0.1:
            if now - self.last_spawn > 4000:  # Every 4 seconds
                for _ in range(4):  # Spawn 4 zombies
                    self.spawn_zombie()
                self.last_spawn = now
        else:
            if now - self.last_spawn > 2000:  # Every 2 seconds
                for _ in range(5):  # Spawn 5 zombies
                    self.spawn_zombie()
                self.last_spawn = now
    
    def throw_zombie_at_player(self):
        now = pg.time.get_ticks()
        if now - self.last_throw > 9000:  # 9 seconds = 9000 milliseconds
            player_pos = self.target.pos
            mob_pos = self.pos
            mob_to_player = player_pos - mob_pos
            distance_to_player = mob_to_player.length()
            
            if distance_to_player < THROW_RANGE:
                # Launch the zombie towards the player
                mob_to_player.normalize_ip()
                mob_velocity = mob_to_player * THROW_SPEED
                # Create a new zombie at the current position
                new_mob = ZombieMob(self.game, mob_pos.x, mob_pos.y)
                # Set the velocity of the new zombie
                new_mob.vel = mob_velocity
                self.last_throw = now  # Update the last_throw time

    def update(self):
        super().update()
        self.throw_zombie_at_player()
        self.spawn_zombies_based_on_health()

class ScorpionBoss(Boss):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs, game.boss
        super().__init__(game, x, y)

    def update(self):
        super().update()

class RobotBoss(Boss):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs, game.boss
        super().__init__(game, x, y)

    def update(self):
        super().update()

class AirportBot(Boss):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs, game.boss
        super().__init__(game, x, y)

    def update(self):
        super().update()

class BusDriver(Boss):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs, game.boss
        super().__init__(game, x, y)

    def update(self):
        super().update()
# Define the LEVEL_BOSS mapping with lambda functions
LEVEL_BOSS = {
    1: lambda game, x, y: ZombieBoss(game, x, y),
    2: lambda game, x, y: ScorpionBoss(game, x, y),
    3: lambda game, x, y: RobotBoss(game, x, y),
    4: lambda game, x, y: AirportBot(game, x, y),
    5: lambda game, x, y: BusDriver(game, x, y),
    # Continue mapping for other levels as needed
}        


class ZombieMob(Mob):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        super().__init__(game, x, y)
        self.engaged = False  # Initialize engaged state
        self.lunge_cooldown = 3000  # Cooldown time in milliseconds
        self.last_lunge_time = 0  # Track the last lunge time
        self.lunge_pause_duration = 500  # Pause for 500ms after lunging
        self.is_lunging = False  # Indicates if currently in lunge-pause state

    def zombie_lunge(self):
        current_time = pygame.time.get_ticks()
        if self.is_lunging:
            # If in lunging state, check if it's time to reset velocity
            if current_time - self.last_lunge_time > self.lunge_pause_duration:
                self.vel = vec(0, 0)  # Stop moving after lunge pause
                self.is_lunging = False  # Reset lunging state
        else:
            # Check if cooldown has elapsed and it's time to lunge
            if current_time - self.last_lunge_time > self.lunge_cooldown:
                player_pos = self.target.pos
                mob_pos = self.pos
                mob_to_player = player_pos - mob_pos
                distance_to_player = mob_to_player.length()
                if distance_to_player < 200:
                    mob_to_player.normalize_ip()
                    mob_velocity = mob_to_player * 200
                    self.vel = mob_velocity
                    self.last_lunge_time = current_time
                    self.is_lunging = True  # Enter lunging state
        

    def update(self):
        super().update()
        self.zombie_lunge()
        self.pos += self.vel * self.game.dt
        player_dist = self.target.pos - self.pos
        if player_dist.length_squared() < ENGAGE_RADIUS**2:
            if random.random() < 0.002:
                choice(self.game.zombie_moan_sounds).play()
            self.rot = player_dist.angle_to(vec(1, 0))
            self.image = pg.transform.rotate(self.game.mob_img, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(1, 0.01).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 *self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
        if self.health <= 0:
            choice(self.game.zombie_hit_sounds).play()
            self.game.map_img.blit(self.game.splat, self.pos - vec(32, 32))
            self.kill()
            self.game.score += 50

class ScorpionMob(Mob):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs, game.boss
        super().__init__(game, x, y)

    def update(self):
        super().update()

class RobotMob(Mob):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs, game.boss
        super().__init__(game, x, y)

    def update(self):
        super().update()
