# Flappy Plane; first game using Game as OOP, inspired  from 'Clear Code'
from settings import *
from classes import Bg, Ground, Plane, Obstacle
import pygame
pygame.init()


class Game:
    def __init__(self):
        # Screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Flappy Plane Game")

        # Environment images
        self.bg_list = [Bg(0), Bg(images_dict["background.png"].get_width())]
        self.ground_list = [Ground(0), Ground(images_dict["ground.png"].get_width())]
        self.obstacle_list = [Obstacle(WIDTH), Obstacle(WIDTH*(3/2))]

        # Plane
        self.plane = Plane()

        # Clock
        self.clock = pygame.time.Clock()

    def draw_choice(self):
        self.screen.fill(PSEUDO_WHITE)

        font = pygame.font.SysFont("comicsans", 60)
        wlcm_txt = font.render("WELCOME TO", True, BLACK)
        game_name_txt = font.render("Flappy Plane", True, random_color(0, 255))
        game_txt = font.render("GAME", True, BLACK)

        for num, txt in enumerate([wlcm_txt, game_name_txt, game_txt]):
            self.screen.blit(txt, ((WIDTH-txt.get_width())/2, (HEIGHT/4)*(num+1)-(txt.get_height()/2)))

        pygame.display.flip()

    def draw_loosing(self):
        self.screen.fill(PSEUDO_WHITE)

        font = pygame.font.SysFont("comicsans", 60)
        u_lost_txt = font.render("YOU LOST", True, BLACK)

        font = pygame.font.SysFont("comicsans", 30)
        score_txt = font.render(f"Score: {int(self.plane.score)}", True, BLACK)
        HI_score_txt = font.render(f"High Score: {int(self.plane.high_score)}", True, BLACK)

        self.screen.blit(u_lost_txt, ((WIDTH-u_lost_txt.get_width())/2, (HEIGHT - u_lost_txt.get_height())/2))
        self.screen.blit(score_txt, ((WIDTH-score_txt.get_width())/2, HEIGHT*(3/4)))
        self.screen.blit(HI_score_txt, ((WIDTH-HI_score_txt.get_width())/2, HEIGHT*(4/5)))

        pygame.display.flip()

    def handle_loosing(self):
        self.plane.high_score = max(self.plane.score, self.plane.high_score)
        self.plane.score = 0
        self.obstacle_list = [Obstacle(WIDTH), Obstacle(WIDTH * (3 / 2))]
        self.plane.rect.centery = self.plane.origin_y
        self.plane.reset()

        self.draw_loosing()

        pygame.time.wait(2000)

    def draw_screen(self):
        for env_list in [self.bg_list, self.ground_list, self.obstacle_list]:
            for env in range(2):
                env_list[env].draw(self.screen)

        self.plane.draw(self.screen)

        font = pygame.font.SysFont("comicsans", 40)
        score_txt = font.render(str(int(self.plane.score)), True, BLACK)

        self.screen.blit(score_txt, (WIDTH-score_txt.get_width(), 0))

        pygame.display.flip()

    def run(self):
        # Mainloop
        running = True
        is_started = False
        while running:
            self.clock.tick(80)
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                if keys[pygame.K_SPACE] and is_started:
                    self.plane.jump()
                elif (event.type == pygame.MOUSEBUTTONDOWN or keys[pygame.K_SPACE]) and not is_started:
                    is_started = True

            if not is_started:
                self.draw_choice()
                continue

            for env in range(2):
                self.bg_list[env].manage_pos()
                self.ground_list[env].manage_pos()
                self.obstacle_list[env].manage_pos()

            self.plane.handle_movement()
            self.plane.score += 1/30

            # Check for collision against Obstacle
            plane_mask = self.plane.get_mask()
            for obstacle in self.obstacle_list:
                obstacle_mask = obstacle.get_mask()
                offset_x = self.plane.rect.x - obstacle.rect.x
                offset_y = self.plane.rect.y - obstacle.rect.y
                if obstacle_mask.overlap(plane_mask, (offset_x, offset_y)):
                    self.handle_loosing()
                    is_started = False

            # Check for collision against Obstacle
            for ground in self.ground_list:
                ground_mask = ground.get_mask()
                offset_x = self.plane.rect.x - ground.rect.x
                offset_y = self.plane.rect.y - ground.rect.y
                if ground_mask.overlap(plane_mask, (offset_x, offset_y)):
                    self.handle_loosing()
                    is_started = False

            # Player wants to go off screen upper
            if self.plane.rect.y <= 0:
                self.plane.rect.y = 0

            self.draw_screen()


game = Game()
game.run()

# I actually watched the whole video before doing this project, but I didn't copy his code, I had to solve some issues
#  on my own;
# Finished and put in Github the 4/5/2022
