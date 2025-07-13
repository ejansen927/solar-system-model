# Newtonian Planetary Simulation with Pygame

This project simulates a toy solar system using classical Newtonian mechanics to model the motion and interaction of celestial bodies. Implemented in Python with Pygame and NumPy, it visually demonstrates gravitational interactions, orbital mechanics, and inertial motion of planets and stars in 2D space. Final project for Dr. Matthew Wright's Classical Mechanics course at Adelphi University, Fall 2023.

## Features

- Realistic gravitational attraction based on Newton's Law of Universal Gravitation
- Celestial bodies hard coded at programmable coordinates (Sun, Earth, Mars, Jupiter, Alpha Centauri, Dark Matter)
- Interactive mouse-over info display (position, velocity, acceleration)
- Zooming, panning, and adjustable time step (speed control)
- Modular and extensible code for adding more bodies or refining physics approximations
- Visualized using Pygame

## Physics Overview

Each body is defined by:

- Mass, position, velocity, radius, and color
- Acceleration is calculated based on the net gravitational force from all other bodies:

  F = G m1 m2 / r^2 r^hat

- The bodies update their positions and velocities using a time-stepped integration:

  v -> v_0 + a * dt
  r -> r_0 + v * dt

## Controls

| Action                      | Key / Mouse            |
|-----------------------------|------------------------|
| Pause / Resume              | `SPACE`                |
| Increase simulation speed   | `↑` (up arrow)         |
| Decrease simulation speed   | `↓` (down arrow)       |
| Zoom in                     | Scroll up              |
| Zoom out                    | Scroll down            |
| Pan the view                | Click + drag           |
| Exit simulation             | `ESC` or close window  |
| Show body info              | Hover or click on body |

## Simulation Notes

- Positions and distances are scaled down to fit within a screen coordinate system.
- Luminosity (deprecated) is stored for stars but not yet visualized dynamically.
- Dark matter and binary systems (e.g. Alpha Centauri) are included as non-orbiting massive test cases.
- Code is structured for extension: adding collisions, relativistic effects, or visualization of light curves.

- Made first in Jupyter Notebook. Can run in terminal simply using:

```bash
python solar_system.py
```

## Requirements

- Python 3.7+
- Pygame
- NumPy

Install with:
```bash
pip install pygame numpy
