## roguelike

a simple roguelike created during the tutorial event on [r/roguelikedev](https://www.reddit.com/r/roguelikedev/wiki/python_tutorial_series), written with python + libtcod.

the code is mostly a copy of the [(revised) libtcod tutorial](rogueliketutorials.com) (by TStand), which is in turn based on the [original tutorial](http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python%2Blibtcod) on roguebasin (by Jotaf).

over time, i added some features of my own:
+ freeze scroll (and frozen enemy 'behavior')
+ more equipment slots (and new equippable items)
+ consumables and equipment are in different item pools
+ equipment menu (with item stats)
+ target highlighting
+ ui tweaks (colored text, changed font file)
+ added (very basic) description to all entities
+ description and equipped items show up when mouse is moved over entity
+ new menu background (source image by christopher balaskas)
+ monsters can have starting equipment
+ implemented some alternative dungeon generation algorithms (i used [AtTheMatinee's code](https://github.com/AtTheMatinee/dungeon-generation) for reference)
