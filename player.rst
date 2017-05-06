Player fundamentals
===================

The *player* refers to the self. Specifically it is not necessarily *you*, but rather the *self* in the Half-Life universe.

Input
-----

All player movements can be controlled through commands. In the default game setup, pressing down the "W" key usually results in the ``+forward`` command being issued. Releasing the same key will cause ``-forward`` to be issued. This is because the "W" key is bound to the ``+forward`` command with the ``bind`` command, usually issued from ``config.cfg``. The ``-forward`` command needs not be explicitly bound.

There are many similar commands available. It is beyond the scope of this documentation to provide a detailed description for all commands and indeed all cvars. The reader is invited to generate a list of all commands with the ``cmdlist`` command and study the SDK code for each of them.

There are, however, a few points to note about command issuing that are of concern to speedrunning. One of them is the *impulse down* phenomena. This affects primarily the viewangles (see :ref:`player viewangles`) and the FSU (see :ref:`FSU`) computations. For example, the viewangles are typically changed by one of the viewangles commands such as ``+left`` for yawing left. This is done by adding to subtracting the viewangles by the value

.. math:: \tau \times \mathtt{cl\_yawspeed/cl\_pitchspeed} \times \mathrm{key state}

The "key state" is the state of the command being issued (``+left`` for example). The key state is typically 1, but in the *first frame* in which the command is being issued the value is 0.5. In other words, the change in viewangles is half of what it normally is in the *first frame* of the active command.

This is not limited to the viewangles. The FSU values (which is crucial to player movement as will be described in :ref:`FSU`) are also affected by the impulse down. For example, by issuing ``+forward``, the following value will be added to :math:`F`:

.. math:: \mathtt{cl\_forwardspeed} \times \mathrm{key state}

Again, the key state here is typically 1, except the first frame of the ``+forward`` command. This can result in a noticeably drop in player acceleration.

.. tip:: The reader is advised to perform a detailed study of ``cl_dlls/input.cpp`` to understand the processes and computations involved to greater depths.

.. _player viewangles:

Viewangles
----------

The term *viewangles* is usually associated with the player entity. The viewangles refer to a group of three angles which describe the player's view orientation. We call these angles *yaw*, *pitch* and *roll*. Mathematically, we denote the yaw by

.. math:: \vartheta

and the pitch by

.. math:: \varphi

Note that these are different from :math:`\theta` and :math:`\phi`. We do not have a mathematical symbol for roll as it is rarely used. In mathematical discussions, the viewangles are assumed to be in *radians* unless stated otherwise. However, do keep in mind that they are stored in degrees in the game.

One way to change the yaw and pitch is by moving the mouse. This is not useful for tool-assisted speedrunning, however. A better method for precise control of the yaw and pitch angles is by issuing the commands ``+left``, ``+right``, ``+up``, or ``+down``. When these commands are active, the game increments or decrements the yaw or pitch by a certain controllable amount per frame. The amounts can be controlled by adjusting the variables ``cl_yawspeed`` and ``cl_pitchspeed``. For instance, when ``+right`` is active, the game multiplies the value of ``cl_yawspeed`` by the frame time, then subtracts the result from the yaw angle.

.. TODO: should we talk about anglemod in the discussion about client-server in Game fundamentals?

Anglemod
~~~~~~~~

When the viewangles are sent to the server, their values *in degrees* are rounded slightly using the *anglemod* function, which will be denoted :math:`\mathfrak{A}`. The *degrees-anglemod* function may be mathematically written as

.. math:: \mathfrak{A}_d(x) = \frac{360}{65536} \left( \operatorname{int}\left( x \frac{65536}{360} \right) \mathbin{\mathtt{AND}} 65535 \right)

where :math:`\operatorname{int}(x)` denotes the integer part of :math:`x`. Similarly, the *radians-anglemod* function may be written as

.. math:: \mathfrak{A}_r(x) = \frac{2\pi}{65536} \left( \operatorname{int}\left( x \frac{65536}{2\pi} \right) \mathbin{\mathtt{AND}} 65535 \right)

Observe that :math:`0^\circ \le \mathfrak{A}_d(x) < 360^\circ` and :math:`0 \le \mathfrak{A}_r(x) < 2 \pi`, regardless of :math:`x`. To see this, first assume :math:`x \ge 0`. Then, the ``AND`` operation extracts only the lower 16 bits of the first integer argument. This is mathematically equivalent to modulo :math:`65536`. Now if :math:`x < 0`, then recall from the two's complement representation that the *signed* integer representing some negative value :math:`-a` (with :math:`a > 0`) has a positive value of :math:`2^{32} - a` if interpreted as an *unsigned* integer. Now,

.. math::
   \begin{align*}
   (2^{32} - a) \mathbin{\mathtt{AND}} (2^{16} - 1)
   &= (2^{32} - a) \bmod 2^{16} \\
   &= 2^{32} - a - \left\lfloor \frac{2^{32} - a}{2^{16}} \right\rfloor 2^{16} \\
   &= 2^{32} - a - \left\lfloor 2^{16} - \frac{a}{2^{16}} \right\rfloor 2^{16} \\
   &= 2^{32} - a - 2^{32} + \left\lceil \frac{a}{2^{16}} \right\rceil 2^{16} \\
   &= \left\lceil \frac{a}{2^{16}} \right\rceil 2^{16} - a
   \end{align*}

To proceed further, write :math:`a = q 2^{16} + r` where :math:`q` and :math:`r` are integers and :math:`0 \le r < 2^{16}` is the integer remainder when :math:`a` is divided by :math:`2^{16}` (remember that :math:`a \ge 0`). Then

.. math:: \left\lceil \frac{a}{2^{16}} \right\rceil 2^{16} - a
   = \left\lceil q + \frac{r}{2^{16}} \right\rceil 2^{16} - 2^{16} q - r
   = \left\lceil \frac{r}{2^{16}} \right\rceil 2^{16} - r

Since :math:`0 \le r = a \bmod 2^{16} < 2^{16}`, this simplifies to

.. math:: -a \mathbin{\mathtt{AND}} 2^{16} =
   \begin{cases}
   2^{16} - r & r \ne 0 \\
   0 & r = 0
   \end{cases}

Anglemod introduces a loss of precision in setting angles. This can result in a loss of optimality in strafing. There are two ways to reduce the effects of anglemod, namely by the *simple anglemod compensation* and the more advanced *vectorial compensation*. These techniques will be described in :ref:`strafing`.

.. _view vectors:

View vectors
------------

There are two vectors associated with the player's viewangles. These are called the *view vectors*. For discussions in 3D space, they are defined to be

.. math::
   \begin{align*}
   \mathbf{\hat{f}} &:= \langle \cos\vartheta \cos\varphi, \sin\vartheta \cos\varphi, -\sin\varphi \rangle \\
   \mathbf{\hat{s}} &:= \langle \sin\vartheta, -\cos\vartheta, 0 \rangle
   \end{align*}

We will refer to the former as the *unit forward vector* and the latter as the *unit right vector*. The negative sign for :math:`f_z` is an idiosyncrasy of the GoldSrc engine inherited from Quake. This is the consequence of the fact that looking up gives negative pitch angles and looking down gives positive pitch angles.

We sometimes restrict our discussions to the horizontal plane, such as in the description of strafing. In this case we assume :math:`\varphi = 0` and define

.. math::
   \begin{align*}
   \mathbf{\hat{f}} &:= \langle \cos\vartheta, \sin\vartheta \rangle \\
   \mathbf{\hat{s}} &:= \langle \sin\vartheta, -\cos\vartheta \rangle
   \end{align*}

Such restriction is equivalent to projecting the :math:`\mathbf{\hat{f}}` vector onto the :math:`xy` plane, provided the original vector is not vertical.

The above definitions are not valid if the roll is nonzero. Nevertheless, the roll is very rarely nonzero in practice, and so it rarely affects the physics described in this document, if at all.

Punchangles
-----------

The punchangles can refer to the client side or the server side values. The client side punchangles are usually affected by weapon recoil and are cosmetic in nature. Namely, they do not affect the aiming viewangles of the player. The player may be aiming with zero pitch while the camera appears to point elsewhere. The server side punchangles, on the other hand, affects the viewangles and therefore the aiming. The server side punchangles are affected by certain types of damage (see :ref:`health and damage`) and punches from monsters (which are different from the purely damage itself).

.. TODO: the client side value can be set to server side after a saveload?

The punchangles may be denoted as :math:`\mathbf{P}`, consisting of punch pitch, punch yaw, and punch roll. When the punchangles are nonzero, the game will smoothly decrease the angles until all of them become zero. In each frame, the game calculates

.. math:: \mathbf{P}' = \max\left( 0, \lVert\mathbf{P}\rVert \left( 1 - \frac{1}{2} \tau \right) - 10\tau \right) \mathbf{\hat{P}}

The punchangles are rarely big issues except when the punch yaw and punch roll are nonzero. In these cases, strafing (:ref:`strafing`) can be affected. Though this very rarely happens.

When a saveload is performed, the punchangles will be added to the viewangles permanently, while the punchangles will be set to zero. When this happens, the viewangles will not be reduced gradually like the case when punchangles are nonzero.

.. _FSU:

Forwardmove, sidemove, and upmove
---------------------------------

When the movement keys are held, there exists three values, :math:`F`, :math:`S`, and :math:`U`, that are set. These values are called the *forwardmove*, *sidemove*, and *upmove* respectively, or *FSU* for short, and are used in player movement physics (see :ref:`player movement`).

``+forward`` and ``+back``
   Assigns the positive or negative ``cl_forwardspeed`` to :math:`F`

``+moveright`` and ``+moveleft``
   Assigns the positive or negative ``cl_sidespeed`` to :math:`S`

``+moveup`` and ``+movedown``
   Assigns the positive or negative ``cl_upspeed`` to :math:`U`
