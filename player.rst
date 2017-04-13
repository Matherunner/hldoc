Player fundamentals
===================

The *player* refers to the self. Specifically it is not necessarily *you*, but rather the *self* in the Half-Life universe.

Camera
------

Viewangles
~~~~~~~~~~

The term *viewangles* is usually associated with the player entity. The viewangles refer to a group of three angles which describe the player's view orientation. We call these angles *yaw*, *pitch* and *roll*. Mathematically, we denote the yaw by

.. math:: \vartheta

and the pitch by

.. math:: \varphi

Note that these are different from :math:`\theta` and :math:`\phi`. We do not have a mathematical symbol for roll as it is rarely used. In mathematical discussions, the viewangles are assumed to be in *radians* unless stated otherwise. However, do keep in mind that they are stored in degrees in the game.

One way to change the yaw and pitch is by moving the mouse. This is not useful for tool-assisted speedrunning, however. A better method for precise control of the yaw and pitch angles is by issuing the commands ``+left``, ``+right``, ``+up``, or ``+down``. When these commands are active, the game increments or decrements the yaw or pitch by a certain controllable amount per frame. The amounts can be controlled by adjusting the variables ``cl_yawspeed`` and ``cl_pitchspeed``. For instance, when ``+right`` is active, the game multiplies the value of ``cl_yawspeed`` by the frame time, then subtracts the result from the yaw angle.

.. TODO: should we talk about anglemod in the discussion about client-server in Game fundamentals?

When the viewangles are sent to the server, their values *in degrees* are rounded slightly using the *anglemod* function, which will be denoted :math:`\mathfrak{A}`. The *degrees-anglemod* function may be mathematically written as

.. math:: \mathfrak{A}_d(x) = \frac{360}{65536} \operatorname{int}\left( x \frac{65536}{360} \right)

where :math:`\operatorname{int}(x)` denotes the integer part of :math:`x`. Similarly, the *radians-anglemod* function may be written as

.. math:: \mathfrak{A}_r(x) = \frac{\pi}{32768} \operatorname{int}\left( x \frac{32768}{\pi} \right)

View vectors
~~~~~~~~~~~~

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
~~~~~~~~~~~

Ducking
-------

Jumping
-------

When the jump bit is set, the player will jump. To be precise, the act of jumping refers to setting the vertical velocity to

.. math:: v_z = \sqrt{2 \cdot 800 \cdot 45} = 120 \sqrt{5} \approx 268.3

The unsimplified expression for the vertical velocity is how it is calculated in the code. It implies the intention of jumping to the height of 45 units with :math:`g = 800`, though all of the numbers are hardcoded constants independent of any game variables.

The condition of jumping is being onground.

.. _jumpbug:

Jumpbug
~~~~~~~

.. _duckjump:

Duckjump
~~~~~~~~

Gravity
-------

Like other entities in the Half-Life universe, the player experiences gravity. Whenever the player is in the air, a constant downward acceleration will be applied.

Air and ground movements
------------------------

Water movements
---------------
