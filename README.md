# Vintage BASIC Games in Python

This is an in-progress collection of simple, text-based Python games, ported mostly from [David H. Ahl's](https://www.swapmeetdave.com/Ahl/DHA.htm) two hugely popular collections of type-in BASIC program listings:
* [BASIC Computer Games](http://www.vintage-basic.net/games.html) (1973)
* [More BASIC Computer Games](https://www.atariarchives.org/morebasicgames/) (1979)

These programs influenced an entire generation of budding programmers back in the day, myself included. It is hoped that beginning Python coders will derive the same benefits from playing, exploring, and (most importantly) *modifying* these games as we did with the original BASIC versions.

The games here are truly "old school" and run as they would've originally: Right on on the command line (or in a Python IDE) using written output and typed-in input.


### Porting Notes
* The opening comments of each game are taken nearly verbatim from the original descriptions in the books.
* Comments within the code that came from the original listing are indicated with double quotes.
* The games themselves have been kept as close to the original play experience as possible:
   * The text prompts and displays are pretty much exactly as they appeared in the books, with attention paid to original spacing, punctuation, and spelling (including mistakes).
   * The original books included example printouts of test runs of each game. In cases where the output shown was different from what the given code would've actually produced, editorial choices have been made about which version to port over.
   * The output in the books used uppercase throughout, probably because many computers of that era lacked the capability to display anything else. These ports take the liberty of using both uppercase and lowercase.
* Program logic has also been kept fairly close to the originals:
   * Since Python is a [structured language](https://en.wikipedia.org/wiki/Structured_programming) (in contrast to vintage BASIC's older, [unstructured paradigm](https://en.wikipedia.org/wiki/Non-structured_programming)), all the GOTOs have been replaced with while loops, if/else/then blocks, and that sort of thing.
   * Unless they were especially horrible, logical errors have been faithfully replicated! Discovering and fixing them is part of the fun, after all.
   * Variable names have been changed from single letters to descriptive names. I'm not a monster.
* Porting notes and suggestions for modifications are found in the comments at the end of each code file. These are part of this project and did not appear in the original books.

Share and enjoy!

> **Note:** There is [another project on github](https://github.com/chaosotter/python-101-games) that's doing something similar, although not quite as tightly bound to the original play experience as this project aims to be. It looks really cool though, so you might want to check it out too!
