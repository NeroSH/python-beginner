import play
import pygame

play.set_backdrop('light green')
pygame.display.set_caption("The hardest platformer ever")

# тут подключи нужны звуки. Например, звук сбора монетки
coin_sound = pygame.mixer.Sound('coin.wav')
sea_sound = pygame.mixer.Sound('sea.ogg')

# счетчик монет
score_txt = play.new_text(words='Score:', x=play.screen.right - 100, y=play.screen.top - 30, size=70)
score = play.new_text(words='0', x=play.screen.right - 30, y=play.screen.top - 30, size=70)

# подсказки
text = play.new_text(words='Tap SPACE to jump, LEFT/RIGHT to move', x=0, y=play.screen.bottom + 60, size=70)

# перснонаж
sprite = play.new_circle(color="yellow", x=play.screen.left + 20, y=play.screen.top - 20, radius=15, border_width=1,
                         border_color="brown")
sea = play.new_box(color='blue', width=play.screen.width, height=50, x=0, y=play.screen.bottom + 20)

# пустой список блоков и монеток
platforms = []
coins = []


def draw_platforms( ):
    # добавь сюда платформы, по которым будет перемещаться персонаж
    platform1 = play.new_box(color='brown', border_width=1, border_color='black', width=150, height=30,
                             x=play.screen.left + 70, y=play.screen.top - 170)
    platform2 = play.new_box(color='brown', border_width=1, border_color='black', width=250, height=30,
                             x=play.screen.left + 330, y=play.screen.top - 170)
    platform3 = play.new_box(color='brown', border_width=1, border_color='black', width=100, height=30,
                             x=play.screen.left + 550, y=play.screen.top - 120)
    platform4 = play.new_box(color='brown', border_width=1, border_color='black', width=130, height=30,
                             x=play.screen.left + 670, y=play.screen.top - 170)

    platforms.append(platform1)
    platforms.append(platform2)
    platforms.append(platform3)
    platforms.append(platform4)

    for p in platforms:
        p.start_physics(can_move=False, stable=True, obeys_gravity=False, mass=10)


def draw_coins( ):
    # добавь сюда монетки, которык будет собирать персонаж
    coin1 = play.new_circle(color='yellow', x=play.screen.left + 330, y=play.screen.top - 130, radius=10)
    coin2 = play.new_circle(color='yellow', x=play.screen.left + 700, y=play.screen.top - 130, radius=10)

    coins.append(coin1)
    coins.append(coin2)


@play.when_program_starts
def start( ):
    # подключи фоновую музыку
    pygame.mixer_music.load('soundtrack.mp3')
    pygame.mixer_music.play()

    sprite.start_physics(can_move=True, stable=False, obeys_gravity=True, mass=50, friction=1.0, bounciness=0.5)

    draw_platforms()
    draw_coins()


@play.repeat_forever
async def game( ):
    # тут опиши процесс игры
    sprite.physics.x_speed = 0

    if play.key_is_pressed('right', 'd'):
        sprite.physics.x_speed = 10
    if play.key_is_pressed('left', 'a'):
        sprite.physics.x_speed = -10
    if play.key_is_pressed('space', 'up', 'w','ц'):
        sprite.physics.y_speed = 50
        await play.timer(seconds=1)
        sprite.physics.y_speed = 0

    # cбор монет
    for c in coins:
        if sprite.is_touching(c):
            coin_sound.play()
            sprite.physics.y_speed = -sprite.physics.y_speed
            coins.remove(c)
            c.hide()
            score.words=str(int(score.words) + 1)

    # проигрыш
    if sprite.is_touching(sea):
        sea_sound.play()
        sprite.hide()
        await play.timer(seconds=2.0)
        quit()

    await play.timer(seconds=1 / 48)


play.start_program()
