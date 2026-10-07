import pygame
import random

LANE_W=80
COLORS=[(220,60,60),(220,140,40),(140,60,180),(60,180,80),(180,180,40),(60,80,200)]

class Car:
    def __init__(self, lane_x, y, direction, speed):
        self.rect=pygame.Rect(lane_x+10,y,60,80)
        self.direction=direction  # 1=down, -1=up
        self.speed=speed
        self.color=random.choice(COLORS)

    def update(self):
        self.rect.y+=self.direction*self.speed

    def off_screen(self,height):
        return self.rect.top>height+100 or self.rect.bottom<-100

    def draw_headlights(self,screen):
        reach=170
        near_y=self.rect.top+4 if self.direction<0 else self.rect.bottom-4
        far_y=near_y-reach if self.direction<0 else near_y+reach
        center_x=self.rect.centerx
        points=[
            (center_x-20,near_y),
            (center_x+20,near_y),
            (center_x+66,far_y),
            (center_x-66,far_y),
        ]
        pygame.draw.polygon(screen,(255,225,145,38),points)

    def draw(self,screen,night=False):
        pygame.draw.rect(screen,self.color,self.rect,border_radius=8)
        pygame.draw.rect(screen,(180,220,240),pygame.Rect(self.rect.x+8,self.rect.y+10,44,22),border_radius=4)
        for wx in [self.rect.x+6,self.rect.right-16]:
            for wy in [self.rect.y+4,self.rect.bottom-16]:
                pygame.draw.rect(screen,(30,30,30),pygame.Rect(wx,wy,10,12),border_radius=3)
        if night:
            headlight_y=self.rect.bottom-14 if self.direction>0 else self.rect.top+4
            for light_x in [self.rect.left+16,self.rect.right-26]:
                pygame.draw.ellipse(screen,(255,245,180),pygame.Rect(light_x,headlight_y,10,8))

def make_car(lane_idx,height,speed):
    x=lane_idx*LANE_W
    direction=1 if lane_idx%2==0 else -1
    y=-90 if direction==1 else height+10
    return Car(x,y,direction,speed)
