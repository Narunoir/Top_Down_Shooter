import pygame as pg, pygame
import random
from random import uniform, choice, randint
from settings import *
from tilemap import *
import pytweening as tween
from itertools import chain
import math
from pygame.math import Vector2
from talents import build_weapons


def collide_with_walls(sprite, group, dir):
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if not hits:
        return

    wall = hits[0]

    if dir == 'x':
        if sprite.vel.x > 0:  # moving right
            overlap = sprite.hit_rect.right - wall.rect.left
            sprite.hit_rect.right -= overlap
        elif sprite.vel.x < 0:  # moving left
            overlap = wall.rect.right - sprite.hit_rect.left
            sprite.hit_rect.left += overlap
        sprite.vel.x = 0

    elif dir == 'y':
        if sprite.vel.y > 0:  # moving down
            overlap = sprite.hit_rect.bottom - wall.rect.top
            sprite.hit_rect.bottom -= overlap
        elif sprite.vel.y < 0:  # moving up
            overlap = wall.rect.bottom - sprite.hit_rect.top
            sprite.hit_rect.top += overlap
        sprite.vel.y = 0



class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__(game.all_sprites)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect(center=(x, y))
        self.hit_rect = PLAYER_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.rot = 0

        self.health = PLAYER_HEALTH
        self.weapon = 'pistol'
        self.grenade = 'grenade'
        self.has_weapons = {
            'pistol': True,
            'shotgun': True,
            'flamethrower': True,
            'bazooka': True,
            'grenade': True
        }
        self.weapon_images = {
            'pistol': game.player_img_gun,
            'shotgun': game.player_img_shotgun,
            'flamethrower': game.player_img_flamethrower,
            'bazooka': game.player_img_bazooka
        }

        self.grenade_count = 1
        self.last_shot = 0
        self.dot_effect = []
        self.distance = 0
        self.damaged = False
        self.is_stunned = False
        self.stun_start_time = 0
        self.stun_timer = 0
        self.last_vibration_time = 0
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        mouse = pg.mouse.get_pressed()

        if (mouse[0] or keys[pg.K_w]):
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)

        if keys[pg.K_SPACE] or mouse[2]:
            self.shoot()

        weapon_keys = {pg.K_1: 'pistol', pg.K_2: 'shotgun', pg.K_3: 'flamethrower', pg.K_4: 'bazooka'}
        for k, name in weapon_keys.items():
            if keys[k] and self.has_weapons[name]:
                self.weapon = name
                self.game.player_img = self.weapon_images[name]

        if keys[pg.K_e] or mouse[1]:
            if self.has_weapons['grenade']:
                last = self.weapon
                self.weapon = 'grenade'
                self.throw_grenade()
                self.weapon = last

    def shoot(self):
        if self.is_stunned:
            return

        # Get weapon stats with talent modifiers applied
        weapons = build_weapons()
        weapon_stats = weapons[self.weapon]

        now = pg.time.get_ticks()
        if now - self.last_shot < weapon_stats['fireing_rate']:
            return
        self.last_shot = now
        dir = vec(1, 0).rotate(-self.rot)
        pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
        self.vel = vec(-weapon_stats['kickback'], 0).rotate(-self.rot)

        for _ in range(weapon_stats['bullet_count']):
            spread = uniform(-weapon_stats['gun_spread'], weapon_stats['gun_spread'])
            angle = dir.rotate(spread)
            damage = weapon_stats['bullet_damage']

            if self.weapon == 'bazooka':
                explosion_size = weapon_stats.get('explosion_size', 200)
                Rocket(self.game, pos, angle, damage, explosion_size)
            elif self.weapon == 'flamethrower':
                Flame(self.game, pos, angle, damage, 20)
            else:
                Bullet(self.game, pos, angle, damage)

        snd = choice(self.game.weapon_sounds[self.weapon])
        if snd.get_num_channels() > 2:
            snd.stop()
        snd.play()
        MuzzleFlash(self.game, pos)

    def throw_grenade(self):
        if self.grenade_count <= 0:
            return

        # Get weapon stats with talent modifiers applied
        weapons = build_weapons()
        grenade_stats = weapons['grenade']

        now = pg.time.get_ticks()
        if now - self.last_shot < grenade_stats['fireing_rate']:
            return
        self.last_shot = now

        dir = vec(1, 0).rotate(-self.rot)
        pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
        self.vel = vec(-grenade_stats['kickback'], 0).rotate(-self.rot)

        explosion_size = grenade_stats.get('explosion_size', 500)
        for _ in range(grenade_stats['bullet_count']):
            spread = uniform(-grenade_stats['gun_spread'], grenade_stats['gun_spread'])
            angle = dir.rotate(spread)
            Grenade(self.game, pos, angle, grenade_stats['grenade_damage'], explosion_size)

        snd = choice(self.game.weapon_sounds[self.weapon])
        if snd.get_num_channels() > 2:
            snd.stop()
        snd.play()
        self.grenade_count -= 1

    def apply_dot(self, dot_effect):
        self.dot_effect.append(dot_effect)

    def got_hit(self):
        self.damaged = True
        self.damage_alpha = chain(DAMAGE_ALPHA * 2)

    def stunned_effect(self):
        now = pg.time.get_ticks()
        if self.stun_timer > now:
            self.vel = vec(0, 0)
            self.vibration()
        else:
            self.is_stunned = False
            self.stun_timer = 0

    def move_and_collide(self, dt=None):
        if dt is None:
            dt = self.game.dt

        # --- X axis ---
        self.pos.x += self.vel.x * dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.pos.x = self.hit_rect.centerx

        # --- Y axis ---
        self.pos.y += self.vel.y * dt
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.pos.y = self.hit_rect.centery

        # --- Mouse rotation ---
        mx, my = pg.mouse.get_pos()
        cam_x, cam_y = self.game.camera.camera.topleft
        world_mx = mx - cam_x
        world_my = my - cam_y

        dx, dy = world_mx - self.pos.x, world_my - self.pos.y
        self.distance = math.hypot(dx, dy)

        if self.distance > ROTATE_DEADZONE:
            self.rot = math.degrees(-math.atan2(dy, dx))

        # --- Rotate image and update rect ---
        rotated_img = pg.transform.rotate(self.game.player_img, int(self.rot))
        self.image = rotated_img
        self.rect = rotated_img.get_rect(center=(self.pos.x, self.pos.y))


    def vibration(self):
        offset = 10 * (self.tween(self.step / 10) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += 3.5
        if self.step > 10:
            self.step = 0
            self.dir *= -1
            self.move_and_collide()

    def add_health(self, amount):
        self.health = min(self.health + amount, PLAYER_HEALTH)

    def update(self):
        if self.is_stunned:
            self.stunned_effect()
            return

        # 1. Input & velocity
        self.get_keys()

        # 2. Movement, collision, and rotation (all in one place now)
        self.move_and_collide()

        # 3. Damage flash (if any)
        if self.damaged:
            try:
                alpha = next(self.damage_alpha)
                self.image.fill((255, 0, 0, alpha),
                                special_flags=pg.BLEND_RGBA_MULT)
            except StopIteration:
                self.damaged = False       




class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y, mob_type, map_obj=None, player=None, wall_group=None):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        super().__init__(game.all_sprites, game.mobs, self.groups)
        map_obj    = map_obj    or game.map
        player     = player     or game.player
        wall_group = wall_group or game.walls

        self._hp_bar_surf = pg.Surface((1, 7)).convert_alpha()
        self.game      = game
        self.base_img  = game.mob_img[mob_type]
        self.image     = self.base_img.copy()
        self.rect      = self.image.get_rect(center=(x, y))
        self.hit_rect  = self.rect.copy()

        self.pos       = Vector2(x, y)
        self.vel       = Vector2(0, 0)
        self.acc       = Vector2(0, 0)
        self.rot       = 0

        self.mob_type  = mob_type
        self.health    = MOB_HEALTH
        self.speed     = choice(MOB_SPEEDS)
        self.target    = game.player
        self.grid      = game.map.grid
        self.wall_group= game.walls
        self.dot_effect= []
        self.spawn_id  = None  # Will be set by main.py to track this mob
        # Pre-generate rotated images (optional)
        self.rot_images = {
            angle: pg.transform.rotate(self.base_img, angle)
            for angle in range(0, 360, 22)
        }

    def apply_dot(self, dot):
        self.dot_effect.append(dot)

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob is not self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        dt = self.game.dt

        # Detection and movement
        target_dist = self.target.pos - self.pos
        if target_dist.length_squared() < ENGAGE_RADIUS**2:
            if random.random() < 0.002:
                choice(self.game.zombie_moan_sounds).play()

            # Rotate toward player
            self.rot = target_dist.angle_to(Vector2(1, 0))
            self.image = self.rot_images.get(int(self.rot), self.base_img)

            # Acceleration toward player
            self.acc = target_dist.normalize() * self.speed - self.vel
            self.vel += self.acc * dt

            # --- X axis movement ---
            self.pos.x += self.vel.x * dt
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.wall_group, 'x')
            self.pos.x = self.hit_rect.centerx

            # --- Y axis movement ---
            self.pos.y += self.vel.y * dt
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.wall_group, 'y')
            self.pos.y = self.hit_rect.centery

            # Sync draw rect
            self.rect.center = self.hit_rect.center

        # Process DoT in-place
        for i in reversed(range(len(self.dot_effect))):
            dmg = self.dot_effect[i].update(dt)
            self.health -= dmg or 0
            if self.dot_effect[i].duration <= 0:
                self.dot_effect.pop(i)

        # Death check
        if self.health <= 0:
            # Track killed mob to prevent respawn on load
            if hasattr(self, 'spawn_id') and self.spawn_id:
                self.game.killed_mobs.add(self.spawn_id)
            self.kill()
            self.game.score += 50
            self.game.exp += MOB_EXP
            self.game.kill_count += 1

    def draw_health(self):
        if self.health >= MOB_HEALTH:
            return
        width = max(0,int(self.rect.width * self.health / MOB_HEALTH))
        col   = GREEN if self.health>60 else YELLOW if self.health>30 else RED
        self._hp_bar_surf.fill(col)
        hp_surf = pg.transform.scale(self._hp_bar_surf, (width, 7))
        self.image.blit(hp_surf, (0, 0))


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
        self.spawn_id = None  # Will be set by main.py to track this boss
        

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

    def face_player(self):
        player_dist = self.target.pos - self.pos
        self.rot = player_dist.angle_to(vec(1, 0))    
        self.image = pg.transform.rotate(self.game.boss_image[self.boss_level], self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
    
    
    
    def update(self):
        player_dist = self.target.pos - self.pos
        if self.damaged:
            try:
                self.image.fill((255, 0, 0, next(self.damage_alpha)), special_flags=pg.BLEND_RGBA_MULT)
            except:
                self.damaged = False
        if player_dist.length_squared() < ENGAGE_RADIUS**2:  # Adjusted exponent to 2 for a realistic radius
            if random.random() < 0.002:
                choice(self.game.zombie_moan_sounds).play()
            self.face_player()  # Call the new method to face the player
            self.acc = vec(1, 0.01).rotate(-self.rot)
            self.acc.scale_to_length(self.speed)
            self.avoid_mobs()
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.pos.xy
        
            # Process DoT effects
        for dot_effect in self.dot_effect[:]:  # Iterate over a copy of the list
            damage = dot_effect.update(self.game.dt)
            if damage:
                self.health -= damage
            if dot_effect.duration <= 0:
                self.dot_effect.remove(dot_effect)  # Remove expired DoT effects
        
        
        if self.health <= 0:
            # Track killed boss to prevent respawn on load
            if hasattr(self, 'spawn_id') and self.spawn_id:
                self.game.killed_mobs.add(self.spawn_id)
            choice(self.game.zombie_hit_sounds).play()
            self.kill()
            self.game.map_img.blit(self.game.splat, self.pos - vec(32, 32))
            self.game.score += 200
            self.game.exp += BOSS[self.game.current_level]['boss_exp']
            self.game.kill_count += 1


                   
    

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, damage):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # Get modified weapon stats
        weapons = build_weapons()
        weapon_stats = weapons[game.player.weapon]

        self.image = game.bullet_images[weapon_stats['bullet_image']]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * weapon_stats['bullet_speed'] * uniform(0.9, 1.1)
        self.spawn_time = pg.time.get_ticks()
        self.damage = damage
        self.bullet_lifetime = weapon_stats['bullet_lifetime']


    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self,self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > self.bullet_lifetime:
            self.kill()

class Rocket(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, damage, explosion_size):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.explosion_size = explosion_size

        # Get modified weapon stats
        weapons = build_weapons()
        weapon_stats = weapons['bazooka']

        self.image = game.bullet_images[weapon_stats['bullet_image']]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * weapon_stats['bullet_speed'] * uniform(0.9, 1.1)
        self.spawn_time = pg.time.get_ticks()
        self.damage = damage
        self.bullet_lifetime = weapon_stats['bullet_lifetime']


    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self,self.game.walls):
            Explosion(self.game, self.pos, self.explosion_size, self.damage)
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > self.bullet_lifetime:
            self.kill()

class Flame(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, damage, explosion_size):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.explosion_size = explosion_size

        # Get modified weapon stats
        weapons = build_weapons()
        weapon_stats = weapons['flamethrower']

        self.image = game.bullet_images[weapon_stats['bullet_image']]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * weapon_stats['bullet_speed'] * uniform(0.9, 1.1)
        self.spawn_time = pg.time.get_ticks()
        self.damage = damage
        self.bullet_lifetime = weapon_stats['bullet_lifetime']
        # Store DoT stats for application on hit
        self.dot_damage = weapon_stats.get('dot_damage', 1.25)
        self.dot_duration = weapon_stats.get('dot_duration', 30000)


    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self,self.game.walls):
            Explosion(self.game, self.pos, self.explosion_size, self.damage)
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > self.bullet_lifetime:
            self.kill()

class Grenade(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, damage, explosion_size):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.explosion_size = explosion_size

        # Get modified weapon stats
        weapons = build_weapons()
        grenade_stats = weapons['grenade']

        self.image = game.bullet_images[grenade_stats['bullet_image']]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * grenade_stats['bullet_speed'] * uniform(0.9, 1.1)
        self.spawn_time = pg.time.get_ticks()
        self.damage = damage
        self.gravity = 2  # adjust this value to change the arc height
        self.has_exploded = False
        self.grenade_lifetime = grenade_stats['grenade_lifetime']


    def update(self):
        if pg.time.get_ticks() - self.spawn_time > self.grenade_lifetime:
            self.has_exploded = True
        if self.has_exploded == True:
            Explosion(self.game, self.pos, self.explosion_size, self.damage)
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
        self.hit_rect = self.rect
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
        self.hit_rect = self.rect
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
        self.hit_rect = self.rect
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
        self.hit_rect = self.rect

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
        self.hit_rect = self.rect
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
        self.groups = game.all_sprites, game.bullets, game.mob_bullets
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
            self.duration = 0  # Mark as expired so parent can remove it
            return None
        elif self.time_since_last_tick >= self.tick_rate:
            self.apply_damage()  # Apply damage
            random_pos = self.get_random_position_within_target()
            Explosion(self.game, random_pos, 12, 0)
            self.time_since_last_tick = 0  # Reset tick timer
            return self.damage_per_tick
        return None


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
        self.last_shot = 0

    def spit_poison(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > 3000:  
            player_pos = self.target.pos
            mob_pos = self.pos
            mob_to_player = player_pos - mob_pos
            distance_to_player = mob_to_player.length()
            #dir = vec(1, 0).rotate(-self.rot)
            
            if distance_to_player < THROW_RANGE:
                # Launch the poison ball towards the player
                mob_to_player.normalize_ip()
                mob_velocity = mob_to_player * THROW_SPEED
                # Create a new poison ball at the current position
                new_poison_ball = PoisonBall(self.game, mob_pos, 0, mob_velocity)
                # Set the velocity of the new poison ball
                new_poison_ball.vel = mob_velocity
                self.last_shot = now  # Update the last_shot time

    def update(self):
        super().update()
        self.spit_poison()

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

class DirewolfBoss(Boss):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs, game.boss
        super().__init__(game, x, y)
        self.bite_cooldown = 1500
        self.last_bite = 0
        self.claw_cooldown = 1000
        self.last_claw = 0
        self.maul_cooldown = 8000
        self.last_maul = 0
        self.maul_flash_count = 0
        self.maul_flash_timer = 0
        self.is_maul_leaping = False
        self.stun_duration = 1500

    def bite_attack(self):
        now = pg.time.get_ticks()
        if now - self.last_bite > self.bite_cooldown:
            player_dist = self.target.pos - self.pos
            if player_dist.length() < 80:
                self.target.health -= 40  # Bite damage
                self.last_bite = now

    def claw_attack(self):
        now = pg.time.get_ticks()
        if now - self.last_claw > self.claw_cooldown:
            player_dist = self.target.pos - self.pos
            if player_dist.length() < 100:
                self.target.health -= 20  # Claw damage
                self.last_claw = now

    def maul_attack(self):
        now = pg.time.get_ticks()
        if now - self.last_maul > self.maul_cooldown:
            # Start flashing red
            self.maul_flash_count = 0
            self.maul_flash_timer = now
            self.last_maul = now

    def update_maul(self):
        now = pg.time.get_ticks()
        if self.maul_flash_count < 2:
            if now - self.maul_flash_timer > 500:
                self.maul_flash_count += 1
                self.maul_flash_timer = now
                # Flash red
                self.image.fill((255, 0, 0, 128), special_flags=pg.BLEND_RGBA_MULT)
        elif not self.is_maul_leaping:
            # Leap at player
            player_pos = self.target.pos
            direction = (player_pos - self.pos).normalize()
            self.vel = direction * 600  # Leap speed
            self.is_maul_leaping = True
        else:
            # Check if hit player
            if pg.sprite.collide_rect(self, self.target):
                self.target.health -= 100  # Maul damage (20x5)
                # Stun player
                self.target.is_stunned = True
                self.target.stun_timer = now + self.stun_duration
                self.is_maul_leaping = False
                self.vel = vec(0, 0)

    def update(self):
        super().update()
        if self.maul_flash_count > 0 and self.maul_flash_count < 3:
            self.update_maul()
        else:
            self.bite_attack()
            self.claw_attack()
            self.maul_attack()
            player_dist = self.target.pos - self.pos
            if player_dist.length_squared() < ENGAGE_RADIUS**2:
                if random.random() < 0.002:
                    choice(self.game.zombie_moan_sounds).play()
                self.rot = player_dist.angle_to(vec(1, 0))
                self.image = pg.transform.rotate(self.game.boss_image[self.boss_level], self.rot)
                self.rect = self.image.get_rect()
                self.rect.center = self.hit_rect.center

# ==== NEW BOSS CLASSES FOR LEVELS 6-20 ====

class SewerMonster(Boss):
    """Level 6 Boss - Poison spray, summon rats, acid pool, toxic cloud"""
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.poison_spray_cooldown = 3000
        self.last_poison_spray = 0
        self.acid_pool_cooldown = 8000
        self.last_acid_pool = 0
        self.toxic_cloud_cooldown = 12000
        self.last_toxic_cloud = 0
        self.rat_summon_cooldown = 10000
        self.last_rat_summon = 0

    def poison_spray(self):
        now = pg.time.get_ticks()
        if now - self.last_poison_spray > self.poison_spray_cooldown:
            direction = (self.target.pos - self.pos).normalize()
            for i in range(5):  # Spray 5 poison balls in a cone
                spread_angle = random.uniform(-30, 30)
                spread_dir = direction.rotate(spread_angle)
                PoisonBall(self.game, self.pos, 0, spread_dir * THROW_SPEED)
            self.last_poison_spray = now

    def summon_rats(self):
        now = pg.time.get_ticks()
        if now - self.last_rat_summon > self.rat_summon_cooldown:
            for _ in range(3):
                offset = vec(random.randint(-100, 100), random.randint(-100, 100))
                ZombieMob(self.game, self.pos.x + offset.x, self.pos.y + offset.y)
            self.last_rat_summon = now

    def acid_pool(self):
        now = pg.time.get_ticks()
        if now - self.last_acid_pool > self.acid_pool_cooldown:
            # Create acid puddle at player location
            PoisonPuddle(self.game, self.target.pos, 200)
            self.last_acid_pool = now

    def toxic_cloud(self):
        now = pg.time.get_ticks()
        if now - self.last_toxic_cloud > self.toxic_cloud_cooldown:
            # Damage player if in range
            if (self.target.pos - self.pos).length() < 300:
                self.target.health -= 30
            self.last_toxic_cloud = now

    def update(self):
        super().update()
        self.poison_spray()
        self.summon_rats()
        self.acid_pool()
        self.toxic_cloud()


class MountainTroll(Boss):
    """Level 7 Boss - Boulder throw, ground slam, rock armor, avalanche"""
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.boulder_cooldown = 4000
        self.last_boulder = 0
        self.slam_cooldown = 7000
        self.last_slam = 0
        self.armor_cooldown = 15000
        self.last_armor = 0
        self.avalanche_cooldown = 20000
        self.last_avalanche = 0
        self.armor_active = False

    def boulder_throw(self):
        now = pg.time.get_ticks()
        if now - self.last_boulder > self.boulder_cooldown:
            direction = (self.target.pos - self.pos).normalize()
            PoisonBall(self.game, self.pos, 0, direction * THROW_SPEED)  # Reuse for boulder
            self.last_boulder = now

    def ground_slam(self):
        now = pg.time.get_ticks()
        if now - self.last_slam > self.slam_cooldown:
            if (self.target.pos - self.pos).length() < 200:
                self.target.health -= 50
                # Knockback
                direction = (self.target.pos - self.pos).normalize()
                self.target.vel = direction * 300
            self.last_slam = now

    def rock_armor(self):
        now = pg.time.get_ticks()
        if now - self.last_armor > self.armor_cooldown:
            self.armor_active = True
            self.speed = 50  # Slow down
            self.last_armor = now
            # Armor lasts 5 seconds, damage reduced

    def avalanche(self):
        now = pg.time.get_ticks()
        if now - self.last_avalanche > self.avalanche_cooldown:
            # Multiple boulders in all directions
            for angle in range(0, 360, 45):
                direction = vec(1, 0).rotate(angle)
                PoisonBall(self.game, self.pos, 0, direction * THROW_SPEED * 0.7)
            self.last_avalanche = now

    def update(self):
        super().update()
        self.boulder_throw()
        self.ground_slam()
        self.rock_armor()
        self.avalanche()


class Necromancer(Boss):
    """Level 9 Boss - Summon zombies, life drain, dark curse, soul explosion"""
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.summon_cooldown = 5000
        self.last_summon = 0
        self.drain_cooldown = 3000
        self.last_drain = 0
        self.curse_cooldown = 10000
        self.last_curse = 0
        self.explosion_cooldown = 15000
        self.last_explosion = 0

    def summon_undead(self):
        now = pg.time.get_ticks()
        if now - self.last_summon > self.summon_cooldown:
            for _ in range(4):
                offset = vec(random.randint(-150, 150), random.randint(-150, 150))
                ZombieMob(self.game, self.pos.x + offset.x, self.pos.y + offset.y)
            self.last_summon = now

    def life_drain(self):
        now = pg.time.get_ticks()
        if now - self.last_drain > self.drain_cooldown:
            if (self.target.pos - self.pos).length() < 400:
                drain_amount = 25
                self.target.health -= drain_amount
                self.health += drain_amount  # Heal self
            self.last_drain = now

    def dark_curse(self):
        now = pg.time.get_ticks()
        if now - self.last_curse > self.curse_cooldown:
            # Slow player for 5 seconds
            if (self.target.pos - self.pos).length() < 500:
                self.target.vel *= 0.5
            self.last_curse = now

    def soul_explosion(self):
        now = pg.time.get_ticks()
        if now - self.last_explosion > self.explosion_cooldown:
            # Large AoE explosion
            if (self.target.pos - self.pos).length() < 350:
                self.target.health -= 80
            Explosion(self.game, self.pos, 400, 0)
            self.last_explosion = now

    def update(self):
        super().update()
        self.summon_undead()
        self.life_drain()
        self.dark_curse()
        self.soul_explosion()


class ToxicAbomination(Boss):
    """Level 10 Boss - Toxic cloud, mutation surge, poison wave, sludge bomb"""
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.cloud_cooldown = 4000
        self.last_cloud = 0
        self.surge_cooldown = 10000
        self.last_surge = 0
        self.wave_cooldown = 7000
        self.last_wave = 0
        self.bomb_cooldown = 5000
        self.last_bomb = 0

    def toxic_cloud_attack(self):
        now = pg.time.get_ticks()
        if now - self.last_cloud > self.cloud_cooldown:
            if (self.target.pos - self.pos).length() < 250:
                self.target.health -= 20
                # Apply DoT
                dot = DotEffect(self.game, self.target, 5, 3000, 1.0)
                self.target.apply_dot(dot)
            self.last_cloud = now

    def mutation_surge(self):
        now = pg.time.get_ticks()
        if now - self.last_surge > self.surge_cooldown:
            # Temporarily increase stats
            self.speed = 150
            self.damage = 80
            self.last_surge = now

    def poison_wave_attack(self):
        now = pg.time.get_ticks()
        if now - self.last_wave > self.wave_cooldown:
            # 360 degree poison wave
            for angle in range(0, 360, 30):
                direction = vec(1, 0).rotate(angle)
                PoisonBall(self.game, self.pos, 0, direction * 400)
            self.last_wave = now

    def sludge_bomb(self):
        now = pg.time.get_ticks()
        if now - self.last_bomb > self.bomb_cooldown:
            direction = (self.target.pos - self.pos).normalize()
            PoisonBall(self.game, self.pos, 0, direction * THROW_SPEED)
            self.last_bomb = now

    def update(self):
        super().update()
        self.toxic_cloud_attack()
        self.mutation_surge()
        self.poison_wave_attack()
        self.sludge_bomb()


class CyberSpiderQueen(Boss):
    """Level 11 Boss - Web trap, electric shock, spawn spiderlings, cyber hack"""
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.web_cooldown = 6000
        self.last_web = 0
        self.shock_cooldown = 3000
        self.last_shock = 0
        self.spawn_cooldown = 8000
        self.last_spawn = 0
        self.hack_cooldown = 12000
        self.last_hack = 0

    def web_trap(self):
        now = pg.time.get_ticks()
        if now - self.last_web > self.web_cooldown:
            # Trap player, slow them
            if (self.target.pos - self.pos).length() < 300:
                self.target.is_stunned = True
                self.target.stun_timer = now + 2000
            self.last_web = now

    def electric_shock(self):
        now = pg.time.get_ticks()
        if now - self.last_shock > self.shock_cooldown:
            if (self.target.pos - self.pos).length() < 200:
                self.target.health -= 40
            self.last_shock = now

    def spawn_spiderlings(self):
        now = pg.time.get_ticks()
        if now - self.last_spawn > self.spawn_cooldown:
            for _ in range(3):
                offset = vec(random.randint(-100, 100), random.randint(-100, 100))
                ScorpionMob(self.game, self.pos.x + offset.x, self.pos.y + offset.y)
            self.last_spawn = now

    def cyber_hack(self):
        now = pg.time.get_ticks()
        if now - self.last_hack > self.hack_cooldown:
            # Disable player weapon briefly
            if (self.target.pos - self.pos).length() < 400:
                self.target.is_stunned = True
                self.target.stun_timer = now + 3000
            self.last_hack = now

    def update(self):
        super().update()
        self.web_trap()
        self.electric_shock()
        self.spawn_spiderlings()
        self.cyber_hack()


class FireElemental(Boss):
    """Level 12 Boss - Fireball barrage, lava eruption, flame aura, meteor strike"""
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.barrage_cooldown = 4000
        self.last_barrage = 0
        self.eruption_cooldown = 8000
        self.last_eruption = 0
        self.aura_cooldown = 2000
        self.last_aura = 0
        self.meteor_cooldown = 15000
        self.last_meteor = 0

    def fireball_barrage(self):
        now = pg.time.get_ticks()
        if now - self.last_barrage > self.barrage_cooldown:
            for i in range(8):
                direction = (self.target.pos - self.pos).normalize().rotate(random.uniform(-20, 20))
                PoisonBall(self.game, self.pos, 0, direction * THROW_SPEED)
            self.last_barrage = now

    def lava_eruption(self):
        now = pg.time.get_ticks()
        if now - self.last_eruption > self.eruption_cooldown:
            # Create explosion at player feet
            Explosion(self.game, self.target.pos, 250, 60)
            self.last_eruption = now

    def flame_aura(self):
        now = pg.time.get_ticks()
        if now - self.last_aura > self.aura_cooldown:
            # Constant damage to nearby player
            if (self.target.pos - self.pos).length() < 150:
                self.target.health -= 10
            self.last_aura = now

    def meteor_strike(self):
        now = pg.time.get_ticks()
        if now - self.last_meteor > self.meteor_cooldown:
            # Massive explosion
            Explosion(self.game, self.target.pos, 400, 100)
            self.last_meteor = now

    def update(self):
        super().update()
        self.fireball_barrage()
        self.lava_eruption()
        self.flame_aura()
        self.meteor_strike()


class IceGolem(Boss):
    """Level 13 Boss - Ice spikes, blizzard storm, freeze ray, glacier crash"""
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.spikes_cooldown = 5000
        self.last_spikes = 0
        self.blizzard_cooldown = 10000
        self.last_blizzard = 0
        self.freeze_cooldown = 7000
        self.last_freeze = 0
        self.crash_cooldown = 15000
        self.last_crash = 0

    def ice_spikes(self):
        now = pg.time.get_ticks()
        if now - self.last_spikes > self.spikes_cooldown:
            # Line of spikes toward player
            direction = (self.target.pos - self.pos).normalize()
            for i in range(5):
                spike_pos = self.pos + direction * (i * 50)
                Explosion(self.game, spike_pos, 100, 30)
            self.last_spikes = now

    def blizzard_storm(self):
        now = pg.time.get_ticks()
        if now - self.last_blizzard > self.blizzard_cooldown:
            # Slow all movement and damage
            if (self.target.pos - self.pos).length() < 500:
                self.target.health -= 50
                # Slow player
                self.target.vel *= 0.3
            self.last_blizzard = now

    def freeze_ray(self):
        now = pg.time.get_ticks()
        if now - self.last_freeze > self.freeze_cooldown:
            # Stun player briefly
            if (self.target.pos - self.pos).length() < 400:
                self.target.is_stunned = True
                self.target.stun_timer = now + 2500
            self.last_freeze = now

    def glacier_crash(self):
        now = pg.time.get_ticks()
        if now - self.last_crash > self.crash_cooldown:
            # Huge AoE
            if (self.target.pos - self.pos).length() < 450:
                self.target.health -= 90
            Explosion(self.game, self.pos, 500, 0)
            self.last_crash = now

    def update(self):
        super().update()
        self.ice_spikes()
        self.blizzard_storm()
        self.freeze_ray()
        self.glacier_crash()


class ShadowAssassin(Boss):
    """Level 14 Boss - Shadow step, blade dance, darkness cloak, assassination strike"""
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.step_cooldown = 5000
        self.last_step = 0
        self.dance_cooldown = 4000
        self.last_dance = 0
        self.cloak_cooldown = 12000
        self.last_cloak = 0
        self.assassinate_cooldown = 20000
        self.last_assassinate = 0
        self.is_cloaked = False

    def shadow_step(self):
        now = pg.time.get_ticks()
        if now - self.last_step > self.step_cooldown:
            # Teleport behind player
            direction = (self.target.pos - self.pos).normalize()
            self.pos = self.target.pos - direction * 100
            self.last_step = now

    def blade_dance(self):
        now = pg.time.get_ticks()
        if now - self.last_dance > self.dance_cooldown:
            # Rapid strikes
            if (self.target.pos - self.pos).length() < 120:
                for _ in range(5):
                    self.target.health -= 15
            self.last_dance = now

    def darkness_cloak(self):
        now = pg.time.get_ticks()
        if now - self.last_cloak > self.cloak_cooldown:
            self.is_cloaked = True
            self.speed = 250  # Super fast when cloaked
            self.last_cloak = now
            # Cloak lasts 3 seconds

    def assassination_strike(self):
        now = pg.time.get_ticks()
        if now - self.last_assassinate > self.assassinate_cooldown:
            # Massive critical hit
            if (self.target.pos - self.pos).length() < 150:
                self.target.health -= 150
            self.last_assassinate = now

    def update(self):
        super().update()
        self.shadow_step()
        self.blade_dance()
        self.darkness_cloak()
        self.assassination_strike()


class MutantBrute(Boss):
    """Level 15 Boss - Berserker rage, ground pound, throw debris, regeneration"""
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.rage_cooldown = 10000
        self.last_rage = 0
        self.pound_cooldown = 6000
        self.last_pound = 0
        self.throw_cooldown = 4000
        self.last_throw = 0
        self.regen_cooldown = 8000
        self.last_regen = 0
        self.enraged = False

    def berserker_rage(self):
        now = pg.time.get_ticks()
        if now - self.last_rage > self.rage_cooldown:
            self.enraged = True
            self.speed = 180
            self.damage = 120
            self.last_rage = now

    def ground_pound_attack(self):
        now = pg.time.get_ticks()
        if now - self.last_pound > self.pound_cooldown:
            # Massive AoE knockback
            if (self.target.pos - self.pos).length() < 300:
                self.target.health -= 70
                direction = (self.target.pos - self.pos).normalize()
                self.target.vel = direction * 400
            Explosion(self.game, self.pos, 350, 0)
            self.last_pound = now

    def throw_debris(self):
        now = pg.time.get_ticks()
        if now - self.last_throw > self.throw_cooldown:
            direction = (self.target.pos - self.pos).normalize()
            for _ in range(3):
                spread_dir = direction.rotate(random.uniform(-15, 15))
                PoisonBall(self.game, self.pos, 0, spread_dir * THROW_SPEED * 1.2)
            self.last_throw = now

    def regenerate(self):
        now = pg.time.get_ticks()
        if now - self.last_regen > self.regen_cooldown:
            self.health += 500  # Heal
            self.last_regen = now

    def update(self):
        super().update()
        self.berserker_rage()
        self.ground_pound_attack()
        self.throw_debris()
        self.regenerate()


class PlagueDoctor(Boss):
    """Level 16 Boss - Disease cloud, infect minions, plague bomb, quarantine field"""
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.cloud_cooldown = 3000
        self.last_cloud = 0
        self.infect_cooldown = 10000
        self.last_infect = 0
        self.bomb_cooldown = 8000
        self.last_bomb = 0
        self.field_cooldown = 15000
        self.last_field = 0

    def disease_cloud(self):
        now = pg.time.get_ticks()
        if now - self.last_cloud > self.cloud_cooldown:
            # DoT in area
            if (self.target.pos - self.pos).length() < 250:
                dot = DotEffect(self.game, self.target, 8, 5000, 0.8)
                self.target.apply_dot(dot)
            self.last_cloud = now

    def infect_minions(self):
        now = pg.time.get_ticks()
        if now - self.last_infect > self.infect_cooldown:
            # Summon infected zombies
            for _ in range(4):
                offset = vec(random.randint(-120, 120), random.randint(-120, 120))
                ZombieMob(self.game, self.pos.x + offset.x, self.pos.y + offset.y)
            self.last_infect = now

    def plague_bomb(self):
        now = pg.time.get_ticks()
        if now - self.last_bomb > self.bomb_cooldown:
            # Large poison explosion
            Explosion(self.game, self.target.pos, 300, 60)
            PoisonPuddle(self.game, self.target.pos, 250)
            self.last_bomb = now

    def quarantine_field(self):
        now = pg.time.get_ticks()
        if now - self.last_field > self.field_cooldown:
            # Trap player in damage zone
            if (self.target.pos - self.pos).length() < 400:
                self.target.health -= 100
            self.last_field = now

    def update(self):
        super().update()
        self.disease_cloud()
        self.infect_minions()
        self.plague_bomb()
        self.quarantine_field()


class MechTitan(Boss):
    """Level 17 Boss - Missile barrage, energy cannon, force shield, orbital strike"""
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.barrage_cooldown = 5000
        self.last_barrage = 0
        self.cannon_cooldown = 3000
        self.last_cannon = 0
        self.shield_cooldown = 12000
        self.last_shield = 0
        self.strike_cooldown = 20000
        self.last_strike = 0
        self.shield_active = False

    def missile_barrage(self):
        now = pg.time.get_ticks()
        if now - self.last_barrage > self.barrage_cooldown:
            # Many missiles
            for _ in range(10):
                angle = random.uniform(0, 360)
                direction = vec(1, 0).rotate(angle)
                PoisonBall(self.game, self.pos, 0, direction * 500)
            self.last_barrage = now

    def energy_cannon(self):
        now = pg.time.get_ticks()
        if now - self.last_cannon > self.cannon_cooldown:
            # Powerful laser
            direction = (self.target.pos - self.pos).normalize()
            for i in range(10):
                laser_pos = self.pos + direction * (i * 40)
                Explosion(self.game, laser_pos, 80, 25)
            self.last_cannon = now

    def force_shield(self):
        now = pg.time.get_ticks()
        if now - self.last_shield > self.shield_cooldown:
            self.shield_active = True
            # Damage reduction for 5 seconds
            self.last_shield = now

    def orbital_strike(self):
        now = pg.time.get_ticks()
        if now - self.last_strike > self.strike_cooldown:
            # Ultimate attack
            Explosion(self.game, self.target.pos, 600, 150)
            self.last_strike = now

    def update(self):
        super().update()
        self.missile_barrage()
        self.energy_cannon()
        self.force_shield()
        self.orbital_strike()


class VampireLord(Boss):
    """Level 18 Boss - Life drain, summon bats, blood strike, mist form"""
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.drain_cooldown = 2500
        self.last_drain = 0
        self.bats_cooldown = 8000
        self.last_bats = 0
        self.strike_cooldown = 5000
        self.last_strike = 0
        self.mist_cooldown = 15000
        self.last_mist = 0
        self.is_mist = False

    def life_drain_attack(self):
        now = pg.time.get_ticks()
        if now - self.last_drain > self.drain_cooldown:
            if (self.target.pos - self.pos).length() < 350:
                drain = 40
                self.target.health -= drain
                self.health += drain
            self.last_drain = now

    def summon_bats(self):
        now = pg.time.get_ticks()
        if now - self.last_bats > self.bats_cooldown:
            for _ in range(6):
                offset = vec(random.randint(-100, 100), random.randint(-100, 100))
                MantisMob(self.game, self.pos.x + offset.x, self.pos.y + offset.y)
            self.last_bats = now

    def blood_strike(self):
        now = pg.time.get_ticks()
        if now - self.last_strike > self.strike_cooldown:
            if (self.target.pos - self.pos).length() < 200:
                self.target.health -= 80
            Explosion(self.game, self.target.pos, 200, 0)
            self.last_strike = now

    def mist_form(self):
        now = pg.time.get_ticks()
        if now - self.last_mist > self.mist_cooldown:
            self.is_mist = True
            # Teleport to random location
            self.pos = vec(random.randint(100, 800), random.randint(100, 800))
            self.last_mist = now

    def update(self):
        super().update()
        self.life_drain_attack()
        self.summon_bats()
        self.blood_strike()
        self.mist_form()


class AncientDragon(Boss):
    """Level 19 Boss - Fire breath, tail sweep, wing buffet, dragon roar"""
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.breath_cooldown = 6000
        self.last_breath = 0
        self.sweep_cooldown = 8000
        self.last_sweep = 0
        self.buffet_cooldown = 10000
        self.last_buffet = 0
        self.roar_cooldown = 15000
        self.last_roar = 0

    def fire_breath(self):
        now = pg.time.get_ticks()
        if now - self.last_breath > self.breath_cooldown:
            # Cone of fire
            direction = (self.target.pos - self.pos).normalize()
            for i in range(15):
                spread = direction.rotate(random.uniform(-40, 40))
                PoisonBall(self.game, self.pos, 0, spread * THROW_SPEED)
            self.last_breath = now

    def tail_sweep(self):
        now = pg.time.get_ticks()
        if now - self.last_sweep > self.sweep_cooldown:
            # 180 degree sweep
            for angle in range(-90, 90, 20):
                direction = vec(1, 0).rotate(self.rot + angle)
                Explosion(self.game, self.pos + direction * 150, 120, 50)
            self.last_sweep = now

    def wing_buffet(self):
        now = pg.time.get_ticks()
        if now - self.last_buffet > self.buffet_cooldown:
            # Knockback
            if (self.target.pos - self.pos).length() < 400:
                direction = (self.target.pos - self.pos).normalize()
                self.target.vel = direction * 500
                self.target.health -= 60
            self.last_buffet = now

    def dragon_roar(self):
        now = pg.time.get_ticks()
        if now - self.last_roar > self.roar_cooldown:
            # Stun and damage
            if (self.target.pos - self.pos).length() < 600:
                self.target.health -= 100
                self.target.is_stunned = True
                self.target.stun_timer = now + 3000
            self.last_roar = now

    def update(self):
        super().update()
        self.fire_breath()
        self.tail_sweep()
        self.wing_buffet()
        self.dragon_roar()


class ApocalypseOverlord(Boss):
    """Level 20 FINAL BOSS - Ultimate barrage, summon champions, reality tear, apocalypse"""
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.barrage_cooldown = 4000
        self.last_barrage = 0
        self.champion_cooldown = 15000
        self.last_champion = 0
        self.tear_cooldown = 12000
        self.last_tear = 0
        self.apocalypse_cooldown = 30000
        self.last_apocalypse = 0

    def ultimate_barrage(self):
        now = pg.time.get_ticks()
        if now - self.last_barrage > self.barrage_cooldown:
            # Everything at once
            for _ in range(20):
                angle = random.uniform(0, 360)
                direction = vec(1, 0).rotate(angle)
                PoisonBall(self.game, self.pos, 0, direction * random.randint(400, 700))
            self.last_barrage = now

    def summon_champions(self):
        now = pg.time.get_ticks()
        if now - self.last_champion > self.champion_cooldown:
            # Summon all mob types
            for MobClass in [ZombieMob, ScorpionMob, RobotMob, MantisMob, ZombieDogMob]:
                offset = vec(random.randint(-200, 200), random.randint(-200, 200))
                MobClass(self.game, self.pos.x + offset.x, self.pos.y + offset.y)
            self.last_champion = now

    def reality_tear(self):
        now = pg.time.get_ticks()
        if now - self.last_tear > self.tear_cooldown:
            # Create explosions in a pattern
            for i in range(10):
                angle = (i * 36)
                radius = 300
                tear_pos = self.pos + vec(radius, 0).rotate(angle)
                Explosion(self.game, tear_pos, 250, 70)
            self.last_tear = now

    def apocalypse_attack(self):
        now = pg.time.get_ticks()
        if now - self.last_apocalypse > self.apocalypse_cooldown:
            # Massive screen-wide attack
            Explosion(self.game, self.pos, 800, 200)
            # Summon more enemies
            for _ in range(10):
                offset = vec(random.randint(-300, 300), random.randint(-300, 300))
                ZombieMob(self.game, self.pos.x + offset.x, self.pos.y + offset.y)
            self.last_apocalypse = now

    def update(self):
        super().update()
        self.ultimate_barrage()
        self.summon_champions()
        self.reality_tear()
        self.apocalypse_attack()


# Define the LEVEL_BOSS mapping with lambda functions
LEVEL_BOSS = {
    1: lambda game, x, y: ZombieBoss(game, x, y),
    2: lambda game, x, y: ScorpionBoss(game, x, y),
    3: lambda game, x, y: RobotBoss(game, x, y),
    4: lambda game, x, y: AirportBot(game, x, y),
    5: lambda game, x, y: BusDriver(game, x, y),
    6: lambda game, x, y: SewerMonster(game, x, y),
    7: lambda game, x, y: MountainTroll(game, x, y),
    8: lambda game, x, y: DirewolfBoss(game, x, y),
    9: lambda game, x, y: Necromancer(game, x, y),
    10: lambda game, x, y: ToxicAbomination(game, x, y),
    11: lambda game, x, y: CyberSpiderQueen(game, x, y),
    12: lambda game, x, y: FireElemental(game, x, y),
    13: lambda game, x, y: IceGolem(game, x, y),
    14: lambda game, x, y: ShadowAssassin(game, x, y),
    15: lambda game, x, y: MutantBrute(game, x, y),
    16: lambda game, x, y: PlagueDoctor(game, x, y),
    17: lambda game, x, y: MechTitan(game, x, y),
    18: lambda game, x, y: VampireLord(game, x, y),
    19: lambda game, x, y: AncientDragon(game, x, y),
    20: lambda game, x, y: ApocalypseOverlord(game, x, y),
}        


class ZombieMob(Mob):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        super().__init__(game, x, y, 'zombie_mob', game.map, game.player, game.walls)
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
                self.pos += self.vel * self.game.dt
                self.hit_rect.centerx = self.pos.x
                collide_with_walls(self, self.game.walls, 'x')
                self.hit_rect.centery = self.pos.y
                collide_with_walls(self, self.game.walls, 'y')
        else:
            # Check if cooldown has elapsed and it's time to lunge.
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
                    self.avoid_walls()  # Avoid walls during lunge

    def avoid_walls(self):
        current_time = pygame.time.get_ticks()
        """Avoid walls during lunge."""
        for wall in self.game.walls:
            if pygame.sprite.collide_rect(self, wall):
                self.vel = vec(0, 0)  # Stop moving if colliding with a wall
                self.is_lunging = False  # Reset lunging state
                break
        else:
            # Check if cooldown has elapsed and it's time to lunge.
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
        self.pos += self.vel * self.game.dt
        player_dist = self.target.pos - self.pos
        if player_dist.length_squared() < ENGAGE_RADIUS**2:
            self.zombie_lunge()
            if random.random() < 0.002:
                choice(self.game.zombie_moan_sounds).play()
            self.rot = player_dist.angle_to(vec(1, 0))
            self.image = pg.transform.rotate(self.game.mob_img['zombie_mob'], self.rot)
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
            # Track killed mob to prevent respawn on load
            if hasattr(self, 'spawn_id') and self.spawn_id:
                self.game.killed_mobs.add(self.spawn_id)
            choice(self.game.zombie_hit_sounds).play()
            self.game.map_img.blit(self.game.splat, self.pos - vec(32, 32))
            self.kill()



class ZombieBear(Mob):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        super().__init__(game, x, y, 'zombie_bear', game.map, game.player, game.walls)
        self.health = 300  # Large health pool
        self.swipe_cooldown = 2000
        self.last_swipe = 0
        self.charge_cooldown = 5000
        self.last_charge = 0
        self.is_charging = False
        self.charge_speed = 400

    def swipe_attack(self):
        now = pg.time.get_ticks()
        if now - self.last_swipe > self.swipe_cooldown:
            player_dist = self.target.pos - self.pos
            if player_dist.length() < 100:
                self.target.health -= 30  # Swipe damage
                self.last_swipe = now

    def charge_attack(self):
        now = pg.time.get_ticks()
        if now - self.last_charge > self.charge_cooldown:
            player_dist = self.target.pos - self.pos
            if player_dist.length() < 300 and not self.is_charging:
                self.is_charging = True
                direction = player_dist.normalize()
                self.vel = direction * self.charge_speed
                self.last_charge = now

    def update(self):
        super().update()
        if self.is_charging:
            # Continue charging for a short duration
            if pg.time.get_ticks() - self.last_charge > 1000:
                self.is_charging = False
                self.vel = vec(0, 0)
        else:
            self.swipe_attack()
            self.charge_attack()
            player_dist = self.target.pos - self.pos
            if player_dist.length_squared() < ENGAGE_RADIUS**2:
                if random.random() < 0.002:
                    choice(self.game.zombie_moan_sounds).play()
                self.rot = player_dist.angle_to(vec(1, 0))
                self.image = pg.transform.rotate(self.game.mob_img['zombie_bear'], self.rot)
                self.rect = self.image.get_rect()
                self.rect.center = self.hit_rect.center


class ScorpionMob(Mob):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, 'scorpion_mob')
        self.hit_rect.width *= 0.75
        self.hit_rect.height *= 0.75
        self.last_shot = 0
        self.engage_radius = 600

    def spit_poison(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > 3000:
            distance = (self.target.pos - self.pos).length_squared()
            if distance < self.engage_radius**2:
                direction = (self.target.pos - self.pos).normalize()
                velocity = direction * THROW_SPEED
                PoisonBall(self.game, self.pos, 8, velocity)
                self.last_shot = now

    
    def update(self):
        super().update()
        if (self.target.pos - self.pos).length_squared() < self.engage_radius**2:
            self.spit_poison()

    
        
class PoisonBall(pg.sprite.Sprite):
    def __init__(self, game, pos, damage, velocity):
        super().__init__(game.all_sprites, game.mob_bullets)
        self.game = game
        self.image = game.mob_weapon_images['poison_ball']
        self.rect = self.image.get_rect(center=pos)
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.damage = damage
        self.spawn_time = pg.time.get_ticks()
        self.duration = 1000
        self.velocity = velocity
        self.target = game.player


    def update(self):
        self.pos += self.velocity * self.game.dt
        self.rect.center = self.pos

        if pg.sprite.collide_rect(self, self.target):
            self.target.health -= self.damage
            self.target.apply_dot(DotEffect(self.game, self.target, 5, 5000, 500))
            PoisonPuddle(self.game, self.pos)
            self.kill()

        elif pg.sprite.spritecollideany(self, self.game.walls):
            PoisonPuddle(self.game, self.pos)
            self.kill()

        elif pg.time.get_ticks() - self.spawn_time > self.duration:
            PoisonPuddle(self.game, self.pos)
            self.kill()
        

    def apply_dot_effect(self):
        dot_effect = DotEffect(self.game, self.target, 5, 5000, 500)
        self.target.apply_dot(dot_effect)


class PoisonPuddle(pg.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__(game.all_sprites, game.mob_bullets)
        self.game = game
        self.image = game.mob_weapon_images['poison_puddle']
        self.rect = self.image.get_rect(center=pos)
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.damage = POISON_DAMAGE
        self.last_damage_time = 0
        self.damage_interval = 500
        self.spawn_time = pg.time.get_ticks()
        self.duration = 3000
        self.target = game.player

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > self.duration:
            self.kill()

        if self.rect.colliderect(self.target.rect):
            now = pg.time.get_ticks()
            if now - self.last_damage_time > self.damage_interval:
                self.target.health -= self.damage
                self.last_damage_time = now
   

class RobotMob(Mob):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs, game.boss
        super().__init__(game, x, y, 'robot_mob')
        self.engage_radius = 600
        self.last_shot = 0
    
    def pulse_shock(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > 3000:  
            player_pos = self.target.pos
            mob_pos = self.pos
            mob_to_player = player_pos - mob_pos
            distance_to_player = mob_to_player.length()
            #dir = vec(1, 0).rotate(-self.rot)
            
            if distance_to_player < self.engage_radius:
                # Launch the poison ball towards the player
                mob_to_player.normalize_ip()
                mob_velocity = mob_to_player * ELECTRO_SHOCK_SPEED
                # Create a new poison ball at the current position
                new_electro_shock = ElectroShock(self.game, mob_pos, ELECTRO_SHOCK_DAMAGE)
                
                new_electro_shock.vel = mob_velocity
                self.last_shot = now  # Update the last_shot time
        

    def update(self):
        super().update()
        self.pos += self.vel * self.game.dt
        player_dist = self.target.pos - self.pos
        if player_dist.length_squared() < self.engage_radius**2:
           self.pulse_shock()

class ElectroShock(pg.sprite.Sprite):
    def __init__(self, game, pos, damage):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.mob_bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_weapon_images['electro_shock']
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        self.rot = 0
        self.damage = damage
        self.duration = 7000  # Duration of the poison ball in milliseconds
        self.spawn_time = pg.time.get_ticks()  # Track the spawn time
        self.engage_radius = 250  # Engage radius in pixels
        self.wall = game.walls
        self.target = game.player  # Set the target as the player
        # Calculate initial direction and velocity towards the player's position at creation
        direction = (self.target.pos - self.pos).normalize()  # Normalize to get direction
        self.velocity = direction * ELECTRO_SHOCK_SPEED  # Maintain this velocity



    def update(self):
        # Move in the initial direction towards the player's position at creation
        self.pos += self.velocity * self.game.dt
        self.rect.center = self.pos
        #DotEffect(self.game, self.target, 5, 5000, 500)
        if pg.sprite.spritecollideany(self,self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > self.duration:
            self.kill()


class MantisMob(Mob):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, 'mantis_mob')
        self.camouflage_cooldown = 6000  # 6 seconds
        self.last_camouflage_time = 0
        self.is_camouflaged = True
        self.camouflage_duration = 12000  # 12 seconds
        self.last_strike_time = 0
        self.strike_pause_duration = 1000  # 1 second
        self.is_striking = False
        self.target = game.player
        self.strike_damage = 35

    def camouflage(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_camouflage_time > self.camouflage_cooldown and not self.is_camouflaged:
            self.is_camouflaged = True
            self.last_camouflage_time = current_time

        if self.is_camouflaged:
            if current_time > self.camouflage_duration:
                self.is_camouflaged = False
                self.last_camouflage_time = current_time
               
    def mantis_strike(self):
        current_time = pygame.time.get_ticks()
        player_pos = self.target.pos
        mob_pos = self.pos
        mob_to_player = player_pos - mob_pos
        distance_to_player = mob_to_player.length()

        if distance_to_player < 40 and not self.is_striking:  # Within range and not already striking
            mob_to_player.normalize_ip()
            mob_velocity = mob_to_player * 400
            self.vel = mob_velocity
            self.is_striking = True  # Enter lunging state
            self.avoid_walls()  # Avoid walls during lunge
            if pg.sprite.collide_rect(self, self.target):            
                self.game.player.health -= self.strike_damage
        elif self.is_striking:  # If already striking, check if it's time to reset velocity
            if current_time - self.last_strike_time > self.strike_pause_duration:
                self.vel = vec(0, 0)  # Stop moving after lunge pause
                self.is_striking = False  # Reset lunging state
                self.last_strike_time = current_time  # Reset strike cooldown

    def update(self):
        super().update()
        self.camouflage()        
        player_dist = self.target.pos - self.pos
        if player_dist.length_squared() < ENGAGE_RADIUS**2:
            if random.random() < 0.002:
                choice(self.game.zombie_moan_sounds).play()
            self.rot = player_dist.angle_to(vec(1, 0))
            if self.is_camouflaged:
                self.image = pg.transform.rotate(self.game.mob_img['camo_mantis'], self.rot)
            else:
                self.image = pg.transform.rotate(self.game.mob_img['mantis_mob'], self.rot)            
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(1, 0.01).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
        if player_dist.length_squared() < 40:
            self.mantis_strike()
        if self.health <= 0:
            # Track killed mob to prevent respawn on load
            if hasattr(self, 'spawn_id') and self.spawn_id:
                self.game.killed_mobs.add(self.spawn_id)
            choice(self.game.zombie_hit_sounds).play()
            self.game.map_img.blit(self.game.splat, self.pos - vec(32, 32))
            self.kill()
            self.game.score += 50

class ZombieDogMob(Mob):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, 'zombie_dog_mob')
        self.last_spawn = pg.time.get_ticks()  # Initialize last_spawn with the current time
        self.last_dodge = 0  # Initialize last_throw with 0 or current time
        self.speed = 110

    def dodge_bullet(self):
        now = pg.time.get_ticks()
        if now - self.last_dodge > 3000:            
            # Example dodge logic: move the mob to a new position
            dodge_distance = 20  # Distance to dodge
            self.vel = vec(0, dodge_distance)  # Move vertically by dodge_distance
            self.pos += self.vel  # Update the position
            self.last_dodge = now

    def update(self):
        super().update()
        if pg.sprite.spritecollideany(self, self.game.bullets):
            self.dodge_bullet()
        self.speed = 110
        self.dodge_bullet()
        
