import pygame as pg
import pytmx
from settings import *

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        self.grid = self.build_grid()

    def build_grid(self):
        grid = []
        for y in range(self.tmxdata.height):
            row = []
            for x in range(self.tmxdata.width):
                tile = self.tmxdata.get_tile_gid(x, y, 0)
                row.append(tile)
            grid.append(row)
        return grid

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        offset = (int(self.camera.x), int(self.camera.y))
        return entity.rect.move(offset)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)

class TalentBox:
    def __init__(self, x, y, size, label):
        self.rect = pygame.Rect(x, y, size, size)
        self.level = 0  # Current rank
        self.max_rank = 5  # Maximum rank (can be overridden)
        self.font = pygame.font.SysFont(None, 22)
        self.label = label  # Store the label text
        self.talent_id = None  # Will be set by main.py

    def draw(self, surface):
        # Draw box with gradient based on level
        if self.level == 0:
            color = BOX_COLOR
        elif self.level >= self.max_rank:
            color = (255, 215, 0)  # Gold for max rank
        else:
            # Interpolate between BOX_COLOR and HIGHLIGHT_COLOR
            t = self.level / self.max_rank
            color = tuple(int(BOX_COLOR[i] + (HIGHLIGHT_COLOR[i] - BOX_COLOR[i]) * t) for i in range(3))

        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)  # White border

        # Draw label text above the box
        label_text = self.font.render(self.label, True, TEXT_COLOR)
        label_rect = label_text.get_rect(center=(self.rect.centerx, self.rect.top - 15))
        surface.blit(label_text, label_rect)

        # Draw rank text centered in the box (e.g., "3/5")
        rank_display = f"{self.level}/{self.max_rank}"
        rank_text = self.font.render(rank_display, True, BLACK if self.level > 0 else WHITE)
        rank_rect = rank_text.get_rect(center=self.rect.center)
        surface.blit(rank_text, rank_rect)


class Button:
    def __init__(self, x, y, width, height, text, font_name=None, font_size=40):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(font_name, font_size) if font_name else pygame.font.SysFont('arial', font_size)
        self.is_hovered = False
        self.clicked = False

        # Colors
        self.normal_color = (70, 70, 70)
        self.hover_color = (100, 100, 100)
        self.text_color = WHITE
        self.border_color = WHITE

    def draw(self, surface):
        # Determine color based on hover state
        color = self.hover_color if self.is_hovered else self.normal_color

        # Draw button background
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, 3)

        # Draw text centered on button
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event, mouse_pos):
        # Update hover state
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        # Check for click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.clicked = True
                return True
        return False






    
