import userInteraction as ui
import pygame as pg
from ball import Ball
from player import Player
import pgUtils
import geometry as geo

# action type
TARGET = 0
LINE = 1

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
        elif self.type == LINE:
            if geo.isPointOnLine(self.start, self.end, pos):
                return True
        return False

def needUnpack(obj):
        if type(obj) == Player or type(obj) == Ball or type(obj) == userAction and obj.type == TARGET:
            return True
        return False

class userCreation(ui.UserInteraction):
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
        if ui.interactionMode == ui.EDITING_MODE:
            mouse_pos = geo.GeoPoint(pg.mouse.get_pos())
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == ui.MOUSE_LEFT_BUTTON:
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
                if event.button == ui.MOUSE_LEFT_BUTTON:
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
                            if (noEnd or self.action_stack[-1].start == self.action_stack[-1].end) and len(self.action_stack) > 0 and self.action_stack[-1].type == LINE:
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