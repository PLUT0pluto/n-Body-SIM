# n-Body Gravity Simulator

This is a simple n-body gravity simulator built with Python, Pygame, and a C++ module for the physics calculations. It allows you to create, edit, and delete celestial bodies and watch them interact with each other based on gravitational forces.

I started working on this project in c++ with intent on also using some c++ library for ui. But later I changed my mind and decided I'd rather use python since making ui seemed pretty easy with pygame, plus I haven't written anything in it in a while. This separation of physics and ui also gave me the idea to try multithreading and make c++ physics code run in a separate thread. I haven't tested how much this improves performance, but I mainly did it just to see how multithreading works so I'm pretty happy with it.

## How to Run

1.  **Prerequisites**:
    *   Python 3
    *   Pygame: `pip install pygame`
    *   Pygame GUI: `pip install pygame_gui`

2.  **Run the simulation**:
    ```bash
    python src/main.py
    ```

**Note**: The physics calculation is done by a pre-compiled C++ module that I've made (`nbodysim.cp312-win_amd64.pyd`). I've only worked on this project from windows and python3 and I'm not sure if it runs on a different os or other python versions.

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

## Improvements
The problem that is really bothering me is the low resolution of text rendering. I think the reason for this is in how pygame detects the resolution of high dpi screens, but the solutions I found on google haven't worked for me. 
I also have to clean up the c++ code for the physics module and add it to this repositiory. 

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

<img width="1331" height="752" alt="Screenshot 2025-09-22 140849" src="https://github.com/user-attachments/assets/cd731159-b0d3-4f2e-980d-12c12d578a77" />
<img width="1120" height="773" alt="Screenshot 2025-09-22 141145" src="https://github.com/user-attachments/assets/af0d886b-db4f-401b-a973-6044113afa5a" />
