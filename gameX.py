import pygame
import random
import time

pygame.mixer.init(44100, -16,2,2048) #Чтобы работали звуки(с форума)
pygame.init()

walkRight = [pygame.image.load('sprites/right_1.png'), pygame.image.load('sprites/right_2.png'), #Анимации
pygame.image.load('sprites/right_3.png'), pygame.image.load('sprites/right_4.png'), 
pygame.image.load('sprites/right_5.png'), pygame.image.load('sprites/right_6.png')]

walkLeft = [pygame.image.load('sprites/left_1.png'), pygame.image.load('sprites/left_2.png'),
 pygame.image.load('sprites/left_3.png'), pygame.image.load('sprites/left_4.png'), 
 pygame.image.load('sprites/left_5.png'), pygame.image.load('sprites/left_6.png')]

enemywalkRight = [pygame.image.load('sprites/zombie_right1.png'),pygame.image.load('sprites/zombie_right2.png'),
pygame.image.load('sprites/zombie_right3.png'),pygame.image.load('sprites/zombie_right4.png'),
pygame.image.load('sprites/zombie_right5.png'),pygame.image.load('sprites/zombie_right6.png'),
pygame.image.load('sprites/zombie_right7.png'),pygame.image.load('sprites/zombie_right8.png')]

enemywalkLeft = [pygame.image.load('sprites/zombie_left1.png'),pygame.image.load('sprites/zombie_left2.png'),
pygame.image.load('sprites/zombie_left3.png'),pygame.image.load('sprites/zombie_left4.png'),
pygame.image.load('sprites/zombie_left5.png'),pygame.image.load('sprites/zombie_left6.png'),
pygame.image.load('sprites/zombie_left7.png'),pygame.image.load('sprites/zombie_left8.png'),]

bg = pygame.image.load('sprites/bg.jpg')

playerStand = pygame.image.load('sprites/idle.png')

brain = pygame.image.load('sprites/brain.png')

loosebg = pygame.image.load('sprites/loose.png')
try:
	pistolsound = pygame.mixer.Sound('sounds/pistol.ogg')
	zombiesound = pygame.mixer.Sound('sounds/zombie.ogg')
	punchsound = pygame.mixer.Sound('sounds/hit1.ogg')
except pygame.error:
	print('Звук не загрузился')
try:
	pygame.mixer.music.load('sounds/YOUNG RILL - ICE  120 BPM.mp3')
	pygame.mixer.music.set_volume(0.1)
	pygame.mixer.music.play(-1)
except pygame.error:
	print('Фоновая музыка не загрузилась')

font1 = pygame.font.SysFont('arial', 25)

clock = pygame.time.Clock()

winwidth = 500 #Ширина экрана в пикселях
winheigth = 500 #Высота экрана в пикселях

win = pygame.display.set_mode((winwidth,winheigth))
pygame.display.set_caption('What is it ?')#Название окна

def stat():
	global width 
	global height 
	global x 
	global y 
	global speed 
	global lives 
	global resistance 
	global resistancecount 
	global maxresistance 
	global ShootCount
	global maxshootcount 
	global enemyspeed 
	global enemylives 
	global howfastenemyspawn 
	global isenemyspawn
	global score 
	global reward
	global bullets
	global enemies
	global isJump
	global JumpCount

	width = 60
	height = 70
	x = winwidth//2 - width // 2 #Начальное положение
	y = winheigth-height-10
	speed = 3
	lives = 3
	resistance = False
	resistancecount = 0
	maxresistance = 180

	ShootCount = 30
	maxshootcount = 30

	enemyspeed = 1
	enemylives = 3
	howfastenemyspawn = 100 #Как часто спавнятся враги (в тиках)
	isenemyspawn = 0

	score = 0
	reward = 1

	bullets = []
	enemies = []

	isJump = False
	JumpCount = 10

isShooting = False

left = False
right = False
animCount = 0
lastMove = 'right'


isloose = False

class snaryad():
	def __init__(self, x, y, radius, color, facing):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.facing = facing
		self.vel = 8 * facing

	def draw(self, win):
		pygame.draw.circle(win, self.color,(self.x,self.y),self.radius)

class enemy():
	def __init__(self,x,y,facing,enemyanimcount,enemylives):
		self.x = x
		self.y = y
		self.facing = facing
		self.vel = enemyspeed * facing
		self.enemyanimcount = enemyanimcount
		self.enemylives = enemylives

	def draw(self,win):
		if self.enemyanimcount+1 >= 40:
			self.enemyanimcount = 0
		if self.vel < 0:
			win.blit(enemywalkLeft[self.enemyanimcount // 5], (self.x, self.y))
		else:
			win.blit(enemywalkRight[self.enemyanimcount // 5], (self.x, self.y))
		self.enemyanimcount += 1
	#Отрисовка окна
def drawWindow():
	global animCount
	win.blit(bg, (0,0))

	text1 = font1.render('Score '+str(score),1,(255,255,0))
	win.blit(text1,(10,0))

	if animCount+1 >=30:
		animCount = 0

	for bullet in bullets:
		bullet.draw(win)

	for e in enemies:
		e.draw(win)

	if left:
		win.blit(walkLeft[animCount // 5], (x,y))
		animCount += 1
	elif right:
		win.blit(walkRight[animCount // 5], (x,y))
		animCount += 1
	else:
		win.blit(playerStand, (x,y))

	for i in range(lives):
		if i == 0:
			win.blit(brain,(-10,30))
		elif i == 1:
			win.blit(brain,(35,30))
		elif i == 2:
			win.blit(brain,(80,30))
		elif i == 3:
			win.blit(brain,(125,30))
		elif i == 4:
			win.blit(brain,(170,30))
	pygame.display.update()

def loose():
	win.blit(bg,(0,0))
	text1 = font1.render('Score '+str(score),1,(255,255,0))
	win.blit(text1,(10,0))
	win.blit(loosebg,(50,100))
	pygame.display.update()

run = True

stat()
#Запуск игрового процесса
while run:
	clock.tick(60) #Количество тиков в секунду

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	if isloose == False:
		isenemyspawn += 1
		#Спавн врагов
		if isenemyspawn >= howfastenemyspawn:
			if random.randint(0,1) == 0:
				enemies.append(enemy(-70,405,1,0,enemylives))
			else:
				enemies.append(enemy(505,405,-1,0,enemylives))
			isenemyspawn = 0

		for e in enemies:
			e.x += e.vel
			if abs(e.x - x) < 40 and y+71 > 415 and resistance == False :
				lives -= 1
				try:
					punchsound.play()
				except NameError:
					pechalno == True
				resistance = True
				if lives <= 0:
					isloose = True
					loose()

		if resistance == True:
			resistancecount += 1
			if resistancecount >= maxresistance:
				resistancecount = 0
				resistance = False

		#Перемещение пули, удаление пули, если она за пределами экрана и попадание во врага
		for bullet in bullets:
			if bullet.x < 500 and bullet.x > 0:
				bullet.x += bullet.vel
			else:
				bullets.pop(bullets.index(bullet))	#Удаление пули
			for e in enemies:
				if bullet.vel > 0 and x < e.x and bullet.x >= e.x + 11 and e.x > -60 and e.x < 500 and bullet.y >405:
					e.enemylives -= 1
					try:
						zombiesound.play()
					except NameError:
						pechalno = True
					if e.enemylives == 0:
						enemies.pop(enemies.index(e))
						score += reward
						if score == 40:
							enemylives -= 1
						if score % 10 == 0:
							enemyspeed += 0.2
							howfastenemyspawn = round(howfastenemyspawn*0.95)
							maxshootcount = round(maxshootcount*0.98)
					try:
						bullets.pop(bullets.index(bullet))
					except ValueError:
						print('ValueError')
				elif bullet.vel < 0 and x > e.x and bullet.x <= e.x + 50 and e.x > -60 and e.x < 500 and bullet.y >405:
					e.enemylives -= 1
					try:
						zombiesound.play()
					except NameError:
						pechalno = True
					if e.enemylives == 0:
						enemies.pop(enemies.index(e))
						score += reward
						if score == 40:
							enemylives -= 1
						if score % 10 == 0:
							enemyspeed += 0.2
							howfastenemyspawn = round(howfastenemyspawn*0.95)
							maxshootcount = round(maxshootcount*0.98)
					try:
						bullets.pop(bullets.index(bullet))
					except ValueError:
						print('ValueError')
		#Управление
		keys = pygame.key.get_pressed()	
		if keys [pygame.K_SPACE] and isShooting == False:
			if lastMove == 'right':
				facing = 1
			if lastMove == 'left':
				facing = -1
			bullets.append(snaryad(round(x + width //2),round(y +height //2+10), 5,(255,0,0),facing))
			isShooting = True
			try:
				pistolsound.play()
			except NameError:
				pechalno =True
		if isShooting == True:
			ShootCount -= 1
			if ShootCount == 0:
				ShootCount = maxshootcount
				isShooting = False

		if (keys [pygame.K_LEFT] or keys [pygame.K_a])  and x>5:
			x -= speed
			left = True
			right = False
			lastMove = 'left'
		elif (keys [pygame.K_RIGHT] or keys [pygame.K_d]) and x<winwidth-width-5:
			x += speed
			left = False
			right = True
			lastMove = 'right'
		else:
			left = False
			right = False
			animCount = 0
		if not(isJump):		#Прыжок
			if keys [pygame.K_w] or keys [pygame.K_UP]:
				isJump = True
				speed += 3
		else:
			if JumpCount >= -10:
				if JumpCount<0:
					y += (JumpCount **2) // 2.5
				else:
					y -= (JumpCount **2) // 2.5
				JumpCount -= 1
			else:
				isJump = False
				JumpCount = 10
				speed -= 3
		drawWindow()
	else:
		clock.tick(240)
		loose()
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.pos[1] >= 226 and event.pos[1] <= 253 and event.pos[0] >= 173 and event.pos[0] <= 328:
					isloose = False
					stat()
pygame.quit()