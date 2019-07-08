
import pygame
import random
 

SCREEN_WIDTH  = 700
SCREEN_HEIGHT = 500
 
# 敌机类
class Heart(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.image = self.image = pygame.transform.scale(pygame.image.load('./image/res_img/health01.png'),(22,22))
        self.rect = self.image.get_rect()
 
    # 更新坐标
    def reset_pos(self):
        self.rect.y = random.randrange(-300, -20)
        self.rect.x = random.randrange(SCREEN_WIDTH)        
 
    # 自动移动
    def update(self):
        self.rect.y += 1
        if len(game.heart_list) <= 25:
            self.rect.y += 2
         
        if self.rect.y > SCREEN_HEIGHT + self.rect.height:
            self.reset_pos()
 
# 英雄类
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.Surface([20,20])
        self.image.fill(( 255,   0,   0))
        self.rect = self.image.get_rect()
 

# 游戏本体
class Game():
    '''
    游戏本体，初始化参数，监控事件，
    '''
    def __init__(self):
        self.score = 0
        self.gaming = False
        self.ending = True

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        pygame.display.set_caption("My Game")
        pygame.mouse.set_visible(False)
         
        # 初始化列表
        self.heart_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()

        self.clock = pygame.time.Clock() 

        # 创建敌机
        for i in range(50):
            heart = Heart()         
            heart.rect.x = random.randrange(SCREEN_WIDTH)
            heart.rect.y = random.randrange(-300,SCREEN_HEIGHT)
             
            self.heart_list.add(heart)
         
        # 创建英雄
        self.player = Player()

    # 事件监听器
    def eventListener(self):
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.ending = False

            if event.type == pygame.MOUSEMOTION:
                self.player.rect.center = event.pos

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.gaming:
                    self.__init__()
         
        return False
 
    # 更新状态
    def updateStatus(self):
         
        if not self.gaming:
            # 移动敌机
            self.heart_list.update()
             
            # 碰撞检测
            hearts_hit_list = pygame.sprite.spritecollide(self.player, self.heart_list, True)  
          
            # 数目检测
            for heart in hearts_hit_list:
                self.score +=1
                print( self.score )
                 
            if len(self.heart_list) == 0:
                self.gaming = True
                      
    # 结束表盘
    def display_frame(self):
 
        self.screen.fill(( 255, 255, 255))
         
        if self.gaming:
            font = pygame.font.SysFont("serif", 25)
            text = font.render("Game Over, click to restart", True, (   0,   0,   0))
            x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            self.screen.blit(text, [x, y])
         
        if not self.gaming:
            self.heart_list.draw(self.screen)
            self.screen.blit(self.player.image,self.player.rect) 

    # 运行程序
    def run(self):
    	while self.ending:
    		self.eventListener()
    		self.updateStatus()
    		self.display_frame()
    		self.clock.tick(50)
    		pygame.display.flip()


# 主程序
if __name__ == "__main__":
    
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()