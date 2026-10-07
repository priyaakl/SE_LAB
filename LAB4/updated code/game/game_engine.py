import pygame
import random
from game.player import Player,LANE_W
from game.traffic import Car,make_car
from game.high_scores import load_high_scores,save_high_scores

LANES=8
WIDTH=LANES*LANE_W
HEIGHT=600
FPS=60
BG=(60,60,60)
RIVER_HEIGHT=90
RIVER_TOP=(HEIGHT-RIVER_HEIGHT)//2
RAFT_WIDTH=180
RAFT_SPEED=2.5
DAY_NIGHT_INTERVAL=30000

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Traffic Escape")
        self.clock=pygame.time.Clock()
        self.font=pygame.font.SysFont("monospace",24,bold=True)
        self.big_font=pygame.font.SysFont("monospace",44,bold=True)
        self.high_scores=load_high_scores()
        self.day_night_started=pygame.time.get_ticks()
        self.is_night=False
        self.reset()

    def reset(self):
        self.player=Player(WIDTH//2,HEIGHT-80)
        self.cars=[]
        self.timer=0
        self.spawn_interval=50
        self.speed=3
        self.score=0
        self.lives=3
        self.colliding_cars=set()
        self.river=pygame.Rect(0,RIVER_TOP,WIDTH,RIVER_HEIGHT)
        self.raft=pygame.Rect(0,RIVER_TOP,RAFT_WIDTH,RIVER_HEIGHT)
        self.raft_x=float(self.raft.x)
        self.raft_speed=RAFT_SPEED
        self.riding_raft=False
        self.unsafe_in_river=False
        self.game_over=False
        self.won=False
        self.score_recorded=False

    def _record_score(self):
        if self.score_recorded:
            return
        self.score_recorded=True
        updated=sorted(self.high_scores+[self.score//10],reverse=True)[:5]
        if updated!=self.high_scores:
            self.high_scores=updated
            save_high_scores(self.high_scores)

    def _update_day_night(self):
        elapsed=pygame.time.get_ticks()-self.day_night_started
        self.is_night=(elapsed//DAY_NIGHT_INTERVAL)%2==1

    def _move_raft(self):
        previous_x=self.raft.x
        self.raft_x+=self.raft_speed
        if self.raft_x<=0 or self.raft_x>=WIDTH-RAFT_WIDTH:
            self.raft_x=max(0,min(WIDTH-RAFT_WIDTH,self.raft_x))
            self.raft_speed=-self.raft_speed
        self.raft.x=round(self.raft_x)
        return self.raft.x-previous_x

    def _lose_life(self):
        if self.lives>0:
            self.lives-=1
            if self.lives==0:
                self.game_over=True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT: return False
            if event.type==pygame.KEYDOWN and event.key==pygame.K_r: self.reset()
        return True

    def update(self):
        self._update_day_night()
        if self.game_over or self.won: return
        keys=pygame.key.get_pressed()
        raft_dx=self._move_raft()
        if self.riding_raft:
            self.player.rect.x=max(0,min(WIDTH-self.player.rect.width,self.player.rect.x+raft_dx))
        self.player.move(keys,0,WIDTH)
        self.timer+=1
        if self.timer>=self.spawn_interval:
            lane=random.randint(0,LANES-1)
            self.cars.append(make_car(lane,HEIGHT,self.speed))
            self.timer=0
            self.spawn_interval=max(22,self.spawn_interval-0.2)
        in_river=self.river.collidepoint(self.player.rect.center)
        on_raft=in_river and self.raft.left<=self.player.rect.centerx<=self.raft.right
        if in_river and not on_raft:
            if not self.unsafe_in_river and not self.game_over:
                self._lose_life()
            self.unsafe_in_river=True
            self.riding_raft=False
        else:
            self.unsafe_in_river=False
            self.riding_raft=on_raft
        for c in self.cars:
            c.update()
            if not in_river and c.rect.colliderect(self.player.rect):
                if c not in self.colliding_cars and not self.game_over:
                    self._lose_life()
        self.colliding_cars={c for c in self.cars if not in_river and c.rect.colliderect(self.player.rect)}
        self.cars=[c for c in self.cars if not c.off_screen(HEIGHT)]
        self.score+=1
        if self.score%300==0: self.speed=min(10,self.speed+0.5)
        if self.player.rect.top<=10:
            self.won=True
        if self.game_over or self.won:
            self._record_score()

    def draw(self):
        if self.is_night:
            background=(18,25,38)
            lane_color=(65,75,82)
            marking_color=(115,112,78)
            sidewalk_color=(72,72,78)
        else:
            background=BG
            lane_color=(100,100,100)
            marking_color=(200,200,100)
            sidewalk_color=(150,130,110)
        self.screen.fill(background)
        # road markings
        for i in range(LANES+1):
            pygame.draw.line(self.screen,lane_color,(i*LANE_W,0),(i*LANE_W,HEIGHT),2)
        for y in range(0,HEIGHT,60):
            for i in range(LANES):
                pygame.draw.rect(self.screen,marking_color,pygame.Rect(i*LANE_W+LANE_W//2-3,y,6,30))
        # sidewalks
        pygame.draw.rect(self.screen,sidewalk_color,pygame.Rect(0,HEIGHT-50,WIDTH,50))
        pygame.draw.rect(self.screen,sidewalk_color,pygame.Rect(0,0,WIDTH,30))
        if self.is_night:
            headlight_layer=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
            for c in self.cars:
                c.draw_headlights(headlight_layer)
            self.screen.blit(headlight_layer,(0,0))
        for c in self.cars: c.draw(self.screen,self.is_night)
        river_color=(17,54,75) if self.is_night else (35,115,145)
        ripple_color=(45,106,130) if self.is_night else (65,145,165)
        pygame.draw.rect(self.screen,river_color,self.river)
        for y in range(self.river.top+10,self.river.bottom,20):
            for x in range((y//20%2)*24,WIDTH,72):
                pygame.draw.line(self.screen,ripple_color,(x,y),(x+20,y),2)
        pygame.draw.rect(self.screen,(80,48,26),self.raft,border_radius=8)
        inner_raft=self.raft.inflate(-8,-8)
        pygame.draw.rect(self.screen,(150,98,48),inner_raft,border_radius=6)
        for y in range(inner_raft.top+12,inner_raft.bottom,16):
            pygame.draw.line(self.screen,(95,58,30),(inner_raft.left+3,y),(inner_raft.right-3,y),3)
        self.player.draw(self.screen)
        hud=pygame.Rect(0,0,WIDTH,58)
        pygame.draw.rect(self.screen,(20,20,20),hud)
        s=self.font.render(f"Score: {self.score//10}  Lives: {self.lives}",True,(220,220,220))
        controls=self.font.render("GOAL: top  R=Restart",True,(220,220,220))
        mode_text="NIGHT" if self.is_night else "DAY"
        mode_color=(255,220,125) if self.is_night else (175,225,255)
        mode=self.font.render(mode_text,True,mode_color)
        self.screen.blit(s,(6,2))
        self.screen.blit(controls,(6,30))
        mode_rect=mode.get_rect(top=3,right=WIDTH-8)
        self.screen.blit(mode,mode_rect)
        if self.game_over:
            self._msg("CRASHED!",(220,60,60))
        if self.won:
            self._msg("YOU MADE IT!",(80,220,80))
        pygame.display.flip()

    def _msg(self,text,color):
        ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        ov.fill((0,0,0,150))
        self.screen.blit(ov,(0,0))
        m=self.big_font.render(text,True,color)
        sub=self.font.render(f"Score: {self.score//10}  Press R to Restart",True,(200,200,200))
        heading=self.font.render("TOP 5 HIGH SCORES",True,(245,210,100))
        self.screen.blit(m,(WIDTH//2-m.get_width()//2,HEIGHT//2-115))
        self.screen.blit(sub,(WIDTH//2-sub.get_width()//2,HEIGHT//2-55))
        self.screen.blit(heading,(WIDTH//2-heading.get_width()//2,HEIGHT//2))
        for rank in range(5):
            score=str(self.high_scores[rank]) if rank<len(self.high_scores) else "---"
            entry=self.font.render(f"{rank+1}.  {score}",True,(230,230,230))
            self.screen.blit(entry,(WIDTH//2-entry.get_width()//2,HEIGHT//2+32+rank*30))

    def run(self):
        running=True
        while running:
            running=self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
