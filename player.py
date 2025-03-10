import pygame as pg
from camera import Camera
from settings import *

class Player(Camera):
    def __init__(self, app, position=PLAYER_POS, yaw=-90, pitch=0):
        self.app = app
        self.position = position
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)

        super().__init__(position, yaw, pitch)

    def update(self):
        self.keyboard_control()
        self.mouse_control()
        super().update()

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            voxel_handler = self.app.scene.world.voxel_handler
            if event.button == 1:
                voxel_handler.set_voxel()
            if event.button == 3:
                voxel_handler.switch_mode()

    def mouse_control(self):
        mouse_dx, mouse_dy = pg.mouse.get_rel()

        if mouse_dx:
            self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy:
            self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)

    def keyboard_control(self):
        voxel_handler = self.app.scene.world.voxel_handler
        key_state = pg.key.get_pressed()
        vel = PLAYER_SPEED * self.app.delta_time
        noclip = False
        voxel_proximity = 0.5
        if key_state[pg.K_w]:
            if noclip or not voxel_handler.check_collision(self.position, self.position + self.forward * (vel + voxel_proximity)):
                self.move_forward(vel)
        if key_state[pg.K_s]:
            if noclip or not voxel_handler.check_collision(self.position, self.position - self.forward * (vel + voxel_proximity)):
                self.move_back(vel)
        if key_state[pg.K_d]:
            if noclip or not voxel_handler.check_collision(self.position, self.position + self.right * (vel + voxel_proximity)):
                self.move_right(vel)
        if key_state[pg.K_a]:
            if noclip or not voxel_handler.check_collision(self.position, self.position - self.right * (vel + voxel_proximity)):
                self.move_left(vel)
        if key_state[pg.K_SPACE]:
            if noclip or not voxel_handler.check_collision(self.position, self.position + self.up * (vel + voxel_proximity)):
                self.move_up(vel)
        if key_state[pg.K_LSHIFT]:
            if noclip or not voxel_handler.check_collision(self.position, self.position - self.up * (vel + voxel_proximity)):
                self.move_down(vel)