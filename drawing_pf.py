import pygame
import sys
import math
from agent import Agent
class Game:
    def __init__(self, width, height, landmarks, robot, particles):
        pygame.init()

        self.width = width
        self.height = height
        self.landmarks = landmarks
        self.robot = robot
        self.particles = particles

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Particle Filter 2D - Example")

        self.clock = pygame.time.Clock()

        # Set up colors
        self.white = (255, 255, 255)
        self.blue = (0, 0, 255)
        self.red = (255, 255, 0)
        self.black = (0, 0, 0)
        self.green = (0, 255, 0)
        self.yellow = (255, 255, 0)

        self.draw_robot_measurements = False
        self.draw_circle_measurements = False
        self.draw_particles = True

    def draw_landmark(self, x, y, width, height):
        half_width = width / 2.0
        half_height = height / 2.0
        pygame.draw.rect(self.screen, self.blue, (x-half_width, y-half_height, width, height))

    def draw_agent(self, x, y, theta, radius, color):
        line_lenght = 18
        pygame.draw.circle(self.screen, color, [x, y], radius, 0)
        pygame.draw.line(self.screen, self.black, [x, y], [x + line_lenght * math.cos(theta), y + line_lenght * math.sin(theta)], 2)

    def draw_robot_landmarks_measurements(self, landmark_x, landmark_y):
        pygame.draw.line(self.screen, (255, 158, 158, 1), [self.robot.pose_x, self.robot.pose_y], [landmark_x, landmark_y], 2)

    def draw_circle_landmarks_measurements(self, landmark_x, landmark_y, radius):
        pygame.draw.circle(self.screen, (37,156,198,255), [landmark_x, landmark_y], radius, 2)
        

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_m]:
                if self.draw_robot_measurements == False:
                    self.draw_robot_measurements = True
                else:
                    self.draw_robot_measurements = False

            if keys[pygame.K_c]:
                if self.draw_circle_measurements == False:
                    self.draw_circle_measurements = True
                else:
                    self.draw_circle_measurements = False

            if keys[pygame.K_p]:
                if self.draw_particles == False:
                    self.draw_particles = True
                else:
                    self.draw_particles = False

            if keys[pygame.K_q]:
                pygame.quit()
                sys.exit()

            # Draw landmarks on the screen
            self.screen.fill((self.white))
            for landmark in self.landmarks:
                #print("Run:", i[0], i[1])
                self.draw_landmark(landmark[0], landmark[1], 20, 20)


            #Draw particles on the screen
            if self.draw_particles:
                for particle in self.particles:
                    self.draw_agent(particle.pose_x, particle.pose_y, particle.pose_theta, 10, particle.color)
            
            # Draw robot's measurement
            if self.draw_robot_measurements:
                for landmark in self.landmarks:
                    self.draw_robot_landmarks_measurements(landmark[0], landmark[1])

            if self.draw_circle_measurements:
                for landmark in self.landmarks:
                    self.draw_circle_landmarks_measurements(landmark[0], landmark[1], math.sqrt((landmark[0] - self.robot.pose_x)**2 + (landmark[1] - self.robot.pose_y)**2))
                    

            # Draw the robot on the screen
            self.draw_agent(self.robot.pose_x, self.robot.pose_y, self.robot.pose_theta, 10, self.robot.color)

            # Update display
            pygame.display.flip()

            # Control the game loop speed
            self.clock.tick(30)