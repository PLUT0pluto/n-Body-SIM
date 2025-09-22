import copy
import math
from pathlib import Path
import sys
import config
import utils

#import phy c++ module 
try:
    current_dir = Path(__file__).parent  # src/
    project_root = current_dir.parent    
    nplanet_path = str(project_root / "src/physics")

    sys.path.append(nplanet_path)

    import nbodysim
except ImportError as e:
    print(f"Error importing nbodysim: {e}")
    print(f"Looked in path: {nplanet_path}")
    sys.exit(1)

class Simulation:
    def __init__(self):
        self.sim = nbodysim.phySim() #create instance of c++ simulation class
        # [x, y, vx, vy, ax, ay, mass, radius, color]
        self.planets = [[400, 400, 2, 0, 0, 0, 1000, 10, utils.random_color()], #default planets
                       [500, 400, 0, 0, 0, 0, 1000, 10, utils.random_color()]]
        self.planetsStartState = [] #to save initial state for reset
        self.camStartX = 0 #for saving camera pos on start for reset
        self.camStartY = 0
        self.isRunning = False
        self.isPaused = False
        self.lastPosList = []

    def start(self):
        if self.isRunning or not self.planets:
            return
        self.planetsStartState = copy.deepcopy(self.planets) #save initial state for reset
        for planet in self.planets:
            self.sim.addPlanet(*planet[:8]) #pass all but color to c++ side
        self.sim.start()
        self.isRunning = True
        self.isPaused = False

    def stop(self):
        if not self.isRunning:
            return
        self.sim.stop()
        self.isRunning = False
        self.isPaused = False
        self.planets = [] #clear planets to match C++ side
        self.lastPosList = []

    def reset(self):
        self.stop()
        self.planets = copy.deepcopy(self.planetsStartState)
        self.planetsStartState = []

    def toggle_pause(self):
        if not self.isRunning:
            return
        self.isPaused = not self.isPaused

    def update(self): #gets new planet positions from c++ side
        if self.isRunning and not self.isPaused:
            sim_time, positions = self.sim.get_snapshot()
            self.lastPosList = positions
            
            #update internal list of planets with new positions
            for i in range(0, len(positions), 2):
                planet_index = i // 2
                if planet_index < len(self.planets):
                    self.planets[planet_index][0] = positions[i]
                    self.planets[planet_index][1] = positions[i+1]
    
    def add_planet(self, pos):
        if self.isRunning: return
        self.planets.append([
            pos[0], pos[1], 0, 0, 0, 0, 
            config.DEFAULT_PLANET_MASS, 
            config.DEFAULT_PLANET_RADIUS, 
            utils.random_color()
        ])
        
    def remove_planet(self, index):
        if self.isRunning or not (0 <= index < len(self.planets)): return
        self.planets.pop(index)

    def find_planet_at(self, wrldPos):  #returns index of planet at pos or none
        for i, planet in reversed(list(enumerate(self.planets))):
            if utils.points_distance((planet[0], planet[1]), wrldPos) < planet[7]:
                return i
        return None
        
    def update_planet_value(self, index, iData, value):
        if 0 <= index < len(self.planets):
            try:
                self.planets[index][iData] = float(value)
            except (ValueError, TypeError):
                self.planets[index][iData] = 0

    def set_planet_velocity_by_angle(self, index, targetPos): #change spd direction
        if not (0 <= index < len(self.planets)): return
        
        planet = self.planets[index]
        dx = planet[0] - targetPos[0]
        dy = planet[1] - targetPos[1]
        
        curSpd = math.hypot(planet[2], planet[3])
        angle = math.atan2(dy, dx)

        planet[2] = curSpd * math.cos(angle)
        planet[3] = curSpd * math.sin(angle)