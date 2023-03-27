## DungeonGame

*This is a 2D game on pygame, using SQL database. Your goal is to go through all the rooms with enemies and get enought score.*


### The game **Magic Dungeon** - when you start the game, a menu opens with 4 buttons: 
* **Play** (start a new game)
* **Load** (load one of the saved games)
* **Settings** (settings for the music and sounds of the game)
* **Exit** (quit)

When you start the game (new or downloaded), a checkered field (one of the rooms) opens, on which there are: a player, 2-4 enemies, chests where you can find keys for the next rooms, extra life, etc. _You need to reach the passage to the next room._ The player has several lives, every few moves the enemies make moves. 

To complete the game, you need to go through several rooms, then a victory message will appear and the game will end. _The location of enemies and items is randomly generated_ (only on a new game, data about saved rooms is stored in the database). Also at the top of the screen - the number of remaining lives, strength, collected items.

In the database: tables with rooms, enemies, objects and usernames, under which unfinished games are saved.
