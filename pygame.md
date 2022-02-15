## pygame

* 安装：`pip install pygame`，以下便于阐述称呼其为`pg`
* [飞机大战项目](./pyhton_code) 

### 全局设置

* 初始化和正常退出：以`pg.init()`和`pg.quit()`包裹游戏代码，可以使用装饰器。

  ```python
  def py_environment(func):
      def inner(*args,**kwargs):
          pg.init()
          res=func(*args,**kwargs)	#正常游戏代码
          pg.quit()
          return res
      return inner
  ```

  

* 帧率设置：指定每秒刷新的频率。先创建时钟对象，然后调用类方法，效果可以理解成`time.sleep()`。**游戏动画的设计正是依托每帧的图形变化给人带来的视觉效果。**  

  ```python
  clock=pg.time.Clock()	#创建时钟对象
  while True:	
      clock.tick(60)	#每秒刷新60
      pass	#游戏代码
  ```

* 音乐加载：

  ```python
  pg.music.init()	#必须要先初始化
  pg.mixer_music.load('Double Dragon.mp3')	#音乐文件
  pg.mixer_music.play(-1)	#-1表示循坏播放
  ```

  

### 图像绘制

* 游戏窗口绘制：`screen=pg.display.set_mode((width,height))`，使用`display`模块创建指定大小的游戏窗口对象，**随后其他元素的绘制都在该窗口对象，所以是所有绘制步骤之首**。

  * 游戏坐标系：原点在左上角，向右x轴正方向，向下y轴正方向。

* 图片加载：`image=pg.image.load(路径)`，将图片资源从磁盘加载到内存，生成1个图片对象。

* 游戏对象绘制：调用游戏窗口对象的实例方法`blit(图片对象,坐标)`方法绘制图像，坐标可以是2元组`(x,y)`或者`Rect`类。

  ```python
  bg=pg.image.load(路径)	#创建图像对象
  screen.blit(bg,(0,0))	#描绘图形到游戏窗口的指定位置 
  ```

* 矩形绘制：`pg.Rect(x,y,width,height)`，是一个类，`（x,y）`为矩形左上角。**pygame以矩形来表示游戏对象的位置**。 

  ```python
  #Rect类提供的常用属性
  '''
  bottom top	矩形底部、上部位置
  centerx centery 矩形中心的x、y坐标
  left right矩形的左右边界坐标
  size 返回矩形的尺寸大小，二元组
  '''
  
  hero = pg.image.load('image\me1.png')
  hero_rect = pg.Rect(240,500, 102,216)	
  screen.blit(hero,hero_rect)
  ```

  

* 字体渲染：可以使用`pg.font.get_fonts()`查看可用字体

  ```python
  pg.font.init()	#必须先初始化
  font = pg.font.SysFont('arial', 16,False)	#采用系统字体，生成字体对象，字体+大小+是否斜体
  hpInfo = font.render('HP: {}'.format(self.hero.hp), True, [255, 0, 0])	#渲染，True表示开启抗锯齿，[R,G,B]颜色数组
  screen.blit(hpInfo, (0, 0))	#绘制栅格化后的字体
  ```

  

* 更新渲染：`pg.display.update()`，弹出画布。相当于`matpplot.plot.show()`，是所有绘制步骤之尾。pygame按照`screen.blit()`的顺序或者`group.draw()`的顺序依次更新渲染，所以要注意绘制顺序，类似PS里的图层顺序。

### 事件捕获

* 事件捕获：`pg.event.get()`，捕获该帧下的事件列表。事件列表可以是外设的输入、定时器的定时事件触发。不能连续两次捕获，否则后者会清空前者。判断时使用`event.type`获取事件类型。

  ```python
  for event in pg.event.get():	#返回1个列表
      if event.type==pg.QUIT:	#pg的全局变量，QUIT=12
          print('游戏退出')
          exit()
      else:
              pass
  ```

  

* 键盘捕获的两种方式：

  ```python
  #键盘按下弹起才触发
  if  event.type == pg.KEYDOWN and event.key == pg.K_b: 
      pass	#do something
  
  #键盘只要按下就触发
  #获取当前状态下所有按下的按键，是1个列表，下标是pygame里相应按键的宏
  keys_pressed = pg.key.get_pressed()	
  if  keys_pressed[pg.K_RIGHT]:	#如果按下了方向键右
      pass
  ```

### 定时器

* 定时事件：使用`time`模块设置定时器，pygame会自动触发事件。随后，使用事件捕获自定义事件即可。定时器触发的事件应当是一些全局性的事件，如定时刷新敌人等。若要每个对象个体定时触发事件，应当在对象内部自定义1个时钟判断。可以认为，`time`的时钟是同步时间，而类本身的时钟是异步事件。

  ```python
  pg.time.set_timer(CREATE_ENEMY_EVENT, 2000)
  for event in pg.event.get():
      if event==USER_EVENT:
          pass	#do something here
      
  class enemy:
      def __init__(self):
          self.time=0
      def update(self):
          self.time+=1
          if self.time%2==0:	#每隔2帧就 触发
              pass #do something 
  ```

* 自定义事件：`USER_EVNET=pg.USEREVENT`，随后只要顺序+1即可，不会出现事件冲突，如`USER_EVNET2=pg.USEREVENT+1` 。

### 游戏精灵

* 游戏精灵：pg为可视化图形提供的类`Sprite(object)`。用户应当继承该类，将2个最重要的属性`self.image`、`self.rec`捆绑在一起，并自行添加对象属性。

```python
from pygame.sprite import Sprite, Group, groupcollide, spritecollide
class Sprite(object):
    """simple base class for visible game objects

    pygame.sprite.Sprite(*groups): return Sprite

    The base class for visible game objects. Derived classes will want to
    override the Sprite.update() method and assign Sprite.image and Sprite.rect
    attributes.  The initializer can accept any number of Group instances that
    the Sprite will become a member of.

    When subclassing the Sprite class, be sure to call the base initializer
    before adding the Sprite to Groups.

    """
    def kill(self):
        """remove the Sprite from all Groups

        Sprite.kill(): return None

        The Sprite is removed from all the Groups that contain it. This won't
        change anything about the state of the Sprite. It is possible to
        continue to use the Sprite after this method has been called, including
        adding it to Groups.

        """
        pass
    
class GameSprite(Sprite):
    def __init__(self):
        super().__init__()	#调用父类的初始化方法
        self.image=None
        self.rect=None
        self.hp=100	#自创其他属性
    def update(self):
        pass
    def kill(self):
        pass
    def get_image(self, imageName, rect=True):	#自动更新组内的rect和image 
        image = pg.image.load(GameSprite.ImagePath + imageName)
        if rect: self.rect = image.get_rect()

        return image
```

* Group：若干精灵（Sprite）的集合，借用组的概念，可以方便地批量更新（update）、批量绘制（draw）、碰撞检测。若有对象消亡时，可以简单地从组中移除该精灵来实现，而该精灵的实际对象依然存在，没有被回收，后续的调用不会出错。

  ```python
  from pygame.sprite import Sprite, Group, groupcollide, spritecollide
  
  #碰撞检测
  enemy_damage_group=[ MainGame.bullet_group,MainGame.bomb_group]
  for group in enemy_damage_group:
      res = groupcollide(MainGame.enemy_group, group, False, True)	#True表示碰撞到就从该组移除，groupcollide返回1个字典，key是第1组中碰撞的对象，val是与第2组与key相碰撞的精灵列表
      for enemy,damages in res.items():	#字典
          for damage in damages:	#列表
              enemy.get_damaged(damage.damage)
              
  #批量更新 批量绘制
  groups=[enemy_group,hero_group]
  for group in groups:
      group.update()	#会依次调用组内精灵各自的update
      group.draw(self.screen)	#会依次将组内精灵各自的rect绘制到屏幕上 
  ```

  

### 游戏框架

* 全局数据应当设计成类属性，便于读写。根据职责设计各个游戏对象，如果可分离，则当分离。

```python
import pygame as pg
from pygame.sprite import Sprite, Group, groupcollide, spritecollide

SCREEN_SIZE = (480, 700)	#游戏窗口大小
FRAME_RATES = 60	#帧率
CREATE_ENEMY_EVENT = pg.USEREVENT	#自定义事件 

def py_environment(func):	#定义装饰器，初始化游戏属性
    def inner(*args, **kwargs):
        pg.init()
        pg.mixer.init()
        pg.font.init()
        res = func(*args, **kwargs)
        pg.quit()
        return res

    return inner

class GameSprite(Sprite):	#定义游戏精灵
    

class MainGame:
    itemsGroup=group()	#声明空组，在游戏的过程中添加
	def __init__(self):
        self.window = pg.display.set_mode(SCREEN_SIZE)	#游戏窗口
        self.clock = pg.time.Clock()	#帧率刷新
        self.hero = Hero()
        MainGame.heroGroup.add(self.hero)	#修改游戏全局数据，类属性

        pg.time.set_timer(CREATE_ENEMY_EVENT, 2000)	#设定定时器
  	
    def event_handler(self):	#事件捕获
    	pass
    
    def collide_check(self):	#碰撞检测
        pass
    
    def update(self):
        self.event_handler()
        self.collide_check()
        pass
    	pg.display.update()	#更新所有对象 
    
    def start_game(self):
        while True:
            self.clock.tick(FRAME_RATES)
            self.update()	#更新各类对象
            
    def game_over(self):
        pass
    
if __name__ == '__main__':
    mainGame = MainGame()
    mainGame.start_game()
```

