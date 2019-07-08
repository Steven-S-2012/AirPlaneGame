

import pygame
from pygame.locals import *
import time
import random
import math
import copy
import os
import sys

from gamedata import *

blast_list = pygame.sprite.Group()

hero_list = pygame.sprite.Group()

enemy_list = pygame.sprite.Group()

bullet_list_hero = pygame.sprite.Group()

bullet_list_enemy = pygame.sprite.Group()


# 游戏背景地图类
class BackGround:
	'''
	创建游戏地图背景，并使之自动下移
	'''
	# class 初始化
	def __init__(self,image,speed,screen):
		self.image1 = image
		self.image2 = copy.copy(self.image1)
		self.img1_rect = self.image1.get_rect()
		self.img1_rect.y = screen.get_height()-background_map[0].get_height()
		self.img2_rect = self.image2.get_rect()
		self.img2_rect.y = -886

		self.speed = speed
		self.screen = screen

	def move(self):
		self.img1_rect = self.img1_rect.move(0,self.speed)
		self.img2_rect = self.img2_rect.move(0,self.speed)
		if self.img1_rect.y >= 650:
			self.img1_rect.y = -118
			self.img2_rect.y = -886

		self.screen.blit(self.image1,self.img1_rect)
		self.screen.blit(self.image2,self.img2_rect)

# 游戏界面及积分界面
class Panel:
	'''
	游戏室显示游戏界面：英雄血量和积分
	结束时显示总积分和最高积分
	'''
	def __init__(self,screen,imgs=[]):
		self.screen = screen
		self.imgs = imgs


	def gamePanel(self,heroInstance):
		hpSurface = self.screen.blit(self.imgs[0],(2,2))
		xpSurface = self.screen.blit(self.imgs[1],(2,4+self.imgs[0].get_height()))
		if hero_list:
			for i in range(0,heroInstance.hp):
				self.screen.blit(self.imgs[2],(4+self.imgs[0].get_width()+self.imgs[2].get_width() * i , 2))

		gamefont = pygame.font.Font('./font/Marker Felt.ttf',35)
		scorePane = gamefont.render('%s' % heroInstance.score, True, (255, 125, 125,0))
		
		self.screen.blit(scorePane,((4+self.imgs[1].get_width()), (4+self.imgs[0].get_height())))

	def endPanel(self,heroInstance):
		
		s = pygame.Surface((400,500))
		s.fill((221,221,221))
		s.set_alpha(100)
		
		endfont = pygame.font.Font('./font/Marker Felt.ttf',40)
		text1 = endfont.render('Your score: %s' % heroInstance.score, True, (5,5,5))
		if HistoryScore.history == 0:
			HistoryScore.history = heroInstance.score
			atTime = time.strftime('%m-%d-%Y %H:%M:%S',time.localtime(time.time()))
			HistoryScore.day,HistoryScore.tm = atTime.split(' ')

		text2 = endfont.render('Max score: %s' % HistoryScore.history, True, (5,5,5))
		text3 = endfont.render('At: %s' % HistoryScore.tm, True, (5,5,5))
		text4 = endfont.render('     %s' % HistoryScore.day, True, (5,5,5))

		s.blit(text1,(50,50))
		s.blit(text2,(50,150))
		s.blit(text3,(50,250))
		s.blit(text4,(50,350))
		self.screen.blit(s,(56,75))

class Blast(pygame.sprite.Sprite):
	'''
	创建爆炸类
	'''
	def __init__(self,screen,position,imgs = blast_imgs):
		pygame.sprite.Sprite.__init__(self)
		self.screen = screen
		self.imgs = imgs
		self.image = self.imgs[0]
		self.rect = self.image.get_rect()
		self.rect.center = position
		self.timeTick = 0

	def regist(self):
		blast_list.add(self)

	def update(self):
		if self.timeTick % 3 == 0:
			imgIndex = self.timeTick // 3
			self.image = self.imgs[imgIndex]
		self.timeTick += 1
		if self.timeTick == 23:
			self.timeTick = 0	
			blast_list.remove(self)

class BackgroundMusic:
	@staticmethod
	def play_music(sound):
		if pygame.mixer.music.get_busy() == 0:
			pygame.mixer.music.play(loops=0, start=0.0)

# 英雄飞机类
class Hero(pygame.sprite.Sprite):
	'''
	创建英雄飞机，
	并定义对应的控制事件
	对敌机和敌机的子弹碰撞检测
	'''
	# 定义类属性
	up = False
	down = False
	left = False
	right = False
	fight = False
	flag = True
		

	# class初始化
	def __init__(self,screen,imgs,position,speed=5,hp=5):
		pygame.sprite.Sprite.__init__(self)
		self.screen = screen
		self.imgs = imgs 
		# 随机英雄飞机样式
		self.image = self.imgs[0]
		self.mask = pygame.mask.from_surface(self.image)
		self.rect = self.image.get_rect()
		self.rect.topleft = position
		self.hp = hp
		self.speed = speed
		self.timeTick = 0
		self.score = 0

	def regist(self):
		hero_list.add(self)

	def update(self):
		self.move()

		# 执行碰撞检测(子弹)
		self.collision(bullet_list_enemy)	
		# 执行碰撞检测(敌机)		
		self.collision(enemy_list)

		self.checkStatus()


	def move(self):
		# 移动控制
		
		if Hero.right:
			print('right')
			self.rect = self.rect.move(self.speed,0)
		if Hero.left:
			print('left')
			self.rect = self.rect.move(-self.speed,0)
		if Hero.down:
			print('down')
			self.rect = self.rect.move(0, self.speed)
		if Hero.up:
			print('up')
			self.rect = self.rect.move(0, -self.speed)
		if Hero.fight:
			print('fire')
			self.fire()

		# 范围约束
		if self.rect.x <= 0:
			self.rect.x = 0
		if self.rect.x >= (self.screen.get_width() - self.image.get_width()):
			self.rect.x = self.screen.get_width() - self.image.get_width()
		if self.rect.y <= 0:
			self.rect.y = 0
		if self.rect.y >= (self.screen.get_height() - self.image.get_height()):
			self.rect.y = self.screen.get_height() - self.image.get_height()

		

	def checkStatus(self):
		# 检测是否空血		
		if self.hp == 0:
			Blast(self.screen, self.rect.center).regist()
			HistoryScore.updateScore(self.score)
			hero_list.remove(self)


		else:
			self.display()



	def fire(self):
		# 开火延迟
		self.timeTick += 1
		if self.timeTick == 3:
			self.timeTick = 0
			Bullet(self.screen,bullet_imgs[0],
				(self.rect.centerx, (self.rect.y - self.image.get_height() / 10)),
				10,self,Hero.flag).regist()


	def collision(self,target):
		# 碰撞检测,attribute 为自身和对象sprite组
		if target == bullet_list_enemy:
			collidedBullet = pygame.sprite.spritecollide(self,target,True,collided=pygame.sprite.collide_mask)
			if collidedBullet and isinstance(collidedBullet[0],Bullet) :
				self.hp -= 1
		else:
			collidedEnemy = pygame.sprite.spritecollideany(self,target,collided=pygame.sprite.collide_mask)
			if collidedEnemy and isinstance(collidedEnemy,Enemy):
				collidedEnemy.hp = 0				
				self.hp = 0
				self.score += collidedEnemy.score

	def display(self):
		self.screen.blit(self.image,self.rect)


# 敌人飞机类
class Enemy(pygame.sprite.Sprite):
	'''
	构建敌机类
	对英雄飞机子弹的碰撞检测
	'''
	def __init__(self,screen,img,position,flag,speed,hp,score):
		pygame.sprite.Sprite.__init__(self)
		self.screen = screen
		self.image = img
		self.mask = pygame.mask.from_surface(self.image)
		self.rect = self.image.get_rect()
		self.rect.topleft = position
		self.hp = hp
		self.speed = speed
		self.flag = flag
		self.score = score

	def display(self):
		# for b in bullet_list_enemy:
		# 	b.display()
		self.screen.blit(self.image,self.rect)	

	def regist(self):
		enemy_list.add(self)

	def remove(self):
		enemy_list.remove(self)

	def update(self):
		self.move()
		self.fire()

		# 执行碰撞检测(子弹)
		self.collideBullet()
		

		self.checkStatus()

	def move(self):
		# 移动敌机
		self.rect = self.rect.move(0,self.speed)

		# 检测是否飞出屏幕
		if self.rect.y >= 660:
			if self in enemy_list and self != None:
				enemy_list.remove(self)

	def checkStatus(self):
		
		# 检测是否空血
		if self.hp == 0:
			Blast(self.screen, self.rect.center).regist()

			enemy_list.remove(self)
			

		
	def fire(self):
		# 开火延迟
		randomTick = random.randint(0,120)
		if randomTick  == 88:    		
			Bullet(self.screen,bullet_imgs[1],
				(self.rect.centerx, (self.rect.bottom + self.image.get_height() / 2)),
				8,self,self.flag).regist()

	def collideBullet(self,target=bullet_list_hero):
		#碰撞检测,attribute 为自身和对象sprite组		
		collidedTarget = pygame.sprite.spritecollideany(self,target,collided=pygame.sprite.collide_mask)
		if collidedTarget and self in enemy_list:			
			self.hp -= 1
			
			if self.hp == 0:
				
				Blast(self.screen, self.rect.center).regist()
				collidedTarget.belongsto.score += self.score
				enemy_list.remove(self)
			bullet_list_hero.remove(self)

class EnemyFactory:
	'''
	根据Enemy类随机创建敌机
	'''
	@staticmethod
	def createEnemy(screen):
		r = random.randint(1,15)
		if r % 7 == 0:
			Enemy(screen,enemy_imgs[0],(random.randint(0, 400),-90),False,speed=4,hp=4,score=4).regist()
		elif r % 5 == 0:
			Enemy(screen,enemy_imgs[1],(random.randint(0, 420),-90),False,speed=5,hp=5,score=5).regist()
		elif r % 3 == 0:
			Enemy(screen,enemy_imgs[2],(random.randint(0, 410),-90),False,speed=3,hp=3,score=3).regist()



# 子弹类
class Bullet(pygame.sprite.Sprite):
	'''
	创建子弹类
	'''
	def __init__(self,screen,img,position,speed,belongtoInstance,flag=True):
		pygame.sprite.Sprite.__init__(self)
		self.screen = screen
		self.image = img
		self.mask = pygame.mask.from_surface(self.image)
		self.rect = self.image.get_rect()
		self.rect.center = position
		self.speed = speed
		self.flag = flag
		self.belongsto = belongtoInstance

	def regist(self):
		if self.flag:
			bullet_list_hero.add(self)
		else:
			bullet_list_enemy.add(self)

	def update(self):
		if self.flag:
			self.rect = self.rect.move(0,-self.speed)
			if self.rect.y <= -40:
				bullet_list_hero.remove(self)
		else:
			self.rect = self.rect.move(0,self.speed)
			if self.rect.y >= 700:
				bullet_list_enemy.remove(self)

class HistoryScore:
	'''
	记录历史分数，显示最高分
	'''
	history = 0
	logTime = ''
	day = ''
	tm = ''

	# 记录历史分数
	def updateScore(score,path='./score.txt'):
		atTime = time.strftime('%m-%d-%Y %H:%M:%S',time.localtime(time.time()))
		strScore = str(score)
		data = atTime + ' : ' + strScore

		if os.path.exists(path):
			HistoryScore.loadScore()
			if score >= HistoryScore.history:
				with open(path,mode='w') as fp:
					fp.write(data)

		else:
			with open(path,mode='x') as fp:
				fp.write(data)

	def loadScore(path='./score.txt'): 
		if os.path.exists(path):
			with open(path,mode='r') as fp:
				fr = fp.read()
				strIndex = fr.rindex(' ')
				HistoryScore.history = int(fr[(strIndex + 1):])
				HistoryScore.logTime = fr[:(strIndex - 2)]
				HistoryScore.day,HistoryScore.tm = HistoryScore.logTime.split(' ')
		else:
			HistoryScore.updateScore()

def eventListener(screen):
	'''
	K_w
	K_s
	K_a
	K_d
	K_UP                  up arrow
	K_DOWN                down arrow
	K_RIGHT               right arrow
	K_LEFT   			  left arrow	
	K_SPACE               fire
	'''	
	for i in pygame.event.get():
		#判断是否退出
		if i.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		# 方向按键互锁
		if i.type == pygame.KEYDOWN:
			a = pygame.key.get_pressed()

			if i.key == pygame.K_w or i.key == pygame.K_UP:
				Hero.up = True	

			if i.key == pygame.K_s or i.key == pygame.K_DOWN:
				Hero.down = True

			if i.key == pygame.K_a or i.key == pygame.K_LEFT:
				Hero.left = True

			if i.key == pygame.K_d or i.key == pygame.K_RIGHT:
				Hero.right = True

			if i.key == pygame.K_SPACE:
				Hero.fight = True

		if i.type == pygame.KEYUP:
			if i.key == pygame.K_w or i.key == pygame.K_UP:
				Hero.up = False	
			if i.key == pygame.K_s or i.key == pygame.K_DOWN:
				Hero.down = False
			if i.key == pygame.K_a or i.key == pygame.K_LEFT:
				Hero.left = False
			if i.key == pygame.K_d or i.key == pygame.K_RIGHT:
				Hero.right = False	
			if i.key == pygame.K_SPACE:
				Hero.fight = False	

		if i.type == pygame.USEREVENT + 1:
			EnemyFactory.createEnemy(screen)


def main():

	
	# 初始化pygame
	pygame.init()
	pygame.display.init()

	# 创建游戏窗口
	screen = pygame.display.set_mode((512,650),0,0)
	pygame.display.set_caption('飞机大战')

	# 创建一个游戏背景
	backgroundInstance = BackGround(background_map[0], 2, screen)

	# 创建英雄飞机
	hero = Hero(screen, hero_imgs, (200,500))
	hero.regist()

	# 创建界面
	panelIns = Panel(screen,panel_imgs)

	# 播放音乐
	BackgroundMusic.play_music(background_music)

	# 设置任务计时器
	pygame.time.set_timer(pygame.USEREVENT + 1, 500)
	
	# 设置计时器
	clock = pygame.time.Clock()

	ending = False

	#循环显示
	while True:
		#开启时间监控
		eventListener(screen)
	
		# 移动背景画面
		backgroundInstance.move()

		if ending == True:
			panelIns.endPanel(hero)

		else:
			# 绘制游戏元素		
			enemy_list.update()
			bullet_list_enemy.update()
			bullet_list_hero.update()
			blast_list.update()

			hero_list.update()
			hero_list.draw(screen)
			panelIns.gamePanel(hero)	
			enemy_list.draw(screen)
			bullet_list_enemy.draw(screen)
			bullet_list_hero.draw(screen)
			blast_list.draw(screen)
			if len(blast_list) == 0:
				if len(hero_list) == 0:
					ending = True		

		pygame.display.update()

		clock.tick(30)

if __name__ == '__main__':
	main()