import pygame as pg
import configLoader
import userInteraction
from field import Field
from ball import Ball
from player import Player



if __name__ == '__main__':

    # load config
    configloader = configLoader.ConfigLoader('./static_param.json')

    screen_width = configloader.params['screen']['width']
    screen_height = configloader.params['screen']['height']
    ratio = configloader.params['screen']['ratio']

    # initialize field
    field_width = configloader.params['field']['pitch_width']
    field_length = configloader.params['field']['pitch_length']
    field = Field(field_length, field_width, screen_width, screen_height)
    field.init_params(ratio,configloader.params['field']['center_circle_r'], configloader.params['field']['penalty_area_length'],
                      configloader.params['field']['penalty_area_width'], configloader.params['field']['goal_width'],
                      configloader.params['field']['goal_depth'])
    
    # initialize players
    player_radius = configloader.params['vehicle']['player_size']
    me = Player(player_radius, ratio, 0)
    opponent = Player(player_radius, ratio, 1)
    me.move(100, 100)
    opponent.move(200, 200)

    # initialize ball
    ball_radius = configloader.params['ball']['ball_size']
    ball_decay = configloader.params['ball']['ball_decay']
    ball = Ball(ball_radius, ratio, ball_decay)
    ball.move(300, 300)

    # initialize user interaction
    modeMonitor = userInteraction.InteractionModeMonitor()
    movement = userInteraction.Movement(me, opponent, ball)
    userCreation = userInteraction.userCreation(me, opponent, ball)

    pg.init()
    pg.display.set_caption('Roobcup Geometry Visualizer')
    screen = pg.display.set_mode((screen_width, screen_height))
    clock = pg.time.Clock()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False
            modeMonitor.judgeMode(event)
            movement.judgeMovement(event)
            userCreation.judgeUserCreation(event)


        screen.fill((0, 128, 0))

        # main drawing part
        field.draw(screen)
        me.draw(screen)
        opponent.draw(screen)
        ball.draw(screen)
        userCreation.draw(screen)
        modeMonitor.draw(screen)

        pg.display.flip()
        clock.tick(60)
    pg.quit()