Game basics
===========

This documentation largely focuses on game mechanics which involve the player one way or another. Nevertheless, the player doesn't exist in a vacuum: it interacts with the engine and core aspects of the game. For example, the *frame rate* (see :ref:`frame rate`) plays an outsized role in the player movement physics. In this page, we will describe only aspects of the engine and "lower level" game mechanics necessary to understand and exploit Half-Life for speedrunning purposes.

Versioning
----------

Half-Life was first released in 1998. The game has since undergone many changes, though not in the core casual gameplay mechanics and campaign. Changes are usually confined to bug fixes, console command changes, small movement physics alterations, server administration improvements, and quality of life updates. Nevertheless, some ostensibly minor tweaks or bug fixes can neuter critical speedrun tricks and exploits. The most notorious of which is none other than the "bunnyhop cap" (see :ref:`bunnyhop cap`). Community knowledge points to exe version 1.1.0.8 released in 2001 as the first version carrying the "fix". As of 2026, all subsequent versions have the bunnyhop cap, and it is very unlikely Valve will officially remove it.

In speedrunning, the term "version" is ambiguous and usually context dependent. When we talk about Half-Life versions, we are usually concerned with how the version impacts game mechanics (such as the aforementioned bunnyhop cap). The most pertinent is the *engine version*. The `Valve developer community wiki`_ contains a page listing out all Half-Life engine versions. On the page, observe that there isn't a singular "version" as far as the engine is concerned. There are at least the following versioning dimensions:

.. _Valve developer community wiki: https://developer.valvesoftware.com/wiki/GoldSrc/Engine_versions

- engine or exe build number, e.g. 8684
- exe version string, e.g. 1.1.0.8
- protocol version, e.g. 48

The most precise way to refer to a specific official release of the game is by referencing the build number. To find out the build number of a game, we could launch the game and run the ``version`` command in the developer console, or reverse engineer the ``hw.dll`` to examine the value returned by the ``build_number`` function.

Many engine builds share a common set of characteristics which distinguish them from other builds. To help distinguish the most important characteristics among the engine builds, speedrunners categorise them most broadly as **WON** and **Steam**. Broadly speaking, the WON versions of Half-Life refer to versions of the game prior to being released on Steam, and while Steam versions are those released on Steam. We can further divide Steam into **pre-SteamPipe**, **SteamPipe**, and **25th anniversary**. More importantly are the distinguishing characteristics of each category. Most speedrunners adopt the following mental model.

**WON**
  Maximum frame rate of 100 fps. Version 1.1.0.7 and earlier do not have the bunnyhop cap, while 1.1.0.8 and after do. No quickgauss (:ref:`quickgauss`). No easy repeated action scripts with ``_special``. The first crowbar hit has a higher damage.

**Steam, pre-SteamPipe**
  Maximum frame rate raised to 1000 fps. All builds under the pre-SteamPipe category have the bunnyhop cap. Quickgauss works. Scripting with ``_special`` possible. The "501 fps slow down" trick works (see :ref:`501fps slowdown`).

**Steam, SteamPipe**
  No limit to frame rate with some nuances detailed in :ref:`frame rate`, but the code change caused the 501 fps slowdown trick to stop working. Scripting with ``_special`` disabled by Valve despite `pleas from the community <Github Issue_>`_. Later versions since `some time in 2019 <turning fix_>`_ fixed an issue where NPCs turn very slowly at higher frame rates.

.. _Github Issue: https://github.com/ValveSoftware/halflife/issues/1154
.. _turning fix: https://store.steampowered.com/news/app/70/view/1586880891220596671

**Steam, 25th anniversary**
  Object boosting and manoeuvring (:ref:`object manoeuvre`) no longer works. Use key braking removed entirely. The first crowbar hit has a higher damage similar to the WON versions.

This categorisation method will likely stay unmodified indefinitely. As Valve rarely intentionally reverts bug fixes, and the 25th anniversary is generally considered unattractive for speedrunning, future releases of Half-Life will very likely be ignored by the community and therefore do not call for new categorisation.

Version preference
~~~~~~~~~~~~~~~~~~

Manual speedrunners or RTA runners generally prefer the WON version, with an important nuance which we will describe in the :ref:`subsequent section <dll or game version>`. This is primarily due to levelling out the hardware playing field by forcing a cap of 100 fps, lack of bunnyhop cap, and lack of later "fixes" to NPC turn rate and object boosting. The lack of the *extremely* powerful quickgauss in WON is apparently not a big enough downside for RTA speedrunners, especially in light of uncapped bunnyhop. Exploiting the "infinite health door" in the Surface Tension chapter also takes several more seconds in WON compared to Steam, but the community considers this an acceptable trade off.

Tool-assisted speedrunners, however, generally prefer the Steam versions. Tooling is generally better for the Steam versions: for one, Linux binaries with DWARF_ debug symbols are only available in Steam versions. Official vanilla untouched versions are also considered, at least by the author of this documentation, to be "purer", compared to what is commonly done for the WON version used by RTA runners (again, see :ref:`dll or game version`). This matters more to TASes as they run a higher risk of being accused of cheating. The deterrence of bunnyhop cap also matters less because the player could still maintain movement speed by precise :ref:`ducktapping <ducktapping>`. Quickgauss is also much more exploitable in a TAS because inhuman precision is required to control the player at extreme speeds made possible by it. Many would consider creating a TAS on a WON version to be not making full use of the precision afforded by tool assistance. Most importantly, Steam versions allow pinning the frame rate at 1000 fps, which maximises strafing acceleration (see :ref:`strafing`).

As this documentation is primarily focused on TAS applications, we will prioritise our analysis of Half-Life game mechanics on the Steam versions, particularly those before the 25th anniversary changes. As mentioned earlier, the changes brought upon by the 25h anniversary version are poorly received by the speedrunning community. The lack of object boosting to instantly max out the movement speed is too big of a trade off in exchange for nothing of speedrunning value. The inability to perform use key braking is also a deal breaker for high-speed precise TASing.

.. _DWARF: https://en.wikipedia.org/wiki/DWARF

At the time of writing, the last Steam versions generally used for speedrunning are build 6153 and perhaps build 8684 or earlier. There is nothing fundamentally special about build 6153, except that it is the first SteamPipe version (according to tribal knowledge) and it comes with the commonly used `GoldSrc Package 2.4 <goldsrc package_>`_ circulated among speedrunners.

.. _goldsrc package: https://forums.sourceruns.org/t/goldsrc-package-2-4/2634

.. _dll or game version:

Game/DLL version
~~~~~~~~~~~~~~~~

Unfortunately, there is one aspect of Half-Life which makes matters even more confusing. Broadly speaking, the game is modular, consisting of an engine component and a "game/DLL" component. The engine component refers to the following binaries (and their macOS and Linux equivalents):

- ``hw.dll``
- ``sw.dll`` (if present)
- ``hl.exe``

Meanwhile, the "game/DLL" component refers to the following and their equivalents:

- ``hl.dll``
- ``client.dll``
- ``opfor.dll`` (for Half-Life: Opposing Force)

In vanilla Half-Life, this distinction is less critical because when Valve releases a "build", it comes bundled with the corresponding game/DLL component, which may or may not contain code changes specific to that release. However, in modding and speedrunning, *the game/DLL of one release may be swapped for the game/DLL from a different release*. There are multiple reasons for doing this.

The primary reason is that the game/DLL component is source-available on Github as the `Half-Life SDK <HLSDK_>`_ (HLSDK). Modding sometimes entails modifying the source code then distributing the compiled binaries as modified ``hl.dll`` and ``client.dll``, often on `ModDB`_. Sometimes, a mod only distributes a mod folder (akin to the ``valve`` folder) containing only the game/DLL component. The player could easily and conveniently install this into an existing Half-Life installation, which could be running any engine build.

In Half-Life speedrunning since the mid-2010s, this swap is often a solution for those who wish to speedrun on the WON version but are hindered by compatibility and tooling issues on modern systems when running the original game outright. Since many desirable characteristics, such as the absence of bunnyhop cap, are determined by the game/DLL component, a runner can take a more modern Steam-based engine and swap in the older WON game/DLL, creating a "mixed breed" setup.

.. _HLSDK: https://github.com/ValveSoftware/halflife
.. _ModDB: https://www.moddb.com/games/half-life/mods

There is, however, a risk that a runner using a mixed breed version might configure settings that are impossible in any vanilla version. For instance, increasing the frame rate beyond 100 fps while bunnyhopping without a cap. This impossible combination was used to produce the landmark and esteemed :ref:`HL21 <half-life-21>` segmented speedrun, which modern community standards have since reevaluated as not wholly legitimate. To prevent this, the community established rules to ensure a speedrunning experience that remains as close to the original unmodified WON release as possible, while retaining the quality of life and compatibility updates of the Steam engine. The results of this approach can be seen in the `GoldSrc Package <goldsrc package_>`_ and `Half-Life 2005 Package <half-life-2005-package_>`_.

.. _half-life-2005-package: https://bxt.rs/files/goldsrc/Half-Life%202005%20WON.7z

Since Valve do not make large changes to Half-Life and speedruns have become ever closer to optimality, we do not expect the above setups and arrangements to change meaningfully for, perhaps, forever.

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

.. _501fps slowdown:

Slowdown on older engines
~~~~~~~~~~~~~~~~~~~~~~~~~

.. TODO: fix this slow down graph, we have defined it to be the inversion?

.. .. figure:: images/frame_rate_unsync.png
..    :name: frame rate unsync

..    Frame rate dependent slow-down of player movement in older Half-Life engines.

.. FIXME: this is misleading, this implies that on newer engines, the player frame rate is not rounded down. But it still is. It's just that the game also considers frame time remainders.

Suppose the game frame rate is higher than 20 fps. On older game engines, roughly before build 6027, the player frame rate equals the game frame rate rounded towards zero to the nearest 0.001, as mentioned above. Namely, we have

.. math:: \tau_p = \frac{\left\lfloor 1000 \tau_g \right\rfloor}{1000}.

.. prf:definition:: Slowdown factor
  :label: slowdown factor

  The slowdown factor is defined as the fraction

  .. math:: \eta = \frac{\tau_p}{\tau_g} = \frac{\left\lfloor 1000\tau_g \right\rfloor}{1000\tau_g} = \frac{f_g}{1000} \left\lfloor \frac{1000}{f_g} \right\rfloor = \frac{f_g}{f_p}.
    :label: slowdown factor

When the slowdown factor is less than one, the actual movement speed of the player will be lower. The player's position update described in :ref:`player position update` uses :math:`\tau_p` but runs at the rate of :math:`\tau_g^{-1}` Hz. Indeed, the real velocity of the player is directly proportional to :math:`\eta`, since

.. math:: \frac{\mathbf{r}' - \mathbf{r}}{\tau_g} = \frac{\mathbf{r} + \tau_p \mathbf{v}' - \mathbf{r}}{\tau_g} = \frac{\tau_p}{\tau_g} \mathbf{v}' = \eta \mathbf{v}'.

For instance, a trick known as the "501 fps slowdown" was implemented in Half-Life 21 (see :ref:`half-life-21`) to permit opening and passing through doors in the Questionable Ethics chapter without stopping dead by the doors before they could be opened fully. The slowdown factor at 501 fps is :math:`\eta = 0.501`. With this slowdown factor, the real velocity is roughly half the developer-intended player velocity.

It's also worth noting that on pre-Steam versions of Half-Life and its expansions, the default frame rate is 72 fps (and some speedrunners believe it should not be exceeded), which would give a slowdown factor of :math:`\eta = 117/125 = 0.936`. It's interesting that some retail releases made the player move roughly 7% slower than the intended speed.

The following theorem is a well known fact among speedrunners: by setting an appropriate value for the game frame rate :math:`f_g`, the player would experience no slowdown.

.. prf:theorem:: No-slowdown frame rate
  :label: no-slowdown frame rate

  The slowdown factor :math:`\eta = 1` if and only if :math:`1000/f_g` is an integer.

.. prf:proof::

  By the last equality in :eq:`slowdown factor`, :math:`\eta = 1` if and only if :math:`f_g = f_p` if and only if

  .. math:: \left\lfloor \frac{1000}{f_g} \right\rfloor = \frac{1000}{f_g},

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
