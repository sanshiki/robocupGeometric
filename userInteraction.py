import pygame as pg
from field import Field

import pgUtils
import geometry as geo

# mouse button
MOUSE_LEFT_BUTTON = 1
MOUSE_MIDDLE_BUTTON = 2
MOUSE_RIGHT_BUTTON = 3

# interaction mode
MOVING_MODE = 0
EDITING_MODE = 1


DISPLAY_SPACE = 25

interactionMode = MOVING_MODE

class UserInteraction:
    def __init__(self):
        pass

class InteractionModeMonitor(UserInteraction):
    def __init__(self):
        super().__init__()
        self.playerVerbose = False
        self.ballVerbose = False

    def judgeMode(self, event):
        global interactionMode
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_e:
                interactionMode = EDITING_MODE if interactionMode == MOVING_MODE else MOVING_MODE
            elif event.key == pg.K_p:
                self.playerVerbose = not self.playerVerbose
            elif event.key == pg.K_b:
                self.ballVerbose = not self.ballVerbose

    def draw(self, screen):
        if interactionMode == MOVING_MODE:
            screen.blit(pg.font.Font(None, 36).render('Moving', True, (0, 0, 0)), (10, 10))
        else:
            screen.blit(pg.font.Font(None, 36).render('Editing', True, (0, 0, 0)), (10, 10))

        if self.playerVerbose:
            screen.blit(pg.font.Font(None, 36).render('Player Verbose', True, (0, 0, 0)), (10, 10+DISPLAY_SPACE))
        if self.ballVerbose:
            screen.blit(pg.font.Font(None, 36).render('Ball Verbose', True, (0, 0, 0)), (10, 10+2*DISPLAY_SPACE))



class Movement(UserInteraction):
    def __init__(self, me, opponent, ball):
        super().__init__()
        self.me = me
        self.opponent = opponent
        self.ball = ball

    def judgeMovement(self, event):
        global interactionMode
        if interactionMode == MOVING_MODE:
            # mouse down event
            if event.type == pg.MOUSEBUTTONDOWN:
                # mouse left button
                if event.button == MOUSE_LEFT_BUTTON:
                    pos = pg.mouse.get_pos()
                    if self.me.onMouse(pos):
                        self.me.move(pos[0], pos[1])
                        self.me.setDrag()
                    elif self.opponent.onMouse(pos):
                        self.opponent.move(pos[0], pos[1])
                        self.opponent.setDrag()
                    elif self.ball.onMouse(pos):
                        self.ball.move(pos[0], pos[1])
                        self.ball.setDrag()
                # mouse right button
                elif event.button == MOUSE_RIGHT_BUTTON:
                    pos = pg.mouse.get_pos()
                    if self.me.onMouse(pos):
                        self.me.turn(pos)
                        self.me.setTurn()
                    elif self.opponent.onMouse(pos):
                        self.opponent.turn(pos)
                        self.opponent.setTurn()
                    elif self.ball.onMouse(pos):
                        self.ball.setTurn()

            # mouse move event
            if event.type == pg.MOUSEMOTION:
                pos = pg.mouse.get_pos()
                if self.me.onDrag():
                    self.me.move(pos[0], pos[1])
                elif self.opponent.onDrag():
                    self.opponent.move(pos[0], pos[1])
                elif self.ball.onDrag():
                    self.ball.move(pos[0], pos[1])
                elif self.me.onTurn():
                    self.me.turn(pos)
                elif self.opponent.onTurn():
                    self.opponent.turn(pos)

            # mouse up event
            if event.type == pg.MOUSEBUTTONUP:
                self.me.resetDrag()
                self.opponent.resetDrag()
                self.ball.resetDrag()
                self.me.resetTurn()
                self.opponent.resetTurn()

                if self.ball.onTurn():
                    self.ball.setVel(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
                    self.ball.resetTurn()


