Monsters
========

Monsters, also known as NPCs, have some of the least understood behaviours in
Half-Life. Some of the most unpredictable and perplexing tricks are related to
NPC behaviour. For example, luring the scientist in Questionable Ethics to a
retina scanner fluently is a notoriously hit-and-miss endeavour. Therefore, it
is the goal of this chapter to attempt to describe monster behaviour in
Half-Life to validate and disprove existing beliefs or superstitions.

General AI
----------

In this section, we will describe the general AI framework shared by all
monsters in Half-Life, specifically subclasses of ``CBaseMonster``.
Understanding the AI system in Half-Life is crucial in comprehending behaviours
of specific monster types. Keep the Half-Life SDK code opened on the side to aid
understanding.

For a given monster, all AI behaviour starts with ``RunAI`` defined in ``monsterstate.cpp``. This function is
called by ``MonsterThink`` 10 times per second. This function may be overridden
by subclasses. In vanilla Half-Life, only the human assassin, bullsquid, and
controller monster classes do so. As a high level overview, this function checks
for enemies and ensures the *schedules* are running.

A *schedule* composes a series of *tasks* to represent a complex behaviour. Each
task represents an atomic, basic, predefined action, along with a floating point
parameter, the meaning of which depends on the task. For example,
``TASK_MOVE_TO_TARGET_RANGE`` causes the monster to move to within some radius
from the entity pointed to by ``m_hTargetEnt``, where the radius is specified by
the parameter given to the task. Therefore, in addition to the task type, a
schedule also defines a parameter for each task type.

The ``MaintainSchedule`` called by ``RunAI`` is responsible of executing the
tasks in the current schedule or getting new schedules to run. It has a big loop
which executes at most 10 iterations. The loop initiates the execution of new
schedules or tasks with ``StartTask`` within the current schedule. In general,
tasks that can be completed immediately as soon as they are executed will be
executed across several iterations of this loop, until encountering no more
tasks or a task that will take some time to complete (for example, walking to a
point can take many frames). If task is taking a while to execute, every time
``MaintainSchedule`` is called, the ``RunTask`` function is called on the
currently executing task.

The ``StartTask`` and ``RunTask`` functions mentioned above are defined in the
base monster class, though they are often extended by subclasses. These
functions are essentially implementations of the finite state machine, where
given a task and some existing states or conditions, some action is performed
and the task is either completed, failed, or made to continue executing, with
potentially some state changes.

TODO

TODO

As mentioned above, a schedule can be interrupted when some conditions
associated with the entity are set (bits in ``m_afConditions``). The specific
conditions needed to interrupt a schedule vary from schedule to schedule and are
up to the game developer. Generally, for "talk monsters", which is the
superclass of talking monsters like barney guards and scientists, schedules are
interrupted by conditions related to sound, damage, or seeing a new enemy. This
is why shooting a scientist while he is talking will interrupt it. And this is
also why when you push a scientist away, he would literally prefer death to
being interrupted by damage or grenades while walking. This is shown by the
definition of ``slMoveAway`` in ``talkmonster.cpp``:

.. code-block:: c++
   :emphasize-lines: 6

   Schedule_t slMoveAway[] =
   {
     {
       tlMoveAway,
       ARRAYSIZE ( tlMoveAway ),
       0,
       0,
       "MoveAway"
     },
   };

Observe that the ``iInterruptMask`` is 0 in the highlighted line, which means
nothing can interrupt the schedule except death. NPCs in Half-Life can be
surprisingly persistent and stubborn, and this is just one of the ways this
character trait is manifested.

Interestingly, when ``bits_COND_HEAR_SOUND`` is set in ``iInterruptTask``, the
monster will only be interrupted by sounds defined in ``iSoundMask``. The
possible bits for the sound mask is defined in ``dll/soundent.h``. The code for
this behaviour is implemented in ``Listen``, where ``bits_COND_HEAR_SOUND`` or
smell conditions are set only if the sound matches the sound mask, or if
``pCurrentSound->m_iType & iMySounds`` is true.

TODO

TODO

.. TODO think about where to put the following paragraph, and organise it
   better! The functions are introduced in quite an ad-hoc way.

Yawing to face a particular direction is a common task done by monsters.
Examples of these tasks are ``TASK_FACE_ENEMY``, ``TASK_FACE_PLAYER`` etc.
Yawing is done by first setting the *ideal yaw* of the entity, typically by
calling ``MakeIdealYaw`` defined in ``dll/monsters.cpp``. This function takes a
destination vector as argument and computes the yaw that would face it. Then,
``ChangeYaw`` is called with yaw speed as its argument. If the input yaw speed
is :math:`\omega`, then ``ChangeYaw`` adds :math:`\min(10\omega\tau,
\vartheta_\mathrm{ideal} - \vartheta)` to the current yaw. In the case of
``TASK_FACE_PLAYER``, the task will be completed when the difference between
ideal and current yaw is less than 10 degrees and the minimum time to finish the
task has been met (given by the floating point argument to the task). Since this
task is only run 10 times per second, the *actual* yawing speed (in degrees per
second) is only

.. math:: 100\tau\omega

Therefore, the lower the frame rate (i.e. the higher the frame time
:math:`\tau`), the higher the yawing speed.

.. TODO talk about overshoot? Does this actually happen?

Taking cover from sound
~~~~~~~~~~~~~~~~~~~~~~~

Most players would be familiar with the behaviour of monsters running away from
grenades. Most people also believe that these monsters have the capability to
look at grenades, get visual confirmation, and attempt to run away. This is not
true, however. Monsters generally do not track grenades visually. Instead, they
listen to the sounds. Under the right conditions, a hand grenade (see
:ref:`handgrenade`) generates a specific sound which triggers surrounding
entities to flee. Similarly, firing an MP5 grenade (see :ref:`mp5`) also creates
the same type of sound alert. Upon hearing these specific types of sound, a
monster will attempt to take cover.

Each monster type can have its specific implementation of this behaviour. For
example, the human grunt implements ``slGruntTakeCoverFromBestSound`` and does
not use the default ``slTakeCoverFromBestSound`` defined in ``defaultai.cpp``.
Also, each monster may differ in how this schedule is triggered, though
generally ``GetScheduleOfType(SCHED_TAKE_COVER_FROM_BEST_SOUND)`` is called in
``GetSchedule`` when the closest sound returned by ``PBestSound`` has type
``bits_SOUND_DANGER``. This type of sound is created when a hand grenade lands
at a low speed, or when an MP5 grenade if fired, for example.

Regardless of the specific schedule used, the
``TASK_FIND_COVER_FROM_BEST_SOUND`` is typically defined, and this task is
handled by ``CBaseMonster::StartTask``. The most important function called is
``FindCover``, which uses the world's node graph to traverse the map.
Consequently, if no node graph is defined in adjacency, then this function would
not work. If the right conditions are met, of which there are many, a suitable
node will be selected, and ``MoveToLocation`` will be called to move towards the
selected node. ``MoveToLocation`` in turn builds a complete route towards the
node, and the route is stored in ``m_Route``. In subsequent calls to
``MaintainSchedule``, the monster will move from one point to another in the
route array until something causes it to fail, or the route is completed.

Attacking enemies
~~~~~~~~~~~~~~~~~

Most monsters in Half-Life attack the player or other monsters. This is not
surprising, as otherwise there would be no game play to speak of. As a
high-level overview, when a monster sees an enemy, some condition bits will be
set, and the monster state will transition into the *combat* state. Under this
state, the base class's ``GetSchedule`` will return the appropriate schedules to
attack, chase, or take cover.

TODO

Gonarch
-------

The gonarch is a complex monster.

.. _nihilanth:

Nihilanth
---------

Nihilanth is one of the more complex monsters in Half-Life. The nihilanth begins
with 20 floating health spheres around its head. There are three crystal health
recharger in big cylindrical chamber. Nihilanth has an initial health
:math:`\mathcal{H}` of 800 in easy and medium modes, and 1000 in hard mode. When
its health gets reduced below the original health, it will absorb energy
spheres, with each sphere giving a health of :math:`\mathcal{H} / 20`.
Effectively, the nihilanth starts off with twice the designated health.

Death process
~~~~~~~~~~~~~

The process of getting the nihilanth to open his head involves a few steps. The
nihilanth in turn maintains a few critical state information involves these
steps, such as the integers *level* and the *irritation*, among others. The
*level* starts off at 1, and *irritation* at 0. We know that the nihilanth only
opens his head when the *irritation* is 2. In order for the *irritation* to get
to 2, the *level* must get to 10 or above.

As long as either the health is below half the original health *or* the number
of health spheres is below 10, and *level* is at most 9, and ``m_hRecharger`` is
null (he has not found a crystal recharger), then *level* will be incremented
gradually. In fact, it is incremented every time some sequence has completed,
namely when ``m_fSequenceFinished`` is true. For example, when the nihilanth is
in the process of firing some energy balls, the sequence is still ongoing, and
therefore *level* will *not* be incremented until it is done.

As soon as *level* goes above 9, *irritation* will be set to 2. This is seen in
this code segment in ``NextActivity``:

.. code-block:: cpp

   ALERT( at_aiconsole, "nihilanth can't find %s\n", szName );
   m_iLevel++;
   if (m_iLevel > 9)
     m_irritation = 2;

When *irritation* is 2, then the head will open, provided he is not firing the
usual high-damage energy balls attack. You can guarantee this by ensuring the
health is below half the original health. This is because, according to
``NextActivity`` again,

.. code-block:: cpp
   :emphasize-lines: 1

   if (m_irritation >= 2 && pev->health < gSkillData.nihilanthHealth / 2.0)
   {
     pev->sequence = LookupSequence( "attack1_open" );
   }
   else
   {
     ...
   }

That is, only when the health if below half the original, and *irritation* is 2
or above, would the ``attack1_open`` sequence be used, corresponding to the
low-damage single-shot energy ball attack with the head open.

Unfortunately, *irritation* being 2 is the necessary condition to kill
nihilanth, therefore placing a hard limit on how soon we can kill him. To
understand why, notice that when the *irritation* is *not* 3, ``TakeDamage``
always sets the nihilanth's new health to

.. math:: \mathcal{H}' =
          \begin{cases}
          \mathcal{H} - D & D < \mathcal{H} \\
          1 & D \ge \mathcal{H}
          \end{cases}

This implies that there is no way to get his health below 0, thus preventing him
from dying by running ``DyingThink``. Only if *irritation* is 3 does
``TakeDamage`` allow his health to get below 0. In order to get *irritation* to
3, we must look at this relevant block in ``TraceAttack``:

.. code-block:: cpp

   if (m_irritation == 2 && ptr->iHitgroup == 2 && flDamage > 2)
     m_irritation = 3;

This is the only location in ``nihilanth.cpp`` which bumps up *irritation* to 3.
Presumably, hitgroup 2 refers to the part inside nihilanth's head.

In a speedrun, most of the time combating nihilanth is spent waiting for *level*
to gradually increment to 10. The speedrunner must minimise the number of times
nihilanth does any kind of attack, because an attack sequence takes longer to
complete, and while it is playing, ``NextActivity`` will not be called, and
therefore slowing down *level* increments. In addition, the speedrunner must get
the health to as low as possible, even though this is technically not necessary
for *level* to increment. Consider this line in ``HuntThink`` after obtaining
the next sequence to run:

.. code-block:: cpp

   pev->framerate = 2.0 - 1.0 * (pev->health / gSkillData.nihilanthHealth);

That is, the sequence frame rate is higher when the health is lower. Higher
sequence frame rate meant that a sequence completes faster, which implies
``NextActivity`` gets called more frequently, and therefore *level* increments
quicker. In fact, the frame rate at 1 health is nearly twice of that at full
health, implying *level* increments twice as fast.

Reducing health absorption
~~~~~~~~~~~~~~~~~~~~~~~~~~

It is also worth noting that, we can make nihilanth absorb only 10 health
spheres as opposed to 20, thus greatly reducing the amount of damage needed to
inflict upon nihilanth to minimise its health and maximising sequence frame
rate. Namely, we simply save and load when the number of spheres that have been
absorbed is at least 10. When the game loads, the rest of the sphere entities
will be gone, despite them seemingly being visible in the game. To see why,
consider this line in ``nihilanth.cpp`` defining data to be saved:

.. code-block:: cpp

   DEFINE_ARRAY( CNihilanth, m_hSphere, FIELD_EHANDLE, N_SPHERES ),

The ``CNihilanth`` class stores an array of 20 health spheres as ``m_hSphere``,
and of type ``EHANDLE``. When the game is saved, ``CSave::WriteFields`` in
``utils.cpp`` checks to see if a field is empty by checking if the data of that
field is all zeros or nulls. The ``DataEmpty`` function is used for this
purpose, and crucially, this function checks its given data byte-by-byte. A
lookup table of the sizes of various types of field data is used to look up the
size of one element. The developers, however, defined the size of ``EHANDLE`` to
be equal to the size of ``int``, when, in fact, ``sizeof(EHANDLE)`` is 8 while
``sizeof(int)`` is 4. As a result, only the first :math:`20 \cdot 4 = 80` bytes
of ``m_hSphere`` is checked, skipping the next 80 bytes. Therefore, when 10
spheres have been absorbed, the first half of the ``m_hSphere`` array will be
all nulls, fooling ``WriteFields`` into thinking the entire array is empty, when
in fact, it may not be. Consequently, ``m_hSphere`` is never written onto the
disk, and upon restore, the entire array is zero-initialised and losing all
health spheres.

Talk monster
------------

A talk monster is a class that is overridden by monsters that can talk,
including barney guards and scientists. A talk monster makes idle chatter from
time to time. This is done mostly by the ``GetScheduleOfType`` function which
returns chatter schedules based on non-shared RNG (see :ref:`nonshared rng`).

Notably, talk monsters have the ability to move away from a player's push, coded
by the ``slMoveAway`` schedule. In the schedule definition, we see that a talk
monster walks for 100 units before stopping and yawing towards the player.

Talk monsters generally can be used by the player to follow him. The
``FollowerUse`` function is responsible of checking the conditions for following
and calling ``StartFollowing`` on the player entity. In the ``StartFollowing``
function, ``m_hTargetEnt`` is assigned to be the player entity. Subsequently,
the specific schedules and tasks a monster takes to actually do the following
can vary.

Take the scientist in ``scientist.cpp`` as an example. When the monster state is
*idle* or *alert*, ``GetSchedule`` will check for some conditions and ultimately
call ``GetScheduleOfType(SCHED_TARGET_FACE)`` (or the "scared" counterpart),
which returns ``slFaceTarget`` in the right conditions. In the definition for
the ``slFaceTarget`` schedule, we see that the ``TASK_SET_SCHEDULE`` is defined
with ``SCHED_TARGET_CHASE`` as its parameter. When this task is executed,
``GetScheduleOfType(SCHED_TARGET_CHASE)`` will return ``slFollow``, which is the
final schedule that actually makes the scientist moves to the target pointed by
``m_hTargetEnt``, which is the player if used earlier. A similar tracing can be
done for barney.

.. note:: Not all monsters who can talk are talk monsters. For example, the
          G-Man can speak scripted sentences, but he inherits from
          ``CBaseMonster``.

Barney
~~~~~~

Barney guards are common in Half-Life. They play a vital role in a few very
time-saving tricks in Half-Life speedruns.

Due to wearing a vest, the damage received when hitting the stomach may be
halved, depending on the type of damage. This is confirmed by looking at
``TraceAttack``:

.. code-block:: cpp

   case HITGROUP_STOMACH:
     if (bitsDamageType & (DMG_BULLET | DMG_SLASH | DMG_BLAST))
     {
       flDamage = flDamage / 2;
     }
     break;

A barney guard will take cover from his enemy when he receives heavy damage,
specifically, when ``bits_COND_HEAVY_DAMAGE`` is set. This bit is set when a
monster receives a damage :math:`D \ge 20`, according to
``CBaseMonster::TakeDamage`` in ``combat.cpp``.

The barney is also known to retaliate when the player attacks him. However, not
all damage from the player will cause him to do so. Specifically, if the player
attacks barney for the first time but is not looking at him (determined by the
``IsFacing`` function), then the guard will become suspicious but still give the
player the benefit of the doubt. However, any attack the second time will make
barney mad and make the player the enemy. This is done by setting the
``bits_MEMORY_PROVOKED`` bit to ``m_afMemory``. As a result, the next time
``RunAI`` is called, ``GetEnemy`` will be called, which in turn calls
``BestVisibleEnemy``. ``BestVisibleEnemy`` then iterates through a linked list
of monsters, and selects an enemy based on ``IRelationship``. Looking at
``CTalkMonster::IRelationship``, we see that, indeed, when
``bits_MEMORY_PROVOKED`` is set, this function returns ``R_HT``, representing
hatred.

When ``m_hEnemy`` is the player, the barney will begin to attack the player like
any other enemy. The behaviour of attacking and chasing the player is similar to
that of other attacking monsters.

.. TODO Chase Enemy, Range Attack1

Scientist
~~~~~~~~~

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
