import sys
import pygame


class Plane(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surfWidth = 70
        self.surfHeight = 30
        self.black = (0,0,0)
        self.raw_image = pygame.image.load('aircraft.png')
        self.right_image = pygame.transform.scale(self.raw_image,(60,40))
        self.image = self.right_image
        self.image2 = pygame.transform.flip(self.right_image,True,False)
        self.rotate_image_right = pygame.transform.rotate(self.right_image,315)
        self.rotate_image_left = pygame.transform.rotate(self.image2,45)
        self.rect = self.image.get_rect()
        self.rect.y = 100
        self.speed = 3
        self.down_speed = 4
        self.PlaneFired = False
        self.PlaneCollided = False
        self.PlaneLives = 3
        self.plane_crash = pygame.mixer.Sound(file='plane crash.wav')
    def update(self):
        self.rect.x += self.speed
        if self.rect.right > SCREEN_WIDTH and not self.PlaneCollided:
            self.speed = -self.speed
        if self.rect.left <= 0 and not self.PlaneCollided:
            self.speed *= -1
        if self.rect.y < 0 and not self.PlaneCollided:
            self.rect.y = 0
        if self.rect.y > 300 and not self.PlaneCollided:
            self.rect.y = 300
        if self.PlaneCollided:
            self.rect.y += self.down_speed


class PlaneBomb(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.raw_image = pygame.image.load('bomb.png')
        self.right_image = pygame.transform.scale(self.raw_image,(25,30))
        self.image = self.right_image
        self.left_image = pygame.transform.flip(self.right_image,True,False)
        self.rect = self.image.get_rect()
        self.bomb_drop = 3
        self.bomb_drop_sound = pygame.mixer.Sound(file='bombDrop.mp3')
    def update(self):
        self.rect.y += self.bomb_drop


class Tank(pygame.sprite.Sprite):
    def __init__(self,BOTTOM,LEFT):
        super().__init__()
        self.raw_image = pygame.image.load('tank.png')
        self.image = pygame.transform.scale(self.raw_image,(60,60))
        self.rect = self.image.get_rect()
        self.rect.bottom = BOTTOM
        self.rect.left = LEFT
        self.speed = -2
        self.TankTurnedOn = False
        self.TankHit_Sound = pygame.mixer.Sound(file='bombTank hits.wav')
    def update(self):
        self.rect.x += self.speed
        if self.rect.left <= 300:
            self.speed *= -1
        elif self.rect.right >= SCREEN_WIDTH:
            self.speed *= -1



class TankBullet(pygame.sprite.Sprite):
    def __init__(self, ):
        super().__init__()

        self.raw_image = pygame.image.load('bullet.png')
        self.sized_image = pygame.transform.scale(self.raw_image,(20,40))
        self.image = pygame.transform.rotate(self.sized_image,180)
        self.rect = self.image.get_rect()
        self.bulletSpeed = 6

    def update(self):
        self.rect.x -= self.bulletSpeed


class UFO(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.raw_image = pygame.image.load('ufo.png')
        self.image = pygame.transform.scale(self.raw_image,(40,50))
        self.rect = self.image.get_rect()
        self.BeyondTheScreen = 400
        self.speed = 3
        self.current_alien_speed = 3
        self.alien_sound = pygame.mixer.Sound(file='Alien Spawn.wav')
    def update(self):
        self.rect.x -= self.speed


class Bunker(pygame.sprite.Sprite):
    def __init__(self,BunkerHitLimit):
        super().__init__()
        self.raw_image = pygame.image.load('BigSchool.png')
        self.image = pygame.transform.scale(self.raw_image,(275,275))
        self.rect = self.image.get_rect()
        self.rect.bottom = SCREEN_HEIGHT
        self.BunkerHits = 0
        self.BunkerHitLimit = BunkerHitLimit
        self.BunkerHitsLeft = self.BunkerHitLimit - self.BunkerHits


class BunkerText:
    def __init__(self,BunkerHitLimit):
        self.MaxBunkerHitCount = BunkerHitLimit
        self.actual_font = pygame.font.Font(r'C:\Windows\Fonts\comicbd.ttf',18)
        self.BunkerHits = Bunker_.BunkerHits
        self.WrittenText = f'BUNKER HAS {self.MaxBunkerHitCount - self.BunkerHits} HITS LEFT!!!!'
        self.posted_text = self.actual_font.render(self.WrittenText,True,(10,255,0))
        self.textpos = self.posted_text.get_rect(left=0,bottom=Bunker_.rect.top)
    def BlitText(self):
        screen.blit(self.posted_text,self.textpos)


class GameStateText(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.actual_font = pygame.font.Font(r'C:\Windows\Fonts\comicbd.ttf', 18)
        self.WrittenText = 'PRESS ENTER TO CONTINUE'
        self.posted_text = self.actual_font.render(self.WrittenText, True, (0,0,0))
        self.rect = self.posted_text.get_rect()
        self.rect.midtop = Game_State.rect.midbottom
    def BlitGameOverText(self):
        screen.blit(self.posted_text, self.rect)
    def BlitLevel(self,level):
        self.level_text = F'LEVEL {level}'
        self.post_level = self.actual_font.render(self.level_text,True,(0,0,0))
        self.level_rect = self.post_level.get_rect()
        screen.blit(self.post_level,self.level_rect)
    def BlitTanksDestroyed(self,tanks):
        self.destroyed_tanks_text = f'TANKS DESTROYED {tanks}'
        self.tanks_destroyed = self.actual_font.render(self.destroyed_tanks_text,True,(0,0,0))
        self.tanks_destroyed_rect = self.tanks_destroyed.get_rect(left=300)
        screen.blit(self.tanks_destroyed,self.tanks_destroyed_rect)


class GameState(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.YouLose = pygame.image.load('game-over.png').convert()
        self.YouWin = pygame.image.load('win.png').convert()
        self.image = self.YouWin
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2)
        self.GameOver = False
        self.PassedLevel = False
        self.Game_State_Level = 1


class SplashScreen:
    def __init__(self):
        self.actual_font = pygame.font.Font(r'C:\Windows\Fonts\comicbd.ttf', 25)
        self.amelia = 'AMELIA EARHART'
        self.amelia_text = self.actual_font.render(self.amelia, True, (255,255,255))
        self.amelia_rect = self.amelia_text.get_rect(right=-100,bottom=50)
        self.vs = 'VS'
        self.vs_text = self.actual_font.render(self.vs,True,(0,0,255))
        self.vs_rect = self.vs_text.get_rect(center=(SCREEN_WIDTH//2 ,80))
        self.russia = 'RUSSIA'
        self.russia_text = self.actual_font.render(self.russia,True,(255,0,0))
        self.russia_rect = self.russia_text.get_rect(left=SCREEN_WIDTH + 100,bottom=150)


        self.plane_image = pygame.image.load('aircraft.png')
        self.sized_plane = pygame.transform.scale(self.plane_image,(200,200))
        self.plane_rect = self.sized_plane.get_rect(center=(SCREEN_WIDTH//2,250))
        self.bomb = pygame.image.load('bomb.png')
        self.sized_bomb = pygame.transform.scale(self.bomb,(100,100))
        self.bomb_rect = self.sized_bomb.get_rect()
        self.tank = pygame.image.load('tank.png')
        self.sized_tank = pygame.transform.scale(self.tank, (250,250))
        self.tank_rect = self.sized_bomb.get_rect(bottom=700, right=SCREEN_WIDTH // 2)
        self.press_enter = 'PRESS ENTER TO START THE GAME'
        self.press_enter_text = self.actual_font.render(self.press_enter, True, (0,200,90))
        self.press_enter_rect = self.press_enter_text.get_rect(centerx=SCREEN_WIDTH//2,bottom=self.tank_rect.top)
        self.text_list = [self.amelia_text,self.vs_text,self.russia_text,self.press_enter_text]
        self.rect_list = [self.amelia_rect,self.vs_rect,self.russia_rect,self.press_enter_rect]


        self.amelia_speed = 2
        self.russia_speed = 2
        self.GameRunning = False
        self.splash_sound = pygame.mixer.Sound(file='bombTank hits.wav')
    def BlitSplashScreenText(self):
        for i in range(5):
            for a,b in zip(self.text_list,self.rect_list):
                screen.blit(a,b)
        screen.blit(self.sized_plane, self.plane_rect)
        self.bomb_rect.midtop = self.plane_rect.midbottom
        screen.blit(self.sized_bomb, self.bomb_rect)
        screen.blit(self.sized_tank, self.tank_rect)
    def update(self):
        self.amelia_rect.x += self.amelia_speed
        self.russia_rect.x -= self.russia_speed
        if self.amelia_rect.centerx  >= self.vs_rect.centerx:
            self.amelia_speed = 0
        if self.russia_rect.centerx == self.vs_rect.centerx:
            self.russia_speed = 0


pygame.init()
#HANDLING PLAYER LIVES
def CheckingLives():
    '''Handles how many lives the player has and the blits the images on the top right of screen'''
    X_List = [i for i in range(900, 1050, 50)]
    Y_List = [0, 0, 0]
    font_file = pygame.font.Font(r'C:\Windows\Fonts\comicbd.ttf', 18)
    WrittenText = 'LIFE  X '
    posted_text = font_file.render(WrittenText, True, (225, 200, 0))
    rect = posted_text.get_rect()
    rect.right = 890
    image = pygame.image.load('aircraft.png').convert_alpha()
    fixed_image = pygame.transform.scale(image,(30,30))
    screen.blit(posted_text,rect)
    while len(X_List) and len(Y_List) != TheFlyingPlane.PlaneLives:
        X_List.pop()
        Y_List.pop()
    for i in range(TheFlyingPlane.PlaneLives):
        for x,y in zip(X_List,Y_List):
            screen.blit(fixed_image,(x,y))
    return X_List


def CheckEvents():
    for event in pygame.event.get():
        pygame.key.set_repeat(1) #CONTINUOUS PLANE UP/DOWN MOVEMENT
        if event.type == pygame.QUIT:
            raise sys.exit()
        if event.type == pygame.KEYDOWN:
            # DROPPING BOMBS
            if event.key == pygame.K_SPACE:
                if not TheFlyingPlane.PlaneFired:
                    Bombs.rect.midtop = TheFlyingPlane.rect.midbottom
                    PlaneContainer.add(Bombs)
                    PlaneBombGroup.add(Bombs)
                    Bombs.bomb_drop_sound.play(maxtime=2000)

            #UP AND DOWN PLANE MOVEMENT
            if event.key == pygame.K_DOWN:
                TheFlyingPlane.rect.y += 1
            if event.key == pygame.K_UP:
                TheFlyingPlane.rect.y -= 1

            #####SPLITTING THE RETURN KEY USE#####
            if event.key == pygame.K_RETURN:

                #GAMEOVER HANDLING
                if Game_State.GameOver:
                    Game_State_Images_Group.empty()
                    Bunker_.BunkerHits = 0
                    TheFlyingPlane.PlaneLives = 3
                    TheFlyingPlane.speed = 3
                    Game_State.Game_State_Level = 0
                    Aliens.speed = 3
                    Aliens.current_alien_speed = 3
                    pygame.event.set_allowed(
                        [TankOneStopEvent, TankTwoStopEvent, TankThreeStopEvent, UFO_event,GameOver,PassLevelSound])
                    TankContainer.add(TankOne,TankTwo,TankThree)
                    TankOne.TankHitCount,TankTwo.TankHitCount,TankThree.TankHitCount = 0,0,0
                    BunkerContainer.add(Bunker_)
                    Game_State.GameOver = False
                    pygame.mixer.music.play()
                    pygame.event.clear()


                #PASSED LEVEL HANDLING
                if Game_State.PassedLevel:
                    Game_State_Images_Group.empty()
                    AliensGroup.empty()
                    PlaneBombGroup.empty()
                    Bunker_.BunkerHits = 0
                    pygame.mixer.music.play()
                    pygame.event.set_allowed(
                        [TankOneStopEvent, TankTwoStopEvent, TankThreeStopEvent, UFO_event,
                         Tank_Fire_event,PassLevelSound])
                    TankContainer.add(TankOne, TankTwo, TankThree)
                    PlaneContainer.add(TheFlyingPlane)
                    TankOne.TankHitCount, TankTwo.TankHitCount, TankThree.TankHitCount = 0, 0, 0
                    BunkerContainer.add(Bunker_)
                    Game_State.Game_State_Level += 1
                    Aliens.rect.x = SCREEN_WIDTH + Aliens.BeyondTheScreen
                    Aliens.speed += 1
                    Aliens.current_alien_speed += 1
                    for levels in range(0,20,2):
                        if Game_State.Game_State_Level == levels:
                            Current_Plane_Speed = abs(TheFlyingPlane.speed)
                            Current_Plane_Speed += 1
                            TheFlyingPlane.speed = Current_Plane_Speed
                    Game_State.PassedLevel = False
                    pygame.event.clear()
                #EXIT START SCREEN AND START THE GAME
                if not Splash.GameRunning:
                    Splash.GameRunning = True
                    pygame.mixer.music.rewind()


        #CUSTOM EVENTS
        if event.type == TankOneStopEvent:
            TankOne.speed = 0
            pygame.time.set_timer(Tank_Fire_event, 300)
            TankOne.TankTurnedOn = True
        if event.type == TankTwoStopEvent:
            TankTwo.speed = 0
            pygame.time.set_timer(Tank_Fire_event, 300)
            TankTwo.TankTurnedOn = True
        if event.type == TankThreeStopEvent:
            TankThree.speed = 0
            pygame.time.set_timer(Tank_Fire_event, 300)
            TankThree.TankTurnedOn = True
        if event.type == Tank_Fire_event:
            if TankOne.TankTurnedOn:
                Tank_Bullet.rect.midright = TankOne.rect.midleft
                TankBulletGroup.add(Tank_Bullet)
                TankOne.TankTurnedOn = False
            if TankTwo.TankTurnedOn:
                Tank_Bullet.rect.midright = TankTwo.rect.midleft
                TankBulletGroup.add(Tank_Bullet)
                TankTwo.TankTurnedOn = False
            if TankThree.TankTurnedOn:
                Tank_Bullet.rect.midright = TankThree.rect.midleft
                TankBulletGroup.add(Tank_Bullet)
                TankThree.TankTurnedOn = False
        if event.type == UFO_event:
            Aliens.rect.x = SCREEN_WIDTH + Aliens.BeyondTheScreen
            Aliens.rect.y = TheFlyingPlane.rect.y
            AliensGroup.add(Aliens)
            Aliens.alien_sound.play(loops=5)
        if event.type == Spawn_Plane and not TheFlyingPlane.PlaneCollided:
            AliensGroup.empty()
            TheFlyingPlane.PlaneLives -= 1
            PlaneContainer.add(TheFlyingPlane)
            pygame.event.set_allowed([TankOneStopEvent, TankTwoStopEvent, TankThreeStopEvent,UFO_event,pygame.KEYDOWN])
            pygame.event.set_blocked(Spawn_Plane)
        if event.type == GameOver:
            game_over_sound = pygame.mixer.Sound('GameOver (1).wav')
            game_over_sound.play()
            pygame.event.set_blocked(GameOver)
        if event.type == PassLevelSound:
            pass_level_sound = pygame.mixer.Sound('passed level.wav')
            pass_level_sound.play()
            pygame.event.set_blocked(PassLevelSound)

clock = pygame.time.Clock()

#GLOBAL VARIABLES
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

#DECREASE THE RECT COLLIDED SIZE ; SEE pygame.spritecollide section
COLLIDED = pygame.sprite.collide_rect_ratio(0.65)

#SCREENS
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
Splash = SplashScreen()

#BACKGROUND IMAGE
Window_Size = pygame.display.get_window_size()
Image = pygame.image.load('TankGameBackground.jpg')
ImageBackground = pygame.transform.scale(Image, (Window_Size[0], Window_Size[1]))

#GAME_STATE GROUP HANDLING
Game_State = GameState()
Game_State_Text = GameStateText()
Game_State_Images_Group = pygame.sprite.Group()

#PLANE STUFF
TheFlyingPlane = Plane()
PlaneContainer = pygame.sprite.Group()
PlaneContainer.add(TheFlyingPlane)

#PLANE BOMEB STUFF
PlaneBombGroup = pygame.sprite.Group()
Bombs = PlaneBomb()

#TANK STUFF
Tanks_Destroyed = 0
TankContainer = pygame.sprite.Group()
TankOne = Tank(SCREEN_HEIGHT,600)
TankTwo = Tank(SCREEN_HEIGHT,800)
TankThree = Tank(SCREEN_HEIGHT,1000)
TankContainer.add(TankOne,TankTwo,TankThree)

#TANK BULLET STUFF
Tank_Bullet = TankBullet()
TankBulletGroup = pygame.sprite.Group()

#BUNKER STUFF
BunkerHitLimit = 15
BunkerContainer = pygame.sprite.Group()
Bunker_ = Bunker(BunkerHitLimit)
BunkerContainer.add(Bunker_)

#UFO STUFF
Aliens = UFO()
AliensGroup = pygame.sprite.Group()
BeyondTheScreen = 400
Current_Alien_Speed = 0

#EVENTS
TankOneStopEvent = pygame.USEREVENT + 1
TankTwoStopEvent = pygame.USEREVENT + 2
TankThreeStopEvent = pygame.USEREVENT + 3
Tank_Fire_event = pygame.USEREVENT + 4
UFO_event = pygame.USEREVENT + 5
Spawn_Plane = pygame.USEREVENT + 6
#GAMEOVER SOUND HANDLING
GameOver = pygame.USEREVENT + 7
#SOUND WHEN LEVEL IS COMPLETE
PassLevelSound = pygame.USEREVENT + 8

pygame.time.set_timer(TankOneStopEvent, 3000)
pygame.time.set_timer(TankTwoStopEvent,8000)
pygame.time.set_timer(TankThreeStopEvent,13000)
pygame.time.set_timer(UFO_event, 10000)

#Background Music
pygame.mixer.music.load(filename='bg ogg.ogg')
pygame.mixer.music.play()
splash_screen_background_music = pygame.mixer.Sound(file='retro-wave-style-track-59892.wav')
while True:
    pygame.event.pump()
    Bunker_Text = BunkerText(BunkerHitLimit)
    Splash.update()

    if not Splash.GameRunning:
        screen.fill((0,0,0))
        Splash.BlitSplashScreenText()
        pygame.mixer.music.set_volume(0.0)
        #need to fix
        splash_screen_background_music.play(loops=-1)
    else:
        screen.blit(ImageBackground, (0, 0))
        Game_State_Text.BlitLevel(Game_State.Game_State_Level)
        Game_State_Text.BlitTanksDestroyed(Tanks_Destroyed)
        pygame.mixer.music.set_volume(1.0)
        splash_screen_background_music.stop()
        #HANDLING PLAYER LIVES
        CheckingLives()

        #UPDATE SPRITE
        PlaneContainer.update()
        TankContainer.update()
        TankBulletGroup.update()
        AliensGroup.update()

        #DRAWING
        Game_State_Images_Group.draw(screen)
        PlaneContainer.draw(screen)
        TankContainer.draw(screen)
        TankBulletGroup.draw(screen)
        Bunker_Text.BlitText()
        BunkerContainer.draw(screen)
        AliensGroup.draw(screen)
    CheckEvents()

    #PLANE DISPLAYED IMAGES, IMAGE CHANGES WITH PLANE DIRECTION AND IF PLANE HAS COLLIDED WITH UFO
    if TheFlyingPlane.speed < 2 and not TheFlyingPlane.PlaneCollided:
        TheFlyingPlane.image = TheFlyingPlane.image2
    elif TheFlyingPlane.speed < 2 and TheFlyingPlane.PlaneCollided:
        TheFlyingPlane.image = TheFlyingPlane.rotate_image_left
    elif TheFlyingPlane.speed > 1 and not TheFlyingPlane.PlaneCollided:
        TheFlyingPlane.image = TheFlyingPlane.right_image
    elif TheFlyingPlane.speed > 1 and TheFlyingPlane.PlaneCollided:
        TheFlyingPlane.image = TheFlyingPlane.rotate_image_right

    #PLANE RESPAWNING PARAMETERS
    if TheFlyingPlane.rect.y >= SCREEN_HEIGHT:
        TheFlyingPlane.plane_crash.stop()
        PlaneContainer.remove(TheFlyingPlane)
        TheFlyingPlane.rect.y = 100
        TheFlyingPlane.rect.x = 100
        TheFlyingPlane.PlaneCollided = False


    #PLANE BOMB LOGIC ONLY DROP ONE BOMB AT A TIME
    if not PlaneBombGroup: TheFlyingPlane.PlaneFired = False
    else: TheFlyingPlane.PlaneFired = True

    #BOMB MISSES TANK
    for bomb in PlaneBombGroup:
        if Bombs.rect.top > SCREEN_HEIGHT:
            PlaneBombGroup.remove(bomb)
            Bombs.bomb_drop_sound.stop()

    #DISPLAYED BOMB IMAGE IS BASED ON THE DIRECTION OF THE PLANE
    if TheFlyingPlane.speed < 2: Bombs.image = Bombs.left_image
    else: Bombs.image = Bombs.right_image

        #COLLISION HANDLING AND THE EVENTS THAT FOLLOW

    for tanks in TankContainer:
        # PLANEBOMB COLLIDE WITH TANK ONE
        if pygame.sprite.spritecollide(TankOne,PlaneBombGroup,True,collided=COLLIDED):
            if pygame.sprite.spritecollide(Bombs, TankContainer, True, collided=COLLIDED):
                Tanks_Destroyed += 1
                Bombs.bomb_drop_sound.stop()
                TankOne.TankHit_Sound.play()
            pygame.event.set_blocked(TankOneStopEvent)

        # PLANEBOMB COLLIDE WITH TANK TWO
        if pygame.sprite.spritecollide(TankTwo,PlaneBombGroup,True,collided=COLLIDED):
            if pygame.sprite.spritecollide(Bombs, TankContainer, True, collided=COLLIDED):
                Tanks_Destroyed += 1
                Bombs.bomb_drop_sound.stop()
                TankOne.TankHit_Sound.play()
            pygame.event.set_blocked(TankTwoStopEvent)

        # PLANEBOMB COLLIDE WITH TANK THREE
        if pygame.sprite.spritecollide(TankThree,PlaneBombGroup,True,collided=COLLIDED):#bomb disappear
            if pygame.sprite.spritecollide(Bombs, TankContainer, True, collided=COLLIDED):
                Tanks_Destroyed += 1
                Bombs.bomb_drop_sound.stop()
                TankOne.TankHit_Sound.play()
        pygame.event.set_blocked(TankThreeStopEvent)

    # TANK BULLET COLLIDING WITH BUNKER
    if pygame.sprite.spritecollide(Bunker_, TankBulletGroup, True):
        if not TankOne.speed: TankOne.speed -= 2
        if not TankTwo.speed: TankTwo.speed -= 2
        if not TankThree.speed: TankThree.speed -= 2
        #ADDING TO THE HIT COUNT
        Bunker_.BunkerHits += 1
    #ALIENS COLLIDE WITH PLANE
    if pygame.sprite.spritecollide(Aliens,PlaneContainer,False,collided=COLLIDED):
        Aliens.alien_sound.stop()
        AliensGroup.empty()
        Aliens.rect.x = SCREEN_WIDTH + Aliens.BeyondTheScreen
        TheFlyingPlane.plane_crash.play()
        TheFlyingPlane.PlaneCollided = True
        pygame.event.set_blocked([TankOneStopEvent, TankTwoStopEvent, TankThreeStopEvent,UFO_event,pygame.KEYDOWN])
        pygame.event.set_allowed(Spawn_Plane)
        if TheFlyingPlane.PlaneLives > 1:
            pygame.time.set_timer(Spawn_Plane,2000)


    #ALIEN MOVES OUT OF THE SCREEN, DELETE ALIEN, REPLACE ALIEN ON OPPOSITE SIDE OF SCREEN, TURN OFF ALIEN SOUND
    if Aliens.rect.x < 0:
        AliensGroup.empty()
        Aliens.rect.x = SCREEN_WIDTH + 300
        Aliens.alien_sound.stop()
        #MAKE SURE THE PLANE IS NOT AGAINST THE SCREEN BOUNDRY WHEN ALIEN ENTERS THE SCREEN
    if TheFlyingPlane.rect.x > 800 and Aliens.rect.left > SCREEN_WIDTH:
        Aliens.speed = 0

    else:
        Aliens.speed = Aliens.current_alien_speed

            ####GAMESTATE HANDLING####

    #GAME OVER
    if Bunker_.BunkerHits >= Bunker_.BunkerHitLimit or TheFlyingPlane.PlaneLives == 0:
        pygame.mixer.music.stop()
        pygame.event.set_blocked(PassLevelSound)
        pygame.event.post(pygame.event.Event(GameOver))
        Aliens.alien_sound.stop()
        BunkerContainer.remove(Bunker_)
        Game_State.GameOver = True
        pygame.event.set_blocked(
            [TankOneStopEvent, TankTwoStopEvent, TankThreeStopEvent, UFO_event])
        TankContainer.empty()
        BunkerContainer.empty()
        Game_State_Text.BlitGameOverText()
        Game_State.image = Game_State.YouLose
        Game_State_Images_Group.add(Game_State)
    ###PASSED THE LEVEL###
    if not TankContainer:
        pygame.mixer.music.stop()
        Aliens.alien_sound.stop()
        pygame.event.post(pygame.event.Event(PassLevelSound))
        pygame.event.set_blocked(
            [TankOneStopEvent, TankTwoStopEvent, TankThreeStopEvent, UFO_event,Tank_Fire_event])
        Game_State.PassedLevel = True
        TankContainer.empty()
        BunkerContainer.empty()
        PlaneContainer.empty()
        AliensGroup.empty()
        Game_State_Text.BlitGameOverText()
        Game_State_Images_Group.add(Game_State)

    clock.tick(120)
    pygame.display.flip()


