class GameStats:
    """跟踪游戏信息"""
    def __init__(self,ai_game):
        """初始化统计信息"""
        self.settings=ai_game.settings
        self.reset_stats()
        #游戏刚启动时处于活动状态
        self.game_active=False
        self.high_score=9999990   #任何情况下都不能重置最高得分
    
    def reset_stats(self):
        """初始化在游戏运行期间可能出现的统计信息"""
        self.ships_left=self.settings.ship_limit    #在游戏开始时就运行复位程序
        self.score=0    #在reset_stats中设置的原因是每次开始游戏都重置得分
        self.level=1    #设置初始等级并且在每次开始游戏的时候重置他