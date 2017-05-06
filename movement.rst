.. _player movement:

Player movement basics
======================

.. TODO: talk about edgebug, slopejump?, player specific friction, edgefriction, basevelocity, put down FMEs, onground stuff!

In this chapter, we will focus on the fundamental governing equations for the air and ground player movements, and the exploitation of some of the miscellaneous physical phenomena. This chapter also serves as a prerequisite to :ref:`strafing`.

.. _player gravity:

Gravity
-------

Like other entities in the Half-Life universe, the player experiences gravity. Whenever the player is in the air, a constant downward acceleration will be applied. The gravity in the Half-Life universe works in a similar way to the Newtonian gravity in the real world. Namely, a free falling object experiences a *constant* acceleration of :math:`g`, with value specified by

.. math:: \mathtt{sv\_gravity} \times g_e

where :math:`g_e` is may be called the *entity gravity*, which is a modifier that scales the default gravity. Typically, :math:`g_e = 1`, though it can take a fractional value in Xen, for example. The consequence of a constant acceleration is that the velocity and position of the object at time :math:`t` is

.. math:: v_t = v_0 - gt, \quad s_t = s_0 + v_0 t - \frac{1}{2} g t^2

Recall that the Half-Life universe runs at quantised time, that is assuming constant frame rate we may write :math:`t = n\tau`. Or, :math:`t = \tau` after one frame. In Half-Life physics, the position is not calculated directly using the position equation above, but rather, it is obtained by integrating the velocity, namely :math:`\mathbf{r}' = \mathbf{r} + \tau \mathbf{v}`. Therefore, simply changing :math:`t` to :math:`\tau` in the equations to calculate the velocity and position in the next frame will not work well, because in essence that is equivalent to Euler's method. Not only will the errors accumulate over time, but also the jump height will be dependent on the frame rate. To see this, suppose the game calculates new vertical velocity :math:`v_z' = v_z - g\tau` in each frame, and uses :math:`v_z'` to calculate the position. Then

.. math:: r_z' = r_z + v_z' \tau = r_z + v_z \tau - g \tau^2 \ne r_z + v_z \tau - \frac{1}{2} g \tau^2

As one can see, this method does not give the correct expression for the vertical position after one frame.

To avoid these pitfalls from Euler's method, the game instead integrates the velocity using a form of the leapfrog_ method. Namely, by separating the gravitational computation into two stages: ``PM_AddCorrectGravity`` and ``PM_FixupGravityVelocity``, which are respectively called before and after updating the position. Ignoring :ref:`basevelocity` and entity gravity, the first function computes

.. _leapfrog: https://en.wikipedia.org/wiki/Leapfrog_integration

.. math:: \tilde{v}_z' = v_z - \frac{1}{2} g\tau

This velocity is then used for computing the new player position

.. math:: r_z' = r_z + \tilde{v}_z' \tau = r_z + v_z \tau - \frac{1}{2} g\tau^2

which is the correct expression for position. Finally, the velocity is computed by

.. math:: v_z' = \tilde{v}_z' - \frac{1}{2} g\tau

The velocity at the end of the frame is related to the velocity at the beginning of the frame by :math:`v_z' = v_z - g\tau`, which is also the correct expression according to classical mechanics.

It can be shown that the player locus is indeed independent of the frame rate, that is they fit the parabolic curve generated from classical mechanics perfectly. Consequently, the jump height is also independent of frame rate. Vertically launching from a ladder, however, does result in frame rate-dependent heights (see :ref:`ladder physics`).

.. note:: TODO: update ladder chapter

.. _basevelocity:

Basevelocity
------------

.. _player friction:

Ground friction
---------------

When the player is moving on the ground, friction will be applied to reduce the horizontal speed. The friction is applied before air and ground movement calculations (see :ref:`player air ground`) in ``PM_Friction``. The player friction differs from the friction applied to all other entities in that different types of friction is applied depending on the horizontal speed.

Let :math:`E` be the *stop speed*, the value of ``sv_stopspeed`` which is typically 100. Let :math:`k` be the value of

.. math:: \mathtt{sv\_friction} \times k_e \times e_f

which is usually 4 and where :math:`k_e` is called the *entity friction*. The entity friction can be modified by a friction entity (see :ref:`func_friction`). The :math:`e_f` is the *edgefriction* which will be described in a moment. It is usually 1 but can often be 2. The two dimensional player velocity immediately after applying friction (but before air or ground acceleration) is now

.. math:: \lambda(\mathbf{v}) =
   \begin{cases}
   (1 - \tau k) \mathbf{v} & \lVert\mathbf{v}\rVert \ge E \\
   \mathbf{v} - \tau Ek \mathbf{\hat{v}} & \max(0.1, \tau Ek) \le \lVert\mathbf{v}\rVert < E \\
   \mathbf{0} & \lVert\mathbf{v}\rVert < \max(0.1, \tau Ek)
   \end{cases}

Assuming :math:`\lVert\mathbf{v}\rVert \ge E`. Now observe that the player speed is scaled by a constant factor (assuming :math:`k` and :math:`\tau` are constant) each frame, resulting in an exponential decrease. This may be called *geometric friction*, because the series of speeds forms a geometric series. At higher horizontal speeds this type of friction can be devastating, because higher speeds are harder to achieve and maintain (owing to the sublinear growth of speed by pure strafing, see :ref:`strafing`).

At frame :math:`n`, the speed due to geometric friction is

.. math:: \lVert\mathbf{v}_n\rVert = \lVert\lambda^n(\mathbf{v})\rVert = (1 - \tau k)^n \lVert\mathbf{v}_0\rVert

Since time is discretised in the Half-Life universe, we have :math:`t = \tau n`. Therefore,

.. math:: \lVert\mathbf{v}_t\rVert = (1 - \tau k)^{t/\tau} \lVert\mathbf{v}_0\rVert

From this equation, it can be shown that the lower the friction, the greater the geometric friction. However, the difference in friction between different frame rates is so minute that one can hardly notice it.

Assuming :math:`\tau Ek \le \lVert\mathbf{v}\rVert < E`, the type of friction may be called *arithmetic friction*, because the speeds form an arithmetic series. Namely, we have

.. math:: \lVert\mathbf{v}_n\rVert = \lVert\mathbf{v}_0\rVert - n\tau Ek, \quad
   \lVert\mathbf{v}_t\rVert = \lVert\mathbf{v}_0\rVert - tEk

This type of friction is straightforward and independent of the frame rate.

Edgefriction
~~~~~~~~~~~~

Edgefriction is a an extra friction applied to the player when the player is sufficiently close to an edge that is sufficiently high above from a lower ground.

.. note:: TODO: maths descriptions

Although doubling :math:`k` seems minor at the first glance, the effect is *devastating*. Prolonged groundstrafing towards an edge can drastically reduce the horizontal speed, which in turn affects the overall acceleration from airstrafing after jumping off the edge. One way to avoid edgefriction is to jump or ducktap before reaching an edge and start airstrafing. However, this is sometimes impractical. The most optimal way to deal with edgefriction is highly dependent on the circumstances. Extensive offline simulations may be desirable.

.. _player air ground:

Air and ground movements
------------------------

The physics governing the player's air and ground movements are of primary importance. With precise inputs, they can be exploited to allow mathematically unbounded speed gain (barring ``sv_maxvelocity``). The consequences of the air and ground physics will be described in detail in :ref:`strafing`.

.. caution:: All vectors in this section are two dimensional on the :math:`xy` plane unless stated otherwise.

The air or ground accelerations are computed before position update. Assuming :math:`\mathbf{v}'` is the velocity after air or ground acceleration, and :math:`\mathbf{r}` the player position. Ignoring collision (see :ref:`collision`), the position update entails

.. math:: \mathbf{r}' = \mathbf{r} + \tau\mathbf{v}'

Here, the new velocity :math:`\mathbf{v}'` is given by the *fundamental movement equation* (FME). Let :math:`\mathbf{v}` the initial player velocity in *two dimensions*, namely the velocity immediately before friction and acceleration are applied. Then the FME is simply

.. math:: \mathbf{v}' = \lambda(\mathbf{v}) + \mu\mathbf{\hat{a}}

Here, :math:`\mathbf{\hat{a}}` is called the *unit acceleration vector*, given by

.. math:: \mathbf{\hat{a}} = \frac{F\mathbf{\hat{f}} + S\mathbf{\hat{s}}}{M}

A few notes to be made here. First, the :math:`F` and :math:`S` are the forwardmove and sidemove respectively, described in :ref:`FSU`. Second, :math:`\mathbf{\hat{f}}` and :math:`\mathbf{\hat{s}}` are the unit forward and side view vectors described in :ref:`view vectors`. But more importantly, they are obtained by assuming :math:`\varphi = 0`, regardless of the player's actual pitch. Consequently, they do not have a component in the :math:`z` axis. Third, assuming :math:`U = 0`, the :math:`M` has the value of

.. math:: M = \min\left( \mathtt{sv\_maxspeed}, \sqrt{F^2 + S^2} \right)

Observe that :math:`M` is always capped by ``sv_maxspeed``. Observe also that if :math:`F` and :math:`S` are not sufficiently large, one can end up with a smaller value of :math:`M` below ``sv_maxspeed``, which is bad as will be seen later.

In the FME, we also have the :math:`\mu` coefficient. This coefficient may be written as

.. math:: \mu =
   \begin{cases}
   \min(\gamma_1, \gamma_2) & \gamma_2 > 0 \\
   0 & \gamma_2 \le 0
   \end{cases}

where

.. math:: \gamma_1 = k_e \tau MA \quad\quad
   \gamma_2 = L - \lambda(\mathbf{v}) \cdot \mathbf{\hat{a}} = L - \lVert\lambda(\mathbf{v})\rVert \cos\theta

Recall that :math:`k_e` is the entity friction described in :ref:`player friction`. :math:`A` is the value of either ``sv_accelerate`` or ``sv_airaccelerate``, used for ground and air movement respectively. :math:`L` is either :math:`M` or :math:`\min(30, M)`, for ground and air movement respectively. :math:`\theta` is the shortest angle between :math:`\mathbf{v}` and :math:`\mathbf{\hat{a}}`.

We can observe that if :math:`\gamma_2 \le 0`, there will be no acceleration at all. This occurs when

.. math:: \cos\theta \ge \frac{L}{\lVert\lambda(\mathbf{v})\rVert}

Now observe that if :math:`\lVert\lambda(\mathbf{v})\rVert < L`, then this condition will never hold because the maximum value of :math:`\cos\theta` is :math:`1`. That is to say, at lower speeds, the player will be able to accelerate regardless of :math:`\theta` (barring a few zero points). With speeds beyond :math:`L`, acceleration will not occur with angles

.. math:: \lvert\theta\rvert \le \arccos \frac{L}{\lVert\lambda(\mathbf{v})\rVert}

This is just one of the consequences of the FME. Exploitations of this equation will be detailed in :ref:`strafing`.

Water movements
---------------

Waterjump
~~~~~~~~~
