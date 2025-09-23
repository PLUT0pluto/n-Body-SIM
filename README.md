# n-Body Gravity Simulator

This is a simple n-body gravity simulator built with Python, Pygame, and a C++ extension for the physics calculations. It allows you to create, edit, and delete celestial bodies and watch them interact with each other based on gravitational forces.

## Features

*   **Real-time Simulation**: Watch the bodies interact in real-time. 
*   **C++ Performance**: The core physics calculations are performed in a C++ extension for better performance. The algorithm I used for calculations is RKF45.
*   **Add and Remove Bodies**: Click to add new bodies, or select and delete existing ones.
*   **Edit Body Properties**: Select a body to edit its position, velocity, mass, and radius.
*   **Camera Controls**: Pan the camera to view different parts of the simulation.
*   **Pause and Reset**: Pause the simulation to inspect the current state, or reset it to the initial conditions.
*   **Velocity Control**: Drag to set the initial position and right-drag to set the velocity direction of a body.


## How to Run

1.  **Prerequisites**:
    *   Python 3
    *   Pygame: `pip install pygame`
    *   Pygame GUI: `pip install pygame_gui`

2.  **Run the simulation**:
    ```bash
    python src/main.py
    ```

**Note**: The physics calculation is done by a pre-compiled C++ module that I've made (`nbodysim.cp312-win_amd64.pyd`). I've only worked on this project from windows and python3 and I'm not sure if it runs on other os or other python versions.

## Controls

*   **Left-click**:
    *   On empty space: Add a new planet (if none is selected) or deselect the current planet.
    *   On a planet: Select the planet.
*   **Left-click and Drag**:
    *   On a planet: Move the planet.
*   **Right-click**:
    *   On a planet: Change the direction of the planet's velocity.
*   **Right-click and Drag**:
    *   On empty space: Pan the camera.
*   **GUI Buttons**:
    *   **Start**: Starts the simulation.
    *   **Pause/Unpause**: Pauses or unpauses the simulation.
    *   **Reset**: Resets the simulation to its initial state.
    *   **Delete**: Deletes the selected planet.
    *   **Quit**: Exits the application.

## Structure

```
nBody-SIM/
├── src/
│   ├── app.py            # Main application class, handles events and main loop
│   ├── sim.py            # Simulation logic, manages bodies and C++ interface
│   ├── rendering.py      # Handles all drawing and camera
│   ├── gui.py            # Manages the GUI elements
│   ├── config.py         # Configuration variables
│   ├── main.py           # Entry point of the application
│   ├── utils.py          # Utility functions
│   └── physics/
│       └── nbodysim.pyd  # Pre-compiled C++ physics module
└── README.md
```