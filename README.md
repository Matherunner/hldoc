# Half-Life Physics Reference

![Gordon and Scientist](https://raw.githubusercontent.com/Matherunner/hldoc/master/source/images/gordon-scientist.jpg)

This repo contains the source files for the Half-Life physics documentation hosted at

* https://www.jwchong.com/hl/ (or [bit.ly/hlphysics](https://bit.ly/hlphysics))
* https://tastools.rtfd.io (mirror)

## Building

Install python. Then first create a python `venv` folder:

    $ python -m venv venv

Activate the venv:

    $ . ./venv/bin/activate

Then install the packages:

    $ pip install -r requirements.txt

To build the HTML files, run

    $ python build.py build

## How to contribute

You are encouraged to help out this documentation by researching and writing. You will be credited. This project will be kept online for as long as I'm alive. You can begin by checking out the list of topics below and research the ones you find interesting, or simply look at the empty sections of the documentation and contribute to research and writing for it.

| Difficulty | Meaning |
| --- | --- |
| Low | Requires a few hours worth of effort to gain a thorough understanding |
| Medium | Requires a few days worth of focused effort to gain a thorough understanding |
| High | Requires a few days to a few weeks worth of focused effort, while possessing prerequisite knowledge and skills, to gain a reasonable level of understanding |
| Very high | Requires a few weeks to a few months worth of focused effort, while possessing deep prerequisite knowledge and skills, to gain a reasonable level of understanding |
| Extremely high | Requires months or years of focused effort, while possessing expert-level understanding of relevant Half-Life physics and very well trained on specific mathematical skills, to make meaningful contributions |

### Engine internals

Engine internals are generally tedious to research on due to the unavailability of source code.

| Topic | Issues | Difficulty |
| --- | --- | --- |
| Loading, saving, level change | | High |
| Save warping | | Medium |
| BSP collision structure in memory | | High |
| Tracing | | High |
| Frame walkthrough | | High |
| 0ms frames | | Medium |
| Network messages and DELTA | | Medium |
| Demos | | Medium |

### Movement physics

Naturally, movement physics are some of the most maths-heavy parts of Half-Life physics, and thus some of these topics may be very difficult and require a high level of skill and knowledge.

| Topic | Issues | Difficulty |
| --- | --- | --- |
| Surfing | | Extremely high |
| Ducktapping on stairs | | High |
| Entity movements | | Medium |
| Base velocity | | Medium |
| Optimal ladder side exit | | High |
| Optimal tight strafing | | Very high |
| Optimal vent movement with bunnyhop cap | | High |
| Optimal damage boost timing | | High |
| Computing optimal route | | Extremely high |
| Constrained vectorial compensation | | High |
| Implementation of autoactions | | High |
| Characterising human strafing | | Very high |

### Weapons

Some of these topics may require some mathematics, and others may require an understanding of engine internals.

| Topic | Issues | Difficulty |
| --- | --- | --- |
| Optimal snark climbing | | Very high |
| Hornet manipulation and penetration | | Medium |
| Crowbar | | Low |
| Exact selfgauss conditions | | High |
| Exact nuking conditions | | High |
| Tripmines | | Low |
| Rockets | | Medium |
| Mid-air projectile collisions | | Very high |

### Entities

Understanding entities may require venturing into the engine, which again, may be tedious.

| Topic | Issues | Difficulty |
| --- | --- | --- |
| func\_wall vs worldspawn | | Medium |
| trigger\_once and trigger\_multiple | | Medium |
| trigger\_push | | Medium |
| How moving platforms carry entities | | Medium |
| func\_rotating (and friends) crushing mechanism | | Medium |
| Multimanager and scripting | | Medium |

### Monsters

A monster refers to an entity that has an AI, both friendly and unfriendly. Researching on AI can be very tedious due to the complex interactions between different parts of the code.

| Topic | Issues | Difficulty |
| --- | --- | --- |
| Reproducing HL21's gonarch | | Very high |
| Node graphs and monster movements | | High |
| Enemy behaviour | | High |
| Talkmonster behaviour | | High |
| Why models affects behaviour | | High |
| Ammo duplication with save loading, and reportedly without | | High |

### TAS

TAS topics are generally long term.

| Topic | Issues | Difficulty |
| --- | --- | --- |
| Better TAS process and tools | | Very high |
| Application of ML | | Extremely high |
