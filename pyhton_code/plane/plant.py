'''
飞机上下左右可移动 空格开火 开火间隙合理
积分每达到一定值，可以使用伤害较高的炸弹，按b释放

敌机随机生成 每种敌机速度，子弹种类不同 共有
    1.普通弹 2.并排弹 3.散射弹

采用hp生命值机制，非一触即死，hp剩余值不同对应显示不同状态的图片,敌机、英雄生效

敌机、英雄死亡有爆炸动画，动画有时间停留 ，其中
当英雄死亡时，游戏结束，屏幕出现相应提示，玩家不可操作，画面0.5倍速播放

增加游戏音乐（Double Dragon.mp3）、击中伤害显示、游戏得分、hp显示

'''
import random as r
import pygame as pg
from pygame.sprite import Sprite, Group, groupcollide, spritecollide

SCREEN_SIZE = (480, 700)
FRAME_RATES = 60
CREATE_ENEMY_EVENT = pg.USEREVENT
CLEAR_DAMAGE_LIST = pg.USEREVENT + 1


def py_environment(func):
    def inner(*args, **kwargs):
        pg.init()
        pg.mixer.init()
        pg.font.init()
        res = func(*args, **kwargs)
        pg.quit()
        return res

    return inner


class GameSprite(Sprite):
    ImagePath = 'images/'

    def __init__(self):
        super().__init__()
        self.image = None
        self.pngs = None
        self.hp = None
        self.hpFlash = None
        self.hpCheckPoints = None
        self.live = None
        self.deathFlash = None
        self.flashInterval = FRAME_RATES // 2
        self.speed = None
        self.rect = None

    def get_image(self, imageName, rect=True):

        image = pg.image.load(GameSprite.ImagePath + imageName)
        if rect: self.rect = image.get_rect()

        return image

    def get_pngs(self, name, downs, downsName=None, setFlash=True):
        '''
        :param name:
        :param downs: (x,y) all down pngs,y the first bomb png
        :return:
        '''
        pngs = [[], []]
        pngs[0].append(name + '.png')
        x, y = downs
        if not downsName: downsName = name + '_down'

        for i in range(1, y):
            pngs[0].append(downsName + str(i) + '.png')
        for i in range(y, x + 1):
            pngs[1].append(downsName + str(i) + '.png')

        if setFlash:
            self.deathFlash = pngs[1]
            self.hpFlash = pngs[0]

        return pngs

    def set_hp(self, hp):

        if (not self.hpCheckPoints) and self.hpFlash:
            slices = hp // len(self.hpFlash)
            self.hpCheckPoints = []
            for i in range(1, len(self.hpFlash)):
                self.hpCheckPoints.append((i * slices, self.hpFlash[-i]))
        return hp

    def get_damaged(self, damage=0):
        if self.hp - damage > 0:
            self.hp -= damage
            MainGame.damageFontList.append((-damage, (self.rect.right, self.rect.centery)))
            for hp, image in self.hpCheckPoints:
                if self.hp <= hp:
                    self.image = self.get_image(image, rect=False)
                    break
        else:
            self.hp = 0
            self.kill()
            MainGame.flashGroup.add(Flash(self.rect.x, self.rect.y,
                                          self.deathFlash, self.flashInterval))
            self.live = False


class Flash(GameSprite):
    def __init__(self, x, y, flashes, interval=FRAME_RATES // 2):
        super().__init__()
        self.frame = 0
        self.time = 0
        self.interval = interval
        self.flashes = flashes
        self.image = self.get_image(self.flashes[self.frame])
        self.rect.x, self.rect.y = x, y

    def update(self, *args):
        if self.frame >= len(self.flashes):
            self.kill()
        elif self.time % self.interval == 0:
            self.image = self.get_image(self.flashes[self.frame], rect=False)
            self.frame += 1
        self.time += 1


class Hero(GameSprite):
    def __init__(self):
        super().__init__()
        self.pngs = self.get_pngs(name='me1', downs=(4, 3), downsName='me_destroy_')
        self.image = self.get_image(self.pngs[0][0])
        self.rect.x, self.rect.bottom = SCREEN_SIZE[0] // 2, SCREEN_SIZE[1]
        self.speed = (3,2)

        self.hp = self.set_hp(1000)
        self.deathFlash = self.pngs[1]
        self.flashInterval = FRAME_RATES * 2
        self.live = True

        self.fireTime = 0
        self.fireInterval = FRAME_RATES // 5  # 1秒发射子弹数目
        self.bombs=0
        self.score=0

    def move(self, direction=None):
        if self.hp <= 0: return

        if direction == 'up':  # 更新位置
            self.rect.y -= self.speed[1]
        elif direction == 'down':
            self.rect.y += self.speed[1]
        elif direction == 'left':
            self.rect.x -= self.speed[0]
        elif direction == 'right':
            self.rect.x += self.speed[0]

        if self.rect.top <= 0:  # 位置修正
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_SIZE[1]:
            self.rect.bottom = SCREEN_SIZE[1]
        elif self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= SCREEN_SIZE[0]:
            self.rect.right = SCREEN_SIZE[0]

    def fire(self):
        if self.fireTime % self.fireInterval == 0:
            MainGame.bullet_group.add(Bullet(self.rect.centerx, self.rect.top))

    def bomb(self):
        if self.bombs>0:
            self.bombs-=1
            MainGame.bomb_group.add(Bomb(self.rect.centerx,self.rect.top-1))


    def update(self, *args):
        self.fireTime += 1
        if MainGame.score-self.score>Bomb.score_cost:
            self.score=MainGame.score
            self.bombs+=1


class Bullet(GameSprite):
    def __init__(self, x, y, speed=None, damage=20, isEnemy=False):
        super().__init__()
        self.image = self.get_image('bullet1.png') if not isEnemy else self.get_image('bullet2.png')
        self.rect.x, self.rect.y = x, y
        if speed:
            self.speed = speed
        else:
            self.speed = (0, -4) if not isEnemy else (0, 4)
        self.damage = damage

    def update(self, *args):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        if self.rect.top <= 0 or \
                self.rect.left > SCREEN_SIZE[0] or self.rect.right < 0:
            self.kill()


class Bomb(GameSprite):
    score_cost=200
    def __init__(self,x,y):
        super().__init__()
        self.image=self.get_image('bomb.png')
        self.rect.x,self.rect.y=x,y
        self.speed=(0,-2)
        self.damage=500

    def move(self):
        self.rect.y+=self.speed[1]
        if self.rect.bottom<0:self.kill()

    def update(self, *args):
        self.move()


class enemy(GameSprite):
    def __init__(self, kind=1):
        super().__init__()
        downs = (4, 3) if kind != 3 else (6, 5)
        self.kind = kind
        self.score = [50, 100, 200][kind - 1]

        self.pngs = self.get_pngs(name='enemy' + str(kind), downs=downs)
        self.image = self.get_image(self.pngs[0][0])
        self.rect.x = r.randint(0, SCREEN_SIZE[0] - self.rect.size[0])

        self.hp = self.set_hp([100, 300, 900][kind - 1])
        self.live = True
        self.speed = [2, 1, 0.5][kind - 1]
        self.damage = 10 * self.kind

        self.time = 0
        self.fireInterval = FRAME_RATES // (2)

    def get_damaged(self, damage=0):
        super().get_damaged(damage)

        if not self.live:
            MainGame.score += self.score

    def move(self):
        if self.live == False: return
        self.rect.y += self.speed
        if self.rect.top >= SCREEN_SIZE[1]:
            self.kill()

    def fire(self):
        if self.time % self.fireInterval == 0 and r.random() > 0.7:
            if self.kind == 1:
                MainGame.enemy_bullet_group.add(Bullet(x=self.rect.centerx, y=self.rect.bottom, isEnemy=True))
            elif self.kind == 2:
                MainGame.enemy_bullet_group.add(Bullet(x=self.rect.centerx + 10, y=self.rect.bottom, isEnemy=True),
                                                Bullet(x=self.rect.centerx - 10, y=self.rect.bottom, isEnemy=True))
            else:

                MainGame.enemy_bullet_group.add(
                    Bullet(speed=(-1, 4), x=self.rect.left, y=self.rect.bottom, isEnemy=True),
                    Bullet(speed=(0, 4), x=self.rect.centerx, y=self.rect.bottom, isEnemy=True),
                    Bullet(speed=(1, 4), x=self.rect.right, y=self.rect.bottom, isEnemy=True), )

    def update(self, *args):
        self.time += 1
        self.move()
        self.fire()


class BackGround(GameSprite):
    def __init__(self, issecond=False):
        super().__init__()
        self.image = self.get_image('background.png')
        if issecond:
            self.rect.y = -self.rect.size[1]
        self.speed = 1

    def update(self, *args):
        self.rect.y += self.speed
        if self.rect.top == SCREEN_SIZE[1]:
            self.rect.top = -self.rect.size[1]


class GameInfo(GameSprite):
    def __init__(self, name):
        super().__init__()
        self.pngs = {'gameover': 'gameover.png', 'pause': 'pause_nor.png'}
        self.name = name
        self.image = self.get_image(self.pngs[name])
        if name == 'gameover':
            self.rect.centerx, self.rect.centery = SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2


class MainGame:
    heroGroup = Group()
    enemy_group = Group()
    bullet_group = Group()
    bomb_group=Group()
    enemy_bullet_group = Group()
    backGroundGroup = Group(BackGround(), BackGround(True))
    flashGroup = Group()
    InfoGroup = Group()

    damageFontList = []
    gameover = False
    score = 0

    def __init__(self):
        self.window = pg.display.set_mode(SCREEN_SIZE)
        self.clock = pg.time.Clock()
        self.hero = Hero()
        MainGame.heroGroup.add(self.hero)

        self.Font = None
        pg.time.set_timer(CREATE_ENEMY_EVENT, 2000)
        pg.time.set_timer(CLEAR_DAMAGE_LIST, 200)

    def music_play(self):
        pg.mixer_music.load('Double Dragon.mp3')
        pg.mixer_music.play(-1)

    @py_environment
    def start_game(self):
        self.music_play()
        while True:
            self.clock.tick(FRAME_RATES)
            self.update()

    def event_handler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                print('游戏退出')
                exit()
            elif event.type == CREATE_ENEMY_EVENT:
                res = r.random()
                if res <= 0.5:
                    MainGame.enemy_group.add(enemy(1))
                elif res <= 0.95:
                    MainGame.enemy_group.add(enemy(2))
                else:
                    MainGame.enemy_group.add(enemy(3))
            elif event.type == CLEAR_DAMAGE_LIST:
                MainGame.damageFontList.clear()

            if  event.type == pg.KEYDOWN and event.key == pg.K_b: self.hero.bomb()

        keys_pressed = pg.key.get_pressed()


        if keys_pressed[pg.K_RIGHT]:
            self.hero.move('right')
        elif keys_pressed[pg.K_LEFT]:
            self.hero.move('left')
        elif keys_pressed[pg.K_UP]:
            self.hero.move('up')
        elif keys_pressed[pg.K_DOWN]:
            self.hero.move('down')

        if keys_pressed[pg.K_SPACE]:
            self.hero.fire()


    def collide_check(self):
        enemy_damage_group=[ MainGame.bullet_group,MainGame.bomb_group]
        for group in enemy_damage_group:
            res = groupcollide(MainGame.enemy_group, group, False, True)
            for enemy,damages in res.items():
                for damage in damages:
                    enemy.get_damaged(damage.damage)


        hero_damage_group=[MainGame.enemy_group,MainGame.enemy_bullet_group]
        for group in hero_damage_group:
            res = groupcollide(group, MainGame.heroGroup, True, False)
            for enemy in res: self.hero.get_damaged(enemy.damage)


    def game_over(self):
        global FRAME_RATES
        if len(MainGame.heroGroup) == 0 and not MainGame.gameover:
            MainGame.InfoGroup.add(GameInfo('gameover'))
            MainGame.gameover = True
            FRAME_RATES //= 2

    def player_info_update(self):
        font = pg.font.SysFont('arial', 16)
        hpInfo = font.render('HP: {}'.format(self.hero.hp), True, [255, 0, 0])
        scoreInfo = font.render('SCORE: {}'.format(MainGame.score), True, [255, 0, 0])
        bombInfo=font.render('BOMBS: {}'.format(self.hero.bombs), True, [255, 0, 0])
        self.window.blit(hpInfo, (0, 0))
        self.window.blit(scoreInfo, (0, 20))
        self.window.blit(bombInfo, (0, 40))

        damageFont = pg.font.SysFont('arial', 20, True)
        for damage, cordial in MainGame.damageFontList:
            damageInfo = damageFont.render('hit:{}'.format(damage), True, [255, 0, 0])
            self.window.blit(damageInfo, cordial)

    def update(self):
        self.event_handler()
        self.collide_check()
        self.game_over()

        groups = [MainGame.backGroundGroup, MainGame.heroGroup, MainGame.enemy_group,
                  MainGame.bullet_group, MainGame.enemy_bullet_group, MainGame.flashGroup,
                  MainGame.bomb_group,MainGame.InfoGroup]

        for group in groups:
            group.update()
            group.draw(self.window)
        self.player_info_update()

        pg.display.update()


if __name__ == '__main__':
    mainGame = MainGame()
    mainGame.start_game()
