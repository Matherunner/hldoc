Game fundamentals
=================

This page describes the notations that we will use throughout this documentation. We will also introduce some basic concepts that will be used and assumed in all our discussions.

.. _tracing:

Tracing
-------

Tracing is one of the most important computations done by the game. Tracing is done countless times per frame, and it is vital to how entities interact with one another.

.. note:: expansion needed

Randomness
----------

The Half-Life universe is full of uncertainties, much like our universe at the level of quantum mechanics. Randomness in Half-Life is sourced in two ways: by means of the *shared RNG* and the *non-shared RNG*. These are custom written pseudo-RNGs that are powered by vastly different algorithms. The shared RNG is so named because it is computed by the game server and shared with the game clients, while the non-shared RNG is computed independently by the game server and clients without any kind of sharing or synchronisation between them.

.. _shared rng:

Shared RNG
~~~~~~~~~~

The shared RNG code is open source and written in ``dlls/util.cpp`` in the Half-Life SDK. The shared RNG barely qualifies as an RNG given how it is used, and especially due to the fact that, given a fixed interval :math:`[l, h)`, the RNG only returns 253 possible values within the bounds, as we will explain below. The only uses of the shared RNG in Half-Life are related to weapon behaviours and bullet spreads (see :ref:`bullet spread`).

For some context, a typical pseudo-RNG must be seeded prior to use, for a pseudo-RNG needs to have its initial state defined. To put it differently, let :math:`S_0` be the initial state of a typical pseudo-RNG. To use this RNG, we must first call a seeding function :math:`S_0 \gets \operatorname{Seed}(s)` with some value :math:`s`, which is often just the current unix timestamp. Then, the next pseudorandom number is given by :math:`x_0` where :math:`(S_1, x_0) \gets f(S_0)`. In general, the :math:`i`-th pseudorandom number is given by :math:`(S_{i+1}, x_i) \gets f(S_i)`.

.. TODO: which frame? probably not the usercmd frame, but need to explicitly state!

However, the Half-Life shared RNG is used differently. A "seed" in this context refers to an integer that appears to increment sequentially every frame. This integer is stored as the class variable ``CBasePlayer::random_seed``. This variable is set in ``CmdStart`` to the value of its ``random_seed`` parameter:

.. code-block:: cpp
   :caption: ``CmdStart``, ``dlls/client.cpp``
   :emphasize-lines: 8

   void CmdStart( const edict_t *player, const struct usercmd_s *cmd, unsigned int random_seed )
   {
     entvars_t *pev = (entvars_t *)&player->v;
     CBasePlayer *pl = dynamic_cast< CBasePlayer *>( CBasePlayer::Instance( pev ) );

     [...omitted...]

     pl->random_seed = random_seed;
   }

``SV_RunCmd`` in the engine code supplies the value of the seed to ``CmdStart``. The ultimate source of the seed value appears to be dependent on the latest incoming sequence number of the client-server channel. This part of the code is not open source, and therefore not well researched. Nonetheless, empirical and field evidence shows that the seed value obtained in ``CmdStart`` appears to be sequential from frame to frame, or at least, increments in a very predictable way.

The shared RNG may be denoted as :math:`\mathfrak{U}_S(\sigma, l, h)`, where :math:`\sigma` is an integer, while :math:`l` and :math:`h` are floating point numbers representing the lower and upper bounds of the output, forcing the function to give a value within :math:`[l, h)`. The current shared seed value is typically given for :math:`\sigma`, although there are exceptions, such as in the computation of bullet spreads as explained in :ref:`bullet spread`. In the SDK code, :math:`\mathfrak{U}_S` is simply ``UTIL_SharedRandomFloat``. [#shared-RNG-float]_

The most important aspect of the shared RNG is that it returns only 253 possible values for a given interval :math:`[l, h)`. The reader is encouraged to read the SDK code for the implementation details. For a higher level overview here, when ``UTIL_SharedRandomFloat`` is called, it always initialises a global ``glSeed`` to one of the 256 possible values according to a 256-element lookup table. The previous value of ``glSeed`` prior to calling this function is completely discarded as a result. The index to the lookup table is computed by taking the lower 8-bits of the sum of the arguments of ``UTIL_SharedRandomFloat`` reinterpreted as 32-bit signed integers. What follows are computations involving ``glSeed`` and scaling of the output according to the bounds. Notice that because there are only 256 possible initial states, followed by deterministic and pure computations, there can only have a maximum of 256 possible output values. In reality, it is slightly worse than that: we counted the number of unique output values from :math:`\mathfrak{U}_S` (given fixed :math:`l` and :math:`h`), and there are only 253 of them. It is therefore quite a stretch to describe the outputs of the shared RNG as "random".

.. _nonshared rng:

Non-shared RNG
~~~~~~~~~~~~~~

The code for the non-shared RNG is not officially publicly available. Nevertheless, we do not need to resort to reverse engineering as the C++ code for the non-shared RNG is available in the Xash3D engine code, the ReHLDS project, and the leaked Half-Life 2 source code, all of which look almost identical. The non-shared RNG is considerably more complex than the shared RNG. The non-shared RNG is used much more in Half-Life than the shared RNG. Examples of the uses of the non-shared RNG include the randomisation of the player's explosion target position, grenade tumbling velocities, delays between entity "thinks", NPC talking sequences and general behaviours, the pitches of sounds, cosmetics and effects, and much more.

Given the complexity of the non-shared RNG algorithm, we will not attempt to describe how it works here. We can say that it appears to be seeded based on the current unix timestamp. This meant that, in principle, we can change the system clock and restart Half-Life to alter the random behaviours and phenomena in the game. There are two functions exposed to the users to obtain the next random value: the integer version :math:`\mathfrak{U}_{\mathit{NS}}(S,l,h)` and the floating point version :math:`\mathfrak{U}_{\mathit{NS}}(S,l,h)`. Both of these rely on some global state :math:`S`.

.. _frame rate:

Frame rate
----------

When we think of the concept of *frame rate*, or sometimes somewhat incorrectly referred to by its unit of measurement *frames per second* or *fps*, we think of the refresh rate of the screen when playing Half-Life. However, it is crucial to distinguish between three different types of frame rate:

rendering frame rate
  This is the real-time rate at which graphics are painted on the screen, denoted as :math:`f_r = \tau_r^{-1}`. This definition maps to what is normally thought of as the frame rate. The rendering frame rate is usually limited by ``fps_max`` in normal gameplay, though if ``host_framerate`` is set, then ``fps_max`` is ignored. Other factors can also limit the maximum frame rate, including, but not limited to, the "vertical sync" setting (in-game or otherwise) and ``fps_override``.

game frame rate
  This is the *virtual* rate at which the majority (with player movement being the important exception) of the game physics are run, denoted as :math:`f_g = \tau_g^{-1}`. The game frame rate is typically in sync with the rendering frame rate, though not always. For example, suppose a computer is not able to render the graphics beyond a rendering frame rate of 500 fps, but ``host_framerate`` is set to 0.001. This forces the physics to run at a virtual 1000 fps, though because the screen does not update that frequently, the game appears to run twice as slow in real time.

player frame rate
  The player frame rate is the *virtual* frame rate at which the majority of the player movement physics (see :ref:`player movement`) are run, denoted as :math:`f_p = \tau_p^{-1}`. The player frame rate roughly corresponds to the game frame rate. Depending on the engine version, whether the game is paused, and the value of the game frame rate itself, the player frame time :math:`\tau_p` may oscillate between different values, stay at zero, or be rounded towards zero to the nearest 0.001.

Slowdown on older engines
~~~~~~~~~~~~~~~~~~~~~~~~~

.. TODO: fix this slow down graph, we have defined it to be the inversion?

.. .. figure:: images/frame_rate_unsync.png
..    :name: frame rate unsync

..    Frame rate dependent slow-down of player movement in older Half-Life engines.

.. FIXME: this is misleading, this implies that on newer engines, the player frame rate is not rounded down. But it still is. It's just that the game also considers frame time remainders.

Suppose the game frame rate is higher than 20 fps. On older game engines, roughly before build 6027, the player frame rate equals the game frame rate rounded towards zero to the nearest 0.001, as mentioned above. Namely, we have

.. math:: \tau_p = \frac{\left\lfloor 1000 \tau_g \right\rfloor}{1000}

The slowdown factor is then defined as

.. math:: \eta = \frac{\tau_p}{\tau_g} = \frac{\left\lfloor 1000\tau_g \right\rfloor}{1000\tau_g} = \frac{f_g}{1000} \left\lfloor \frac{1000}{f_g} \right\rfloor = \frac{f_g}{f_p}
  :label: slowdown factor

When the slowdown factor is less than one, the actual movement speed of the player will be lower. The player's position update described in :ref:`player position update` uses :math:`\tau_p` but runs at the rate of :math:`\tau_g^{-1}` Hz. Indeed, the real velocity of the player is directly proportional to :math:`\eta`:

.. math:: \frac{\mathbf{r}' - \mathbf{r}}{\tau_g} = \frac{\mathbf{r} + \tau_p \mathbf{v}' - \mathbf{r}}{\tau_g} = \frac{\tau_p}{\tau_g} \mathbf{v}' = \eta \mathbf{v}'

For instance, a trick known as the "501 fps slowdown" was implemented in Half-Life 21 (see :ref:`half-life-21`) to permit opening and passing through doors in the Questionable Ethics chapter without stopping dead by the doors before they could be opened fully. The slowdown factor at 501 fps is :math:`\eta = 0.501`, implying the real velocity is roughly half the intended player velocity. On pre-Steam versions of Half-Life and its expansions, the default frame rate is 72 fps (and some speedrunners believe it should not be exceeded), which would give a slowdown factor of :math:`\eta = 117/125 = 0.936`.

It is a well known fact that the slowdown factor :math:`\eta = 1` if and only if :math:`1000/f_g` is an integer. This is because as seen in :eq:`slowdown factor`, if :math:`\eta = 1` we must have

.. math:: \left\lfloor \frac{1000}{f_g} \right\rfloor = \frac{1000}{f_g}

which is only possible if :math:`1000/f_g` is an integer.

Savestates
----------

.. _delta:

DELTA
-----

The DELTA mechanism is one of the ways Half-Life uses to save bandwidth in
client-server communication.

TODO


Walking through a frame
-----------------------

This section attempts to outline some of the major events relevant to speedrunning that happen in a frame. Extreme detail on how each part of the game engine works is beyond the scope of this documentation. In fact, some believe that code is documentation! Until Valve releases the source code of Half-Life, one can study the Xash3D engine source or the disassembly of Half-Life.

.. rubric:: Footnotes

.. [#shared-RNG-float] We omit any mention of the integer version of the shared RNG, ``UTIL_SharedRandomLong``, because no code is calling this function in the SDK. It also behaves very similarly to the floating point version with only minor differences.
