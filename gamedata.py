
import pygame

pygame.init()

background_map = [
	pygame.image.load('./image/res_img/map01.jpg')
]

panel_imgs = [
	pygame.transform.scale(pygame.image.load('./image/res_img/hp.png'),(30,30)),
	pygame.transform.scale(pygame.image.load('./image/res_img/xp.png'),(30,30)),
	pygame.transform.scale(pygame.image.load('./image/res_img/health01.png'),(30,30))
]

hero_imgs = [
	pygame.image.load('./image/res_img/hero01.png'),
	pygame.image.load('./image/res_img/hero02.png')
]

enemy_imgs = [
	pygame.image.load('./image/res_img/enemy01.png'),
	pygame.image.load('./image/res_img/enemy02.png'),
	pygame.image.load('./image/res_img/enemy03.png')
]

bullet_imgs = [
	pygame.transform.scale((pygame.image.load('./image/res_img/bullet01.png')),(15,30)),
	pygame.transform.scale((pygame.image.load('./image/res_img/bullet02.png')),(15,30))
]

blast_imgs = [
	pygame.image.load('./image/res_img/blast01.png'),
	pygame.image.load('./image/res_img/blast02.png'),
	pygame.image.load('./image/res_img/blast03.png'),
	pygame.image.load('./image/res_img/blast04.png'),
	pygame.image.load('./image/res_img/blast05.png'),
	pygame.image.load('./image/res_img/blast06.png'),
	pygame.image.load('./image/res_img/blast07.png'),
	pygame.image.load('./image/res_img/blast08.png')
]


pygame.mixer.init()
background_music = [
	pygame.mixer.music.load('./Sound/Nightwish_she_is_my_sin.mp3')
]
