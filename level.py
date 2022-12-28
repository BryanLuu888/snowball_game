import pygame
from settings import *
from Tile import Tile
from player import Player
from support import *
from random import choice
from ui import UI
from projectile import Projectile
# from debug import debug
class level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.create_map()
        self.ui = UI()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_Objects.csv')
        }

        graphics = {
            'grass': import_folder('graphics/Grass'),
            'objects': import_folder('graphics/objects'),
        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index*TILESIZE
                        y = row_index*TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'grass', random_grass_image)
                        if style == 'object':
                            if int(col) < 10:
                                col = "0" + col
                            obj_filename = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites,self.obstacle_sprites], 'object', obj_filename)
        #         if col=='x':
        #             Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
        #         if col=='p':
        #             self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)
        self.player = Player((2000, 1430), [self.visible_sprites], self.obstacle_sprites, self.shoot_arrow)


    def shoot_arrow(self, vector, selected_weapon):
        self.arrow = Projectile(self.player, groups=[self.visible_sprites], vector=vector, selected_weapon=selected_weapon)


    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)
        self.ui.drag_shoot(self.player)



class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]//2
        self.half_height = self.display_surface.get_size()[1]//2
        self.offset = pygame.math.Vector2()

        #creating the floor
        self.floor_surface = pygame.image.load('graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        #camera movement
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
