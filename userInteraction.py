import pygame as pg
from field import Field
from ball import Ball
from player import Player
import pgUtils
import geometry as geo

# mouse button
MOUSE_LEFT_BUTTON = 1
MOUSE_MIDDLE_BUTTON = 2
MOUSE_RIGHT_BUTTON = 3

# interaction mode
MOVING_MODE = 0
EDITING_MODE = 1

# action type
TARGET = 0
LINE = 1

interactionMode = MOVING_MODE

class UserInteraction:
    def __init__(self):
        pass

class InteractionModeMonitor(UserInteraction):
    def __init__(self):
        super().__init__()

    def judgeMode(self, event):
        global interactionMode
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_c:
                interactionMode = EDITING_MODE if interactionMode == MOVING_MODE else MOVING_MODE

    def draw(self, screen):
        if interactionMode == MOVING_MODE:
            screen.blit(pg.font.Font(None, 36).render('Moving', True, (0, 0, 0)), (10, 10))
        else:
            screen.blit(pg.font.Font(None, 36).render('Creating', True, (0, 0, 0)), (10, 10))



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


class userAction:
    def __init__(self, type, *args):
        self.type = type
        if type == TARGET:
            self.pos = args[0]
        elif type == LINE:
            self._start = args[0]
            self._end = args[1]
            self.start = args[0]
            self.end = args[1]

    def update(self):
        if self.type == TARGET:
            pass
        elif self.type == LINE:
            if needUnpack(self._start):
                self.start = self._start.pos
            if needUnpack(self._end):
                self.end = self._end.pos

    def onMouse(self, pos):
        if self.type == TARGET:
            if (self.pos - pos).mod <= 10:
                return True
        return False

def needUnpack(obj):
        if type(obj) == Player or type(obj) == Ball or type(obj) == userAction and obj.type == TARGET:
            return True
        return False

class userCreation(UserInteraction):
    def __init__(self, me, opponent, ball):
        super().__init__()
        self.action_stack = []
        self.me = me
        self.opponent = opponent
        self.ball = ball

        self.isCreatingTarget = True

    def createTarget(self, pos):
        self.action_stack.append(userAction(TARGET, pos))

    def createLine(self, start, end):
        self.action_stack.append(userAction(LINE, start, end))

    def moveTarget(self, pos):
        if len(self.action_stack) > 0 and self.action_stack[-1].type == TARGET:
            self.action_stack[-1].target = pos
    
    def moveLine(self, end):
        if len(self.action_stack) > 0 and self.action_stack[-1].type == LINE:
            if needUnpack(end):
                self.action_stack[-1]._end = end
                end = end.pos
            self.action_stack[-1].end = end

    def draw(self, screen):
        for action in self.action_stack:
            action.update()
            if action.type == TARGET:
                pgUtils.drawTarget(screen, action.pos, 10, (255, 0, 0))
            elif action.type == LINE:
                pg.draw.line(screen, (255, 0, 0), action.start, action.end, 1)

    def undo(self):
        self.action_stack.pop()

    def clear(self):
        self.action_stack.clear()

    def judgeUserCreation(self, event):
        if interactionMode == EDITING_MODE:
            mouse_pos = geo.GeoPoint(pg.mouse.get_pos())
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == MOUSE_LEFT_BUTTON:
                    self.isCreatingTarget = True
                    if self.me.onMouse(mouse_pos):
                        start = self.me
                        end = mouse_pos
                        self.createLine(start, end)

                    elif self.opponent.onMouse(mouse_pos):
                        start = self.opponent
                        end = mouse_pos
                        self.createLine(start, end)

                    elif self.ball.onMouse(mouse_pos):
                        start = self.ball
                        end = mouse_pos
                        self.createLine(start, end)
                    else:
                        for action in self.action_stack:

                            if action.onMouse(mouse_pos):
                                start = action
                                end = mouse_pos
                                self.createLine(start, end)
                                self.isCreatingTarget = False
                                break
                    
            elif event.type == pg.MOUSEMOTION:
                self.isCreatingTarget = False
                if event.buttons[0]:
                    if len(self.action_stack) > 0 and self.action_stack[-1].type == LINE:
                        self.moveLine(mouse_pos)

            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == MOUSE_LEFT_BUTTON:
                    if not self.isCreatingTarget:
                        if self.me.onMouse(mouse_pos):
                            self.moveLine(self.me)
                        elif self.opponent.onMouse(mouse_pos):
                            self.moveLine(self.opponent)
                        elif self.ball.onMouse(mouse_pos):
                            self.moveLine(self.ball)
                        else:
                            noEnd = True
                            for action in self.action_stack:
                                if action.onMouse(mouse_pos):
                                    self.moveLine(action)
                                    noEnd = False
                                    break
                            if noEnd and len(self.action_stack) > 0 and self.action_stack[-1].type == LINE:
                                self.undo()
                            
                    else:
                        self.createTarget(mouse_pos)

            # ctrl+z: undo
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_z and pg.key.get_mods() & pg.KMOD_CTRL:
                    if len(self.action_stack) > 0:
                        self.undo()
                # ctrl+x: clear
                if event.key == pg.K_x and pg.key.get_mods() & pg.KMOD_CTRL:
                    self.clear()