import pygame as pg
import pgUtils

class Field:
    def __init__(self, pitch_length, pitch_width, screen_width, screen_height):
        self.pitch_length = pitch_length
        self.pitch_width = pitch_width
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.screen_center = (self.screen_width / 2, self.screen_height / 2)

        self.color = (255, 255, 255)

    def init_params(self,size_in_screen,conter_circle_r,penalty_area_length,penalty_area_width,goal_width,goal_depth):
        self.ratio = size_in_screen
        self.center_circle_radius = conter_circle_r * self.ratio
        self.penalty_area_length = penalty_area_length * self.ratio
        self.penalty_area_width = penalty_area_width * self.ratio
        self.goal_width = goal_width * self.ratio
        self.goal_depth = goal_depth * self.ratio


        self.border = int(self.ratio * 50)
        self.pitch_length = int(self.pitch_length * self.ratio)
        self.pitch_width = int(self.pitch_width * self.ratio)

    def draw(self, screen):
        # draw field
        pgUtils.drawCenterRect(screen, self.screen_center, self.pitch_length, self.pitch_width, self.color, self.border)
        # draw our penalty area
        pg.draw.rect(screen, self.color, (self.screen_center[0] - self.pitch_length / 2, self.screen_center[1] - self.penalty_area_length / 2, self.penalty_area_width, self.penalty_area_length), self.border)
        # draw opponent penalty area
        pg.draw.rect(screen, self.color, (self.screen_center[0] + self.pitch_length / 2 - self.penalty_area_width, self.screen_center[1] - self.penalty_area_length / 2, self.penalty_area_width, self.penalty_area_length), self.border)
        # draw center circle
        pg.draw.circle(screen, self.color, self.screen_center, self.center_circle_radius, self.border)
        # draw middle line
        pg.draw.line(screen, self.color, (self.screen_center[0], self.screen_center[1] - self.pitch_width / 2), (self.screen_center[0], self.screen_center[1] + self.pitch_width / 2), self.border)
        # draw our goal
        pg.draw.rect(screen, self.color, (self.screen_center[0] - self.pitch_length / 2 - self.goal_depth, self.screen_center[1] - self.goal_width / 2, self.goal_depth, self.goal_width), self.border)
        # draw opponent goal
        pg.draw.rect(screen, self.color, (self.screen_center[0] + self.pitch_length / 2, self.screen_center[1] - self.goal_width / 2, self.goal_depth, self.goal_width), self.border)


