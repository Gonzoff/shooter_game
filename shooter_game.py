from pygame import *
from random import randint

font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render("ПОБЕДА!", True, (255, 255, 255))
lose = font1.render("ПОРАЖЕНИЕ!", True, (180, 0, 0))

font2 = font.SysFont('Arial', 36)

lost = 0
max_lost = 5
score = 0
goal = 50
HP = 3

#фоновая музыка
mixer.init()

mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
 
#нам нужны такие картинки:
bullets = "bullet.png"
img_bullet = "bullet.png"
img_back = "galaxy.png" #фон игры
img_hero = "rocket.png" #герой
img_enemy = "asteroid.png"
img_boss = "ufo.png"
 
#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
 #конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #Выз
       # ываем конструктор класса (Sprite):
       sprite.Sprite.__init__(self)
 
       #каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
 
       #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #метод, отрисовывающий героя на окне
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
 
# класс спрайта-пули
class Bullet(GameSprite):
# движение врага
    def update(self):
        self.rect.y += self.speed
# исчезает, если дойдет до края экрана
        if self.rect.y < 0:
            self.kill()

#класс главного игрока
class Player(GameSprite):
   #метод для управления спрайтом стрелками клавиатуры
    def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
 #метод "выстрел" (используем место игрока, чтобы создать там пулю)
    # метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
 
# класс спрайта-врага
class Enemy(GameSprite):
# движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        # исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Enemy2(GameSprite):
# движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        # исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1          

#Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
#создаем спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
 
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(4, 6))
    monster2 = Enemy2(img_boss, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
    monsters.add(monster)
    monsters.add(monster2)

bullets = sprite.Group()
#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#Основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна
while run:
   #событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
 
    if not finish:
        #обновляем фон
        window.blit(background,(0,0))

        text = font2.render("Счёт: " + str(score), 1, (255,255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))


       #производим движения спрайтов
        ship.update()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)

        #обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
 
        
        #цикл срабатывает каждые 0.05 секунд
    
        time.delay(50)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            if c.speed <= 3:
                monster2 = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
                monsters.add(monster2)
            else:
                monster = Enemy2(img_boss, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
                monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            window.blit(lose, (200, 200))
            finish = True

        if score >= goal:
            window.blit(win, (200, 200))
            finish = True
        display.update()
                                  

