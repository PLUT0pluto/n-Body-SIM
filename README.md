Some time ago i watched one of those "ADHD" videos on TikTok where its just a minute of random objects in a physics simulation. At the time I was also watching nplanet problem series on netflix so i got the idea of trying to simulate multiple planets in a gravity simulation to see how chaotic it really is.

The nPlanet problem is a well known physics problem, which says that there is not closed form equation for how multiple objects in space move. 


improvements
the simulation can stutter when too many planets are closed by. This is expected since there is more precise calculations done in such case, but i think there is room for improvement. Also the python UI is very minimal. I decided to use pygame, since its easy to use, but the main problem is that pygame does not scale properly for high dpi screens. The consequence is that everything looks more pixelated than it should. I know there are ways to fix this using pygame.SCALED, but my main goal of this project was just the physics simulation so the look of ui is pretty far down in terms of necessity.