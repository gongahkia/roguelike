# Rouguelike final update (14 Jan 2023)

![](http://static1.squarespace.com/static/5628419be4b0919906577165/t/56b90111f8508214b89b5751/1454965106563/katana_kittens-the_hunt-puppygrenade_com.jpg?format=2500w)

Did my best to make my code as readable as possible, so I won't be going into what each file does.

This is the final iteration of a small game I worked on over the span of 2 consecutive days, in an effort to familiarise myself with OOP. This game is to be played in Command Prompt.
To try it, download all the files within this folder, make sure they're in the same file directory, and run 'input.py'. Make sure you have Python3 or later versions installed!

----------

## What can be improved:

1. Failed to integrate bombs into the gameplay loop. The logic shouldn't be too difficult to implement, since the necromancer class has similar behaviour. However, **difficulty scaling** in this game is a big issue, and needs reworking.
2. Much of the code in `main.py` that could be compressed into functions were copied and pasted for easy reference. Code refactoring would have improved this.
3. Inability to print more than one bullet to the screen. Reworking the entity logging and printing system to a purely global coordinate-based dictionary that is updated by all entities per update, alongside a single print function, would have enabled multiple bullets to be printed.
4. Much of the HUD display for the user is hard coded. Refactoring them into functions for greater reusabilty would be ideal.

----------

That said, this was a refreshing learning experience, and working on a longer-form project that I was passionate about was fulfilling. Hope to do something like this again soon. If there's anything you feel could be improved, please don't hesistate to contact me on Twitter or my other socials. Thanks!

-Gong :)
