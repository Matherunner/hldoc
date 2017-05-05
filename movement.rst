.. _player movement:

Player movement basics
======================

.. TODO: talk about edgebug, slopejump?, player specific friction, edgefriction, basevelocity, put down FMEs, onground stuff!

In this chapter, we will focus on the fundamental governing equations for the air and ground player movements, and the exploitation of some of the miscellaneous physical phenomena. This chapter also serves as a prerequisite to :ref:`strafing`.

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



Air and ground movements
------------------------

The physics governing the player's air and ground movements are of primary importance.

Water movements
---------------

Waterjump
~~~~~~~~~
