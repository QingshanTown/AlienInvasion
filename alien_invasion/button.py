import pygame.font #可以让pygam将font渲染屏幕上
class Button:
    def __init__(self,ai_game,msg): #msg是要显示的文本
        """初始化按钮的属性"""
        self.screen=ai_game.screen  #将屏幕设置为一个属性
        self.screen_rect=self.screen.get_rect() #将屏幕的属性get到一个属性中
        #设置按钮的尺寸和其他属性
        self.width,self.height=200,50
        self.button_color=(0,255,0) #按钮的颜色是亮绿色
        self.text_color=(255,255,255) #字体为白色
        self.font=pygame.font.SysFont(None,48)  #渲染文本的字体是默认字体(None)大小为48字号 创建属性
        #创建按钮的rect对象，并让按钮居中
        self.rect=pygame.Rect(0,0,self.width,self.height)   #00表示矩形左上角的xy坐标，后面分别为宽和高
        self.rect.center=self.screen_rect.center    #将所设置的按钮放置在屏幕的中央位置
        #按钮的标签只创建一次
        self._prep_msg(msg) #调用函数方法_prep_msg
    
    def _prep_msg(self,msg):
        """将msg渲染为图像，并将其按在按钮上居中"""
        self.msg_image=self.font.render(msg,True,self.text_color,self.button_color)
        #将msg中的文本转换为图像，True是开启反锯齿功能，后面两个是颜色
        self.msg_image_rect=self.msg_image.get_rect() #获取转化为图像之后的文本的矩形信息
        self.msg_image_rect.center=self.rect.center     #将文本图像放在按钮的中间
    
    def draw_button(self):
        """绘制一个用颜色填充的按钮，再绘制文本"""
        self.screen.fill(self.button_color,self.rect)   #用按钮的颜色将按钮的矩形Rect填充完整
        self.screen.blit(self.msg_image, self.msg_image_rect)    #用blit将图像及图像的rect传递给程序，从而绘制文本图像 在ship.py中也有


