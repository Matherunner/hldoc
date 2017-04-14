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

Camera
------

.. _player viewangles:

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

.. _FSU:

Forwardmove, sidemove, and upmove
---------------------------------
