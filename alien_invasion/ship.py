import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """管理飞船的类"""
    def __init__(self,ai_game):
        """初始化飞船并设置其初始位置"""
        super().__init__()
        self.screen=ai_game.screen  #将屏幕赋给一个属性从而在本方法中轻松访问
        self.settings=ai_game.settings
        self.screen_rect=ai_game.screen.get_rect() #获得屏幕的属性rect
        #加载飞船图像并获取其外接矩形
        self.image=pygame.image.load('E:/Code/vscode/Python/alien_invasion/images/ship.bmp') #加载图像并将图像位置传给属性self.image，返回一个表示飞船的surface
        self.rect=self.image.get_rect() #获取self.image的surface的属性rect
        #将新飞船放置在屏幕的底部中央
        self.rect.midbottom =self.screen_rect.midbottom #右边是屏幕的底部位置，将屏幕的底部位置赋给飞船的底部中心位置
        self.x=float(self.rect.x) #在飞船属性x中存储小数值新属性
        self.moving_right = False   #移动标志开始时设置为关闭
        self.moving_left = False   #移动标志开始时设置为关闭
    
    def update(self):
        """根据移动标志调整飞船位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:  #当按下右键并且当图像的右边的值比屏幕的值小的时候才可以
            self.x +=self.settings.ship_speed #当标志位True时就开始向右移动 speed为setting里设置的值
        if self.moving_left and self.rect.left > self.screen_rect.left:    #不用elif的原因是保证两个命令的优先级是一样的，如果用elif的话将会优先执行向右的命令
            self.x -=self.settings.ship_speed #当标志位True时就开始向左移动 speed为setting里设置的值
        self.rect.x=self.x    #将self.x里面的值交给self.rect.x从而控制飞船进行移动。此时self.rect.x仍为整数，影响不大
    
    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image,self.rect)  #运用方法.blit将图像self.image绘制到self.rect的位置上去

    def center_ship(self):
        """让飞船在屏幕底部居中"""
        self.rect.midbottom =self.screen_rect.midbottom #右边是屏幕的底部位置，将屏幕的底部位置赋给飞船的底部中心位置
        self.x=float(self.rect.x) #在飞船属性x中存储小数值新属性
