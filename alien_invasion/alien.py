import pygame
from pygame.sprite import Sprite

class Alien(Sprite):  #详单与Alien继承了Sprite这个类可以调用其中的函数
    """表示单个外星人的类"""
    def __init__(self, ai_game):
        """初始化外星人并设置其初始位置"""
        super().__init__() #super()表示继承关系的函数
        self.screen=ai_game.screen  #将初始化的窗口设置为本函数中的一个属性从而保证调用
        self.settings=ai_game.settings  #将setting变为一个属性
        """加载外星人图像并且设置其rect属性"""
        self.image=pygame.image.load('E:/Code/vscode/Python/alien_invasion/images/alien.bmp') #导入图片
        self.rect=self.image.get_rect() #将所导入的图片get到的属性rect变为一个函数的属性
        """每个外星人最初都在屏幕的左上角"""
        self.rect.x=self.rect.width     #左边距设置为外星人宽度
        self.rect.y=self.rect.height    #上边距设置为外星人高度
        """存储外星人的精确水平位置"""
        self.x=float(self.rect.x) #存放小数点进行设计
    
    def check_edges(self):
        """如果外星人位于屏幕边缘就返回True"""
        screen_rect=self.screen.get_rect()
        if self.rect.left<=0 or self.rect.right>=screen_rect.right:
            return True
    
    def update(self):
        """向左或向右移动外星人"""
        self.x+=(self.settings.alien_speed* self.settings.fleet_direction) #单个外星人向左或者向右移动
        self.rect.x=self.x  #将float的整数部分赋给self.rect.x

