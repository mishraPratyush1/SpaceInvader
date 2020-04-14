import pygame
import random
import math
from pygame import mixer
# initialise the module
pygame.init() 

# create a screen (width,height)
screen= pygame.display.set_mode((800,600))


# bakcground
background=pygame.image.load('images/background.png')

# background sound
mixer.music.load('sound/background.wav')
mixer.music.play(-1) #-1 to play on loop

# Title and icon
pygame.display.set_caption('space invaders')
icon=pygame.image.load('images/spaceship.png')
pygame.display.set_icon(icon)

# images player
player = pygame.image.load('images/space-invaders (2).png')

# to position the player in the desired location
playerX = 370
playerY = 480
px_change=0

# multiple enemy

num_of_enemies=4
enemy=[]
enemyX=[]
enemyY=[]
ex_change=[]
ey_change=[]

for i in range(num_of_enemies):
    enemy.append(pygame.image.load('images/enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(40,140))
    ex_change.append(4) 
    ey_change.append(40)

# bullet
bullet= pygame.image.load('images/bullet.png')
bulletX = 0
bulletY = 480
by_change = 10
# ready -you cant see the bullet
# fire - it is moving
b_state = 'ready'

#score
score=0
font = pygame.font.Font('font/pintersan.ttf', 52)

textX = 10
textY = 10

# gameover
ov=pygame.font.Font('font/pintersan.ttf', 100)

def gameOver():
    ov=font.render('Game Over',True,(0,255,0))
    screen.blit(ov,(400,300))



def show_score(textX,textY):
    sc=font.render('score : '+str(score),True,(0,255,0))
    screen.blit(sc,(textX,textY))



def play(x,y):
    # to display the player image
    screen.blit(player,(x,y))

def enem(x,y,i):
    screen.blit(enemy[i],(x,y))

def bulletFire(x,y):
    global b_state
    b_state='fire'
    # so that it appears on the spaceship
    screen.blit(bullet,(x + 16, y + 10))


def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
    
    if distance < 27:
        return True
    else:
        return False


    


# game loop
run = True

while run:
    
    # whatever you want to have in your screen all the time
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False 

        # if keystrole is pressed,check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                px_change=-5
            if event.key == pygame.K_RIGHT:
                px_change=+5
            if event.key ==pygame.K_SPACE:
                if b_state is 'ready':
                    bullet_sound=mixer.Sound('sound/laser.wav')
                    bullet_sound.play()
                    # get the current x-cordinate of the space ship.
                    bulletX=playerX
                    bulletFire(bulletX,bulletY)
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                px_change=0
            # if event.Key == pygame.K_RIGHT:
            #     px_change = 0 

        
        
        
        
        
                
    
    # checking for boundaries so that it stays within the screen
    playerX += px_change

    if playerX <= 0:
        playerX=0
        
    elif playerX >= 736:
        playerX = 736
        

    
    # enemy movement
    for i in range(num_of_enemies):
        
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[i] = 2000
            gameOver()
            break

        enemyX[i] += ex_change[i]

        if enemyX[i] <= 0:
            ex_change[i] = 4
            enemyY[i]+=ey_change[i]

        elif enemyX[i] >= 736:
            ex_change[i] = -4
            enemyY[i]+=ey_change[i]
    
    # collision
        collide = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collide:
            explode=mixer.Sound('sound/explosin.wav')
            explode.play()
            bulletY=480
            b_state='ready'
            score += 1
                
            enemyX[i] =random.randint(0,735)
            enemyY[i] = random.randint(40,140)

        enem(enemyX[i],enemyY[i],i)


    # bullet move
    if bulletY <=0:
        bulletY=480
        b_state='ready'
    if b_state is 'fire':
        bulletFire(bulletX,bulletY)
        bulletY-=by_change


    
       




    # calling the function
    play(playerX,playerY)
    show_score(textX,textY)

    # if you dont update the new changes wont be able to see
    pygame.display.update()
