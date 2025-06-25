

For quite some time now, I've been interested in developing a classic rogue-like. I’m currently working on a passion project called Messidor, an open world(inspired by Zelda I & II), procedurally generated hardcore survival(inspired by RLCraft), with dungeon crawl sections(inspired by brogue) and maximalist complexity(inspired by Dwarf Fortress and Nethack).

It’s a terminal-based ASCII roguelike, built from scratch in Python using curses, focused on emergent systems and expressive, simulation-driven gameplay. It combines open-ended survival, dangerous exploration, and a rich procedural world where everything(terrain, weather, dungeons, creatures) can potentially interact.

The game is still in its early stages, but I already have the core engine up and running. The world is generated in tiles using Perlin noise, and the player can move freely through it with a camera system centered on the visible screen. Entities persist in the world, AI is functioning, collision and layering are working, and movement is mapped cleanly between screen and world coordinates.
