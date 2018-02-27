Monsters
========

Barney
------

Gonarch
-------

.. _nihilanth:

Nihilanth
---------

Nihilanth is one of the more complex monsters in Half-Life. As a high level
description, the nihilanth begins with 20 floating energy spheres around its
head. There are three crystals around the big cylindrical chamber. Nihilanth has
an initial health :math:`\mathcal{H}_n` of 800 in easy and medium modes, and
1000 in hard mode. When its health gets reduced below the starting health, it
will absorb energy spheres, with each sphere giving a health of
:math:`\mathcal{H}_n / 20`. Effectively, the nihilanth starts off with twice the
designated health.


Scientist
---------

Scientists are very weak.

A scientist can heal the player if the player health is less than or equal to 50 and if the player is at most 128 units away from the scientist. Once healed, the scientist will not heal again until after one minute. The heal amount is always 25 health, as specified by the ``sk_scientist_heal`` skill cvars.

.. _squeak grenade monster:

Snarks
------

As monsters, snarks do not attack the player under any circumstances until it
has bounced off some entity at least once. For example, a snarks that is freshly
tossed will never seek out the player mid-air until it has landed and bounced
off the ground.

Snarks have friction and gravitational modifiers of 0.5, and a health of 2.
Snarks are set to ``MOVETYPE_BOUNCE`` in each ``HuntThink``, which occurs once
every 2 seconds. This implies that the bounce coefficient is :math:`b = 2 - 1/2
= 3/2`. This bounce coefficient can affect how snarks bounce off any surface, as
dictated by the general collision equation in :ref:`collision`.
