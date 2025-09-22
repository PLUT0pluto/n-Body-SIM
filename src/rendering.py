import pygame
import config
import utils

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.trailSurf = pygame.Surface(config.TRAIL_SURF_SIZE) #surface for drawing trails
        self.trailSurf.set_colorkey(config.COLOR_BLACK) #makes black transparent
        self.trailShiftX = (config.TRAIL_SURF_SIZE[0] - config.WINDOW_SIZE[0]) // 2 #for correct trail suface draw position
        self.trailShiftY = (config.TRAIL_SURF_SIZE[1] - config.WINDOW_SIZE[1]) // 2
        self.camX = 0 #camera position
        self.camY = 0
        self.topUiRect = pygame.Rect(0, 0, config.WINDOW_SIZE[0], config.UI_TOP_PANEL_HEIGHT) #top UI panel 

    def world_to_screen(self, x, y): #adds camera offset
        return (x + self.camX, y + self.camY)

    def screen_to_world(self, x, y): #removes camera offset
        return (x - self.camX, y - self.camY)
        
    def clear_trails(self):
        self.trailSurf.fill(config.COLOR_BLACK)

    def draw(self, simulation, gui_manager, iPlanet): #main draw function
        self.screen.fill(config.COLOR_BLACK) # clear screen
        
        #draw trails first so thatb theyre at the bottom
        self.screen.blit(self.trailSurf, (-self.trailShiftX + self.camX, -self.trailShiftY + self.camY))

        if not simulation.isRunning: 
            self._draw_setup_mode(simulation.planets, iPlanet)
        else:
            self._draw_running_mode(simulation.planets, simulation.lastPosList)
        
        #draw ui
        pygame.draw.rect(self.screen, config.UI_BG_COLOR, self.topUiRect)
        gui_manager.draw(self.screen)
        
        pygame.display.flip()

    def _draw_setup_mode(self, planets, iPlanet): #draws planets in setup mode 
        for i, planet in enumerate(planets):
            screenPos = self.world_to_screen(planet[0], planet[1])
            radius = planet[7]
            color = planet[8]

            pygame.draw.circle(self.screen, color, screenPos, radius)

            # Draw velocity vector
            if planet[2] != 0 or planet[3] != 0:
                angle = pygame.math.Vector2(planet[2], -planet[3]).angle_to(pygame.math.Vector2(1, 0))
                utils.draw_arrow_by_angle(self.screen, screenPos, angle, color=color)

            # Draw selection outline
            if i == iPlanet:
                pygame.draw.circle(self.screen, config.COLOR_WHITE, screenPos, radius + 4, 2)
    
    def _draw_running_mode(self, planets, positions):
        if not positions:
            return

        #position list returned by c++module is flat
        for i in range(0, len(positions), 2):
            iPlanet = i // 2
            if iPlanet >= len(planets): continue
            
            planet = planets[iPlanet]
            nX, nY = int(positions[i]), int(positions[i+1])
            
            #draw planet
            pygame.draw.circle(self.screen, planet[8], self.world_to_screen(nX, nY), planet[7])
            
            #draw trail 
            startPos = (planet[0] + self.trailShiftX, planet[1] + self.trailShiftY)
            endPos = (nX + self.trailShiftX, nY + self.trailShiftY)
            pygame.draw.aaline(self.trailSurf, planet[8], startPos, endPos)