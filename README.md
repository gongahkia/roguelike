# `Roguelike` 🧌

## Abstract

This is the final iteration of a small game I worked on over the span of 2 consecutive days, in an effort to familiarise myself with OOP. This game is played in Command Prompt.

## Usage 

To try it, download all the files within this folder, make sure they're in the same file directory, and run `input.py`. Make sure you have Python3 or later versions installed!

Gameplay controls use a single keypress; do not press Enter after `w`, `a`, `s`, `d`, `e`, `b`, `y`, or `n`.

Necromancer spells display `+` while loading, `!` for two windup turns, and `#` when they strike.

Every level starts with one bomb. Bombs damage enemies and destroy interior walls in their diamond-shaped blast area.

Use python3 input.py --level 0, --level 1, --level 2, or --level 3 to start a level directly for debugging. --level boss is an alias for the boss fight.

The boss arena is fully revealed, while the threat levels retain fog of war.
