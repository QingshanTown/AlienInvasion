import sys
import pygame
from pygame.constants import MOUSEBUTTONDOWN
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:    #class表示类，类的名称要首字母要大写，并且后面要加一个：
    """"管理游戏资源和行为的类"""   #单行注释用# 多行注释用三个单引号或者三个双引号
    def __init__(self):
        '''初始化游戏并创建游戏资源'''
        pygame.init()
        self.settings=Settings()    #将Settings里面的所有的函数都变为self.settings里面的函数并直接调用
        self.screen=pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
            #原代码self.screen=pygame.display.set_mode((1200,700)) #初始化要显示的窗口，设置一个surface的尺寸
        pygame.display.set_caption("Alien Invasion")    #更改surface上的标题
            #原代码self.bg_color=(230,230,230)  #设置背景色并将其赋给self.bg_color
        self.stats=GameStats(self)  #创建一个存储游戏统计信息的统计实例
        self.sb=Scoreboard(self)    #创建计分盘
        self.ship=Ship(self)    #在这里因为Ship需要一个参数ai_game，所以需要给一个参数self，在这里self指向的是AlienInvasion实例
        self.bullets=pygame.sprite.Group()  #创建一个精灵编组
        self.aliens=pygame.sprite.Group()   #创建一个精灵编组
        self._create_fleet()
        #创建play按钮
        self.play_button=Button(self,"Play") #调用Button创建一个按钮，文本是Play，并且赋给一个属性
    
    def run_game(self):
        """开启游戏主循环"""
        while True:   #while也要有：
            self._check_events()    #使用辅助方法，直接使用self.的方法来进行调用
            if self.stats.game_active:
                self._update_aliens()   #更新外星人的位置
                self.ship.update()      #更新飞船的位置
                self._update_bullets()  #更新子弹的位置并且删除消失的子弹
            self._update_screen()   #使用辅助方法，直接使用self.的方法来进行调用
                
    def _check_events(self):
         #响应按键和鼠标事件
        for event in pygame.event.get():     #从队列中获取事件，并将它存放在event列表里
            if event.type==pygame.QUIT:      #pygame.QUIT是点击surface的关闭按钮   检查队列中的某一个值得类型（.type）是不是pygame.QUIT
                sys.exit()     
            elif event.type==pygame.KEYDOWN:    #KEYDOWN是按键按下的注册事件类型
                self._check_keydown_events(event)
            elif event.type==pygame.KEYUP:  #当事件的类型是KEYUP即松开按键的时候就及时检测到事件的发生
                self._check_keyup_events(event)
            elif event.type==pygame.MOUSEBUTTONDOWN:    #用户点击屏幕的任何地方都会产生一个MOUSEBUTTONDOWN事件
                mouse_pos=pygame.mouse.get_pos()    #.get_pos()可以返回一个元组 里面包含玩家单击时鼠标的xy坐标
                self._check_play_button(mouse_pos)  #上面得到的鼠标点击位置的坐标将反馈给方法_check_play_button进一步处理
    
    def _check_play_button(self,mouse_pos):
        """单击Play时开始游戏"""
        buttom_clicked=self.play_button.rect.collidepoint(mouse_pos)    #collidepoint()可以检查鼠标单击位置是否在Play的矩形框内
        if buttom_clicked and not self.stats.game_active:   #当鼠标在play_button的范围内按下并且游戏标志处在False的时候才重置游戏信息
            self.settings.initialize_dynamic_settings() #重置游戏设置
            self.stats.reset_stats()    #重置游戏的统计信息 此时得分变为0
            self.stats.game_active=True #当满足条件之后，标志变为True游戏开始运营
            self.sb.prep_score()    #用来将开始游戏时的得分清零
            self.sb.prep_level()    #用来将开始游戏时的等级设置为1(这在reset_stats中进行设置)并进行渲染
            self.sb.prep_ships()    #用来将开始游戏时将飞船的个数重置
            #清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            #创建一群新的外星人并让飞船居中
            self._create_fleet()
            self.ship.center_ship()
            #隐藏鼠标光标
            pygame.mouse.set_visible(False) #当self.stats.game_active=True之后  游戏开始隐藏鼠标光标

    def _check_keydown_events(self,event):
        if event.key==pygame.K_RIGHT:   #event.key是用来确认具体按下的是哪个键来进行判断   pygame.K_RIGHT是右箭头键
            self.ship.moving_right=True #当按下向右的移动时标志变为True，进而在ship.py中就开始运动向右移动
        elif event.key==pygame.K_LEFT:   #event.key是用来确认具体按下的是哪个键来进行判断   pygame.K_RIGHT是右箭头键
            self.ship.moving_left=True #当按下向右的移动时标志变为True，进而在ship.py中就开始运动向右移动
        elif event.key==pygame.K_q:        #按下q就退出surfa
            sys.exit()
        elif event.key==pygame.K_SPACE:     #按下空格键就开始设计
            self._fire_bullet()
    
    def _check_keyup_events(self,event):
        if event.key==pygame.K_RIGHT:   #如果松开按键事件发生的按键是右箭头的话就执行下面的命令将标志变为False
            self.ship.moving_right=False
        elif event.key==pygame.K_LEFT:   #如果松开按键事件发生的按键是右箭头的话就执行下面的命令将标志变为False
            self.ship.moving_left=False
    
    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中"""
        if len(self.bullets)<self.settings.bullets_allowed:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)    #将创建的子弹加入到列表中，不创建的时候，列表里的元素数是0
    
    def _create_fleet(self):
        """创建外星人群"""
        #创建一个外星人并计算可以容纳多少个外星人
        #外星人的间距设置为外星人的宽度
        alien=Alien(self)   #此处也创建了一个外星人 但是此外星人不加入队列
        alien_width,alien_height=alien.rect.size    #size是一个元组包含宽度和高度两个变量，将这两个变量赋给前面的两个属性
        available_space_x=self.settings.screen_width-(2*alien_width)    #整个屏幕减去左右两边编剧所能使用的空间
        number_aliens_x=available_space_x //(2*alien_width) #整个屏幕素能承载的外星人(外星人之间的距离为一个width)
        """计算屏幕可以容纳多少行外星人"""
        ship_height=self.ship.rect.height   #将飞船的高度设置为一个def属性
        available_space_y=(self.settings.screen_height-(3*alien_height)-ship_height) #外星人高度空间是屏幕高度减去飞船高度减去上边距减去底层外星人与飞船之间的间距
        number_rows=available_space_y // (2*alien_height) #外星人上下间距等于外星人高度
        """创建外星人群"""
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number,row_number)
    
    def _create_alien(self,alien_number,row_number):
        """创建第一个外星人并且加入当前行"""
        alien=Alien(self)   #创建一个外星人
        alien_width,alien_height=alien.rect.size    #size是一个元组包含宽度和高度两个变量，将这两个变量赋给前面的两个属性
        alien.x=alien_width+2*alien_width*alien_number  #设置当前外星人的x坐标并进行赋值
        alien.rect.x=alien.x    #将小数化为整数
        alien.rect.y=alien_height+2*alien_height*row_number
        self.aliens.add(alien)    #将创建的外星人加入到列表中，不创建的时候，列表里的元素数是0
    
    def _check_fleet_edges(self):
        """检查外星人是否到达边缘并执行相应措施"""
        for alien in self.aliens.sprites(): #self.aliens.sprites()可以返回一个列表列表里包干self.aliens里面的所有精灵
            if alien.check_edges():     #查看是否有alien碰到了边缘
                self._change_fleet_direction()  #调用方法_change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """将整个外星群下移并且改变方向"""
        for alien in self.aliens.sprites(): #self.aliens.sprites()可以返回一个列表列表里包干self.aliens里面的所有精灵
            alien.rect.y += self.settings.fleet_drop_speed  #将每一个alien的y值加一(即向下移动)
        self.settings.fleet_direction*=-1   #控制方向的标志*-1改变下次的方向

    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹"""
        #更新子弹的位置
        self.bullets.update()   #因为这个self.bullets是一个编组，所以对他用update时会自动的对编组中的每一个元素使用bullet.update
                                #因为Bullets直接用super继承了sprite，在后面的fire_bullet直接将Bullet(self)产生的实例导入到了self.bullets里
                                #所以在self.bullets里的每一个元素都相当于是一个实例，可以直接用.调用bullet.py里的def
        #删除消失的子弹
        for bullet in self.bullets.copy():  #在for遍历列表的时候所遍历的列表不能有加减元素，所以用.copy(文件进行)
            if bullet.rect.bottom<=0:   #当子弹的矩形边框的下边小于屏幕的上边的时候就会从self.bullets里面被移除，从而.copy也会被重置
                self.bullets.remove(bullet)  
        self._check_bullet_alien_collisions()
        
    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人碰撞"""
        #删除发生碰撞的子弹和外星人
        #检查是否有子弹集中了外星人
        #如果是就删除相应的子弹和外星人
        collisions=pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)   #子弹和外星人相撞时，两者直接消失
        #.groupcollide可以检测两个编组(aliens)和(bullets)发生的碰撞，可以返回一个字典，里面包含相碰撞的键对值，后面的两个True可以删除发生碰撞的键对值
        if collisions:
            for aliens in collisions.values():  #values表示字典collisions里面的值
                self.stats.score+=self.settings.alien_points*len(aliens)    #如果发生了相撞，则统计里面的得分加每个外星人的分值
                                                                            #得分中每一个值都是一个列表len(aliens)表示一个值列表的长度即击杀的外星人个数
            self.sb.prep_score()    #调用函数.prep_score()用来将得分渲染成图像
            self.sb.check_high_score()  #检查是否出现了新的记录，如果是的话就更新
        if not self.aliens:
            """删除现有的子弹并且新建一批外星人"""
            self.bullets.empty()    #用方法empty删除列表里面的精灵
            self._create_fleet()
            self.settings.increase_speed()  #新建外星人的同时游戏的难度和速度提升
            self.stats.level+=1 #提高等级
            self.sb.prep_level()    #等级提高完之后就重新准备等级然后渲染等级

    def _ship_hit(self):
        """响应飞船被外星人撞到"""
        if self.stats.ships_left>0:
            #将ship.left减1并更新记分牌
            self.stats.ships_left -=1 #减少飞船的数量
            self.sb.prep_ships()    #更新左上角给穿的渲染个数
            #清空余下的外星人和子弹
            self.aliens.empty() #将外星人编组清空
            self.bullets.empty()    #将子弹编组清空
            #创建一群新的外星人并将飞船放到屏幕低端的中央
            self._create_fleet()    #创造新的外星人
            self.ship.center_ship() #调用ship中的方法来讲飞船居中
            #暂停一下
            sleep(0.5)
        else:
            self.stats.game_active=False #将stats里面的活动标志设置为False
            pygame.mouse.set_visible(True)  #游戏失败之后需要显示鼠标光标来电机Play进行重新游戏
        
    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕底端"""
        screen_rect=self.screen.get_rect() #设置屏幕参数实例
        for alien in self.aliens.sprites(): #self.aliens.sprites()可以返回一个列表列表里包干self.aliens里面的所有精灵
            if alien.rect.bottom>=screen_rect.bottom:
                #想飞船被撞一样处理
                self._ship_hit()
                break

    def _update_aliens(self):
        """检查是否有外星人处于边缘位置并更新外星人群中的所有外星人位置"""
        self._check_fleet_edges()   #检查是否有外星人碰壁
        self.aliens.update()    #此处与子弹的更新是相同的，self.aliens是一个编组里面的每一个alien都是Alien(self)生成的所以都可以调用里面的函数
        #检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
        #.spritecollideany可以检测编组(aliens)和精灵(飞船)发生的碰撞，找到与飞船碰撞的外星人之后就停止运行
            self._ship_hit()
        #检查是否有外星人到了底部
        self._check_aliens_bottom()
    
    def _update_screen(self):
        #每次循环时都重绘屏幕
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites(): #self.bullets.sprites可以返回一个列表包含所有精灵
            bullet.draw_bullet()              #调用Bullet里面的.draw_bullet()来填充子弹的颜色
        self.aliens.draw(self.screen)
        self.sb.show_score()    #将最新的得分(渲染好的图像)显示在屏幕上
        if not self.stats.game_active:  #当标志位是False的时候调用button中的绘制命令，将按钮绘制出来,当运行时只是不显示了
            self.play_button.draw_button()
        #让最近绘制的屏幕可以看见。
        pygame.display.flip()                #将完整地显示surface更新到屏幕上

        

if __name__=='__main__': #本行代码的意思是当作为Python脚本直接运行的时候此时__name__与__main__是相等的，所以运行后面的程序。
                         #而当此.py文件作为模块被import的时候此时两者不相等  所以后面的不执行。
    #创建游戏实例并运行游戏。
    #print("__name__",__name__)   #验证作为脚本直接运行时的__name__的值可以看到是等于__main__的。
    ai=AlienInvasion()
    ai.run_game()
