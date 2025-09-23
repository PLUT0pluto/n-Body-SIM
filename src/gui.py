import pygame
import pygame_gui as pygui
import config

class GUIManager:
    def __init__(self, window_size):
        self.manager = pygui.UIManager(window_size)

        #restrict input to only numbers, decimal point and minus sign (for input fields)
        self.allowed_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '-']

        #create UI elements
        self.btnStart = pygui.elements.UIButton(relative_rect=config.START_BUTTON_RECT, text='Start', manager=self.manager)
        self.btnQuit = pygui.elements.UIButton(relative_rect=config.QUIT_BUTTON_RECT, text='Quit', manager=self.manager)
        self.btn_delete = pygui.elements.UIButton(relative_rect=config.DELETE_BUTTON_RECT, text='Delete', manager=self.manager)
        self.btnReset = pygui.elements.UIButton(relative_rect=config.RESET_BUTTON_RECT, text='Reset', manager=self.manager)
        self.btnPause = pygui.elements.UIButton(relative_rect=config.PAUSE_BUTTON_RECT, text='Pause', manager=self.manager)
        
        self.lbl_pos_x = pygui.elements.UILabel(relative_rect=config.POS_X_LABEL_RECT, text='posX', manager=self.manager)
        self.lbl_pos_y = pygui.elements.UILabel(relative_rect=config.POS_Y_LABEL_RECT, text='posY', manager=self.manager)
        self.lbl_speed_x = pygui.elements.UILabel(relative_rect=config.SPEED_X_LABEL_RECT, text='spdX', manager=self.manager)
        self.lbl_speed_y = pygui.elements.UILabel(relative_rect=config.SPEED_Y_LABEL_RECT, text='spdY', manager=self.manager)
        self.lbl_mass = pygui.elements.UILabel(relative_rect=config.MASS_LABEL_RECT, text='mass', manager=self.manager)
        self.lbl_radius = pygui.elements.UILabel(relative_rect=config.RADIUS_LABEL_RECT, text='radius', manager=self.manager)

        self.inp_pos_x = pygui.elements.UITextEntryLine(relative_rect=config.POS_X_INPUT_RECT, manager=self.manager)
        self.inp_pos_y = pygui.elements.UITextEntryLine(relative_rect=config.POS_Y_INPUT_RECT, manager=self.manager)
        self.inp_speed_x = pygui.elements.UITextEntryLine(relative_rect=config.SPEED_X_INPUT_RECT, manager=self.manager)
        self.inp_speed_y = pygui.elements.UITextEntryLine(relative_rect=config.SPEED_Y_INPUT_RECT, manager=self.manager)
        self.inp_mass = pygui.elements.UITextEntryLine(relative_rect=config.MASS_INPUT_RECT, manager=self.manager)
        self.inp_radius = pygui.elements.UITextEntryLine(relative_rect=config.RADIUS_INPUT_RECT, manager=self.manager)
        
        self.labels = [self.lbl_pos_x, self.lbl_pos_y, self.lbl_speed_x, self.lbl_speed_y, self.lbl_mass, self.lbl_radius]
        self.input_fields = [self.inp_pos_x, self.inp_pos_y, self.inp_speed_x, self.inp_speed_y, self.inp_mass, self.inp_radius]
        self.hide_planet_editor()

    def process_events(self, event):
        self.manager.process_events(event)

    def update(self, timeDelta):
        self.manager.update(timeDelta)

    def draw(self, surface):
        self.manager.draw_ui(surface)
        
    def hide_planet_editor(self): #hides planet editor fields if none selected
        self.btn_delete.hide()
        for field in self.input_fields:
            field.hide()
        for label in self.labels:
            label.hide()
            
    def show_planet_editor(self, planet_data):
        self.btn_delete.show()
        for i, field in enumerate(self.input_fields):
            field.show()
            self.labels[i].show()
            #corresponding index in the planet data list [x, y, vx, vy, ax, ay, mass, radius, color]
            data_index = i if i < 4 else i + 2 #acceleration cant be set 
            field.set_text(str(planet_data[data_index]))