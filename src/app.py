# app.py
import pygame
import pygame.freetype
import pygame_gui as pygui
import sys
import time

import config
from sim import Simulation
from rendering import Renderer
from gui import GUIManager

class App:
    def __init__(self):
        pygame.init()
        pygame.freetype.init()

        self.screen = pygame.display.set_mode(config.WINDOW_SIZE)
        pygame.display.set_caption(config.CAPTION)
        self.clock = pygame.time.Clock()

        self.simulation = Simulation()
        self.renderer = Renderer(self.screen)
        self.gui = GUIManager(config.WINDOW_SIZE)
        
        self.running = True
        self.selectedPlanet = 0 #index of selected planet (-1 if none)
        self.draggedPlanet = -1 #index of the planer being dragged
        self.spdPlanet = -1 #index of the planet getting spd dierction changed
        self.camPannning = False
        
        #timers to for drag vs click detection
        self.dragStartTime = 0
        self.spdStartTime = 0
        
        self.gui.show_planet_editor(self.simulation.planets[self.selectedPlanet])

    def run(self):
        while self.running:
            timeDelta = self.clock.tick() / 1000.0
            
            self.handle_events()
            self.update()
            
            self.gui.update(timeDelta)
            self.renderer.draw(self.simulation, self.gui, self.selectedPlanet)
        
        self.cleanup()

    def handle_events(self):
        wrldMousePos = self.renderer.screen_to_world(*pygame.mouse.get_pos())
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            #check gui events first
            self.gui.process_events(event)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_down(event, wrldMousePos)
            if event.type == pygame.MOUSEBUTTONUP:
                self._handle_mouse_up(event, wrldMousePos)

            if event.type == pygui.UI_BUTTON_PRESSED:
                self._handle_gui_buttons(event.ui_element)
            
            if event.type == pygui.UI_TEXT_ENTRY_CHANGED:
                self._handle_text_input(event.ui_element)

    def _handle_mouse_down(self, event, wrldMousePos):
        #ignore clicks on the UI panel
        if self.renderer.topUiRect.collidepoint(event.pos):
            return

        indPlanet = self.simulation.find_planet_at(wrldMousePos)

        if event.button == 1: # Left click
            if indPlanet is not None:
                self.draggedPlanet = indPlanet
                self.dragStartTime = time.time()
        
        elif event.button == 3: # Right click
            if indPlanet is not None:
                self.spdPlanet = indPlanet
                self.spdStartTime = time.time()
            else: # Pan camera
                self.camPannning = True

    def _handle_mouse_up(self, event, wrldMousePos):
        if event.button == 1: #left 
            if self.draggedPlanet != -1:
                # If short click, select the planet
                if time.time() - self.dragStartTime < 0.2:
                    self.selectedPlanet = self.draggedPlanet
                    self.gui.show_planet_editor(self.simulation.planets[self.selectedPlanet])
                self.draggedPlanet = -1

            #clicked on empty space
            elif not self.renderer.topUiRect.collidepoint(event.pos):
                if self.selectedPlanet == -1:
                    self.simulation.add_planet(wrldMousePos)
                else: # Deselect
                    self.selectedPlanet = -1
                    self.gui.hide_planet_editor()

        elif event.button == 3: # Right
            self.camPannning = False
            if self.spdPlanet != -1:
                self.spdPlanet = -1
        
    def _handle_gui_buttons(self, uiElement):
        if uiElement == self.gui.btnStart:
            self.simulation.start()
            self.selectedPlanet = -1
            self.gui.hide_planet_editor()
        elif uiElement == self.gui.btnQuit:
            self.running = False
        elif uiElement == self.gui.btn_delete and self.selectedPlanet != -1:
            self.simulation.remove_planet(self.selectedPlanet)
            self.selectedPlanet = -1
            self.gui.hide_planet_editor()
        elif uiElement == self.gui.btnReset:
            self.simulation.reset()
            self.renderer.clear_trails()
            self.renderer.camX = self.simulation.camStartX
            self.renderer.camY = self.simulation.camStartY
            self.gui.btnPause.set_text("Pause")
        elif uiElement == self.gui.btnPause:
            self.simulation.toggle_pause()
            self.gui.btnPause.set_text("Unpause" if self.simulation.isPaused else "Pause")
    
    def _handle_text_input(self, uiElement):
        if self.selectedPlanet == -1: return
    
        try:
            # Get the index of the input field in the list
            field_idx = self.gui.input_fields.index(uiElement)
            # Map it to the index in the body's data list
            data_idx = field_idx if field_idx < 4 else field_idx + 2
            
            # Get the current text and update the simulation
            # No need to sanitize or call set_text() anymore!
            text = uiElement.get_text()
            self.simulation.update_planet_value(self.selectedPlanet, data_idx, text)

        except ValueError:
            # This will now only catch if the element isn't in our list
            pass

    def update(self): #update camera and dragged planet positions
        mouseRel = pygame.mouse.get_rel()
        wrldMousePos = self.renderer.screen_to_world(*pygame.mouse.get_pos())
        
        # Update camera pos
        if self.camPannning:
            self.renderer.camX += mouseRel[0]
            self.renderer.camY += mouseRel[1]

        #update dragged planet position
        if self.draggedPlanet != -1 and time.time() - self.dragStartTime >= 0.2:
            planet = self.simulation.planets[self.draggedPlanet]
            planet[0] += mouseRel[0]
            planet[1] += mouseRel[1]
            if self.draggedPlanet == self.selectedPlanet:
                self.gui.inp_pos_x.set_text(f"{planet[0]:.2f}")
                self.gui.inp_pos_y.set_text(f"{planet[1]:.2f}")
                
        #update spd direction
        if self.spdPlanet != -1:
            self.simulation.set_planet_velocity_by_angle(self.spdPlanet, pygame.mouse.get_pos())
            if self.spdPlanet == self.selectedPlanet:
                planet = self.simulation.planets[self.selectedPlanet]
                self.gui.inp_speed_x.set_text(f"{planet[2]:.2f}")
                self.gui.inp_speed_y.set_text(f"{planet[3]:.2f}")

        self.simulation.update()
        
    def cleanup(self):
        #clean up
        self.simulation.stop()
        pygame.quit()
        sys.exit()