import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    """显示得分信息的类"""
    def __init__(self,ai_game):
        """初始化显示得分涉及的属性"""
        self.ai_game=ai_game
        self.screen=ai_game.screen
        self.screen_rect=ai_game.screen.get_rect()
        self.settings=ai_game.settings
        self.stats=ai_game.stats
        #显示得分信息时使用的字体设置
        self.text_color=(30,30,30)
        self.font=pygame.font.SysFont(None,48)  #渲染文本的字体是默认字体(None)大小为48字号 创建属性
        #准备初始得分图像以及最高得分图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
    
    def prep_ships(self):
        """显示还余下多少艘飞船"""
        self.ships=Group()  #创建一个空的编组用来存储飞船
        for ship_number in range(self.stats.ships_left):    #用来运行剩余飞船数量的循环次数
            ship=Ship(self.ai_game)
            ship.rect.x=10+ship_number*ship.rect.width  #设置每艘飞船的左右位置
            ship.rect.y=10  #设置每艘飞船的上下位置
            self.ships.add(ship)    #将所有的新飞船编到编组里面去
            
    
    def prep_level(self):
        """将等级转换为渲染的图像"""
        level_str=str(self.stats.level)    #将self.stats.level变为字符串从而进行输入
        self.level_image=self.font.render(level_str,True,self.text_color,self.settings.bg_color)
        #将level_str中的文本转换为图像，True是开启反锯齿功能，后面两个是颜色，一个是文本颜色，一个是背景颜色
        #将等级放在得分的下方
        self.level_rect=self.level_image.get_rect() #拾取等级图像的矩形边框
        self.level_rect.right=self.score_rect.right     #设置等级图像的左右位置
        self.level_rect.top=self.score_rect.bottom +10  #设置等级图像的上下位置
    
    def prep_score(self):
        """将得分渲染为图像"""
        rounded_score=round(self.stats.score,-1)    #将self.stats.score舍入到十位(-1是十位，1是小数点后一位)
        score_str="{:,}".format(rounded_score)  #在rounded_score中插入,
        self.score_image=self.font.render(score_str,True,self.text_color,self.settings.bg_color)
        #将score_str中的文本转换为图像，True是开启反锯齿功能，后面两个是颜色，一个是文本颜色，一个是背景颜色
        #在屏幕右上角显示得分
        self.score_rect=self.score_image.get_rect() #拾取得分图像的矩形边框
        self.score_rect.right=self.screen_rect.right-20 #设置得分图像的左右位置
        self.score_rect.top=20  #设置得分图像的上下位置
    
    def prep_high_score(self):
        """将得分渲染为图像"""
        high_score=round(self.stats.high_score,-1)    #将self.stats.high_score舍入到十位(-1是十位，1是小数点后一位)
        score_str="{:,}".format(high_score)  #在rounded_score中插入,
        self.high_score_image=self.font.render(score_str,True,self.text_color,self.settings.bg_color)
        #将score_str中的文本转换为图像，True是开启反锯齿功能，后面两个是颜色，一个是文本颜色，一个是背景颜色
        #将最高得分放在屏幕顶部中央
        self.high_score_rect=self.score_image.get_rect() #拾取得分图像的矩形边框
        self.high_score_rect.centerx=self.screen_rect.centerx #设置得分图像的左右位置
        self.high_score_rect.top= self.score_rect.top #设置得分图像的上下位置

    def show_score(self):
        """在屏幕上显示得分、等级以及剩余的飞船数"""
        self.screen.blit(self.score_image,self.score_rect)  #用blit将图像及图像的rect传递给程序，从而在rect处绘制图像
        self.screen.blit(self.high_score_image,self.high_score_rect)  #用blit将图像及图像的rect传递给程序，从而在rect处绘制图像
        self.screen.blit(self.level_image,self.level_rect)  #用blit将图像及图像的rect传递给程序，从而在rect处绘制图像
        self.ships.draw(self.screen)    #将飞船绘制在屏幕上给
    
    def check_high_score(self):
        """检查是否诞生了新的最高得分"""
        if self.stats.score>self.stats.high_score:
            self.stats.high_score=self.stats.score  #更新最高得分
            self.prep_high_score()

        
    
