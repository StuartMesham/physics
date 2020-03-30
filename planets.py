import pygame
import numpy as np
import time

background_colour = (30,50,100)
(width, height) = (1100, 700)

class Particle:
    def __init__(self, x_y, size, mass):
        x, y = x_y
        self.size = size
        self.colour = (200, 200, 200)
        self.thickness = 1
        self.elasticity = 0.8
        self.drag = 0.0
        self.mass = mass #Doesn't do anything

        self.r = np.matrix([[x], #position vector
                            [y]])

        self.V = np.matrix([[0.0], #velocity vector
                            [0.0]])

    def display(self):
        pygame.draw.circle(screen, self.colour, (self.r[0][0], self.r[1][0]), self.size, self.thickness)

    def move(self, dT):
        self.r += self.V*dT
        self.V *= 1.0 - self.drag*dT

    def bounce(self):
        #right and left
        if self.r[0][0] + self.size > width:
            self.r[0][0] = 2*width - 2*self.size - self.r[0][0]
            self.V[0][0] = -self.V[0][0] * self.elasticity
        elif self.r[0][0] - self.size < 0:
            self.r[0][0] = 2*self.size -self.r[0][0]
            self.V[0][0] = -self.V[0][0] * self.elasticity

        #bottom and top
        if self.r[1][0] + self.size > height:
            self.r[1][0] = 2*height - 2*self.size - self.r[1][0]
            self.V[1][0] = -self.V[1][0] * self.elasticity
        elif self.r[1][0] - self.size < 0:
            self.r[1][0] = 2*self.size -self.r[1][0]
            self.V[1][0] = -self.V[1][0] * self.elasticity

    def apply_force(self, F, dT):
        self.V += (F/self.mass)*dT

particles = []
selected_particle = None

def findParticle(x, y):
    mousePosition = np.matrix([[x],
                               [y]])
    for particle in particles:
        #if distance from mouse click to particle center < particle size (mouse clicked in particle)
        if np.linalg.norm(mousePosition - particle.r) <= particle.size:
            return particle
    return None

particles.append(Particle((150.0, 50.0), 35, 500))
particles.append(Particle((200.0, 100.0), 15, 5))
particles.append(Particle((250.0, 100.0), 20, 15))
#
# particles.append(Particle((200.0, 300.0), 15, 5))
# particles.append(Particle((100.0, 160.0), 15, 5))
# particles.append(Particle((300.0, 400.0), 15, 5))
# particles.append(Particle((200.0, 500.0), 15, 5))
# particles.append(Particle((500.0, 200.0), 15, 5))


gravity = np.matrix([[0.0],
                     [400.0]])

#start running
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Lepartiqué!')

running = True
lastTime = time.time()
currentTime = 0.0
dT = 0.0
G = 10000

while running:
    #clear the screen
    screen.fill(background_colour)

    currentTime = time.time()
    dT = currentTime - lastTime
    lastTime = currentTime

    #update each particle
    for i, particle in enumerate(particles):
        # particle.apply_force(gravity, dT)
        for j in range(i + 1, len(particles)):
            # print(i, j)
            # print(particle.r)
            # print(particles[j].r)
            gVector = particles[j].r - particle.r
            force = (G * particle.mass * particles[j].mass / (np.linalg.norm(gVector) ** 3)) * gVector
            particle.apply_force(force, dT)
            particles[j].apply_force(-force, dT)

        particle.move(dT)
        particle.bounce()
        particle.display()

    #draw everything
    pygame.display.flip()

    # Handle user interactions

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            selected_particle = findParticle(mouseX, mouseY)

            if selected_particle:
                selected_particle.colour = (255, 255, 255)

        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_particle:
                selected_particle.colour = (200, 200, 200)
            selected_particle = None

    if selected_particle:
        (mouseX, mouseY) = pygame.mouse.get_pos()
        mousePosition = np.matrix([[mouseX],
                                   [mouseY]])

        selected_particle.V = (mousePosition - selected_particle.r) * 10
