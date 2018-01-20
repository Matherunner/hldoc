Motion under gravity
====================

Motion under gravity, with or without strafing, is ubiquitous in Half-Life. In speedrunning, such questions are sometimes raised:

- Is it possible at all to clear that gap?
- What is the minimum long jump speed required to clear that gap?
- How much speed boost is needed to jump over that wall?
- How much speed boost is needed to clear that gap?
- At what angle should I toss the MP5 grenade to hit the target?

Here we will attempt to answer these questions, and provide formulae or algorithms to solve many of these common cases.

Preliminaries
-------------

We will restrict discussions to a vertical plane, where the horizontal and vertical axes are denoted as the :math:`x` and :math:`z` axes respectively. We will assume all bodies have initial position at the origin :math:`(x_0, z_0) = (0, 0)`.

Recall from classical kinematics that a particle under projectile motion (motion under the sole influence of gravity) with initial velocities :math:`v_{i,x}`, :math:`v_{i,z}`, and gravitational acceleration :math:`g` has final positions

.. math:: x_f = v_{i,x} t \qquad z_f = v_{i,z} t - \frac{1}{2} gt^2

In most of the discussions below, the equation for :math:`z` will remain unchanged, but the equation for :math:`x` will depend on whether strafing is done.

Recall from strafing physics that given initial velocity :math:`v_{i,x}` and strafing variables, the final horizontal speed and position after :math:`t` seconds of strafing is

.. math:: v_{f,x} = \sqrt{v_{i,x}^2 + tK} \qquad x_f = \frac{2}{3K} \left( \left( v_{i,x}^2 + tK \right)^{3/2} - v_{i,x}^3 \right)

Here, :math:`K` depends on the type of strafing. Possible values are :math:`K = MA(2L - \tau MA)` or :math:`K = L^2/\tau`.

Position and a velocity component
---------------------------------

In speedrunning situations, the final position is often given, and the goal would be to move from the current position, to the final position, subject to some constraints in one of the velocity components. For example, determining the minimum initial horizontal velocity needed to clear a gap by jumping and strafing alone (initial vertical velocity is known), or determining the minimum boost needed to reach a certain height (the final vertical velocity is zero).

Assuming initial and final positions :math:`(0, 0)` and :math:`(x_f, z_f)`, we may be given just one of the following:

.. math:: v_{i,x} \quad v_{i,z} \quad v_{f,x} \quad v_{f,z}

Knowing just one of these quantities is sufficient to solve the entire equation of motion in both axes.

Time constraint equation
~~~~~~~~~~~~~~~~~~~~~~~~

The time it takes to reach the final position must be the same for both :math:`x` and :math:`z` directions. In other words, the position in both directions must reach the final position simultaneously. Solving the time in the vertical equation of motion yields

.. math:: t_z = \frac{v_{i,z} \pm \sqrt{v_{i,z}^2 - 2gz_f}}{g}

If strafing is performed, the time it takes to reach the final horizontal position is found to be

.. math:: t_x = \frac{1}{K} \left( \left( v_{i,x}^3 + \frac{3}{2} Kx_f \right)^{2/3} - v_{i,x}^2 \right)

Then, :math:`t_z = t_x` must be satisfied for the body to reach the final position. This is the time constraint equation that will be used in later analyses.

Note also the maximum :math:`t_x` is achieved by having zero initial horizontal velocity, while keeping the other variables constant. This yields

.. math:: t_{x,\mathrm{max}} = \left. t_x \right\rvert_{v_{i,x} = 0} = K^{-1/3} \left( \frac{3}{2} x_f \right)^{2/3}

The purpose of this quantity will be illustrated later as well.

Given :math:`v_{i,x}`
~~~~~~~~~~~~~~~~~~~~~

With :math:`v_{i,x}` known, we can simply compute the horizontal time :math:`t_x`, and compute

.. math:: v_{i,z} = \frac{gt_x^2 + 2z_f}{2t_x}

The calculated initial vertical speed is guaranteed to reach the final position in the same time. However, the trajectory may take a different shape. That is, the path might either be strictly increasing or ends with a decreasing curve. To check this, we check the sign of the final vertical velocity. If the path is strictly increasing, we have

.. math::
   \begin{aligned}
   v_{f,z} = v_{i,z} - gt_x = \frac{gt_x^2 + 2z_f}{2t_x} - gt_x &\ge 0 \\
   \implies 2z_f &\ge gt_x^2
   \end{aligned}

Observe that if :math:`t_x` increases while all else kept constant, the inequality will eventually be violated, resulting in a inverted bell shaped path. In addition, if :math:`z_f < 0`, that is when the final position is below the starting position, then the inequality will always be violated regardless of :math:`t_x`.

Given :math:`v_{f,x}`
~~~~~~~~~~~~~~~~~~~~~

TODO TODO

Given :math:`v_{i,z}`
~~~~~~~~~~~~~~~~~~~~~

Firstly, the final height is reachable if :math:`v_{i,z}^2 \ge 2gz_f`, which ensures the square root in the :math:`t_z` equation give a real number. Notice that if :math:`z_f < 0` then this condition will always hold, which is intuitive.

This is where we will make use of the :math:`t_{x,\mathrm{max}}` described earlier. There are four different cases we need to handle. Namely, two from the the sign of the square root when computing :math:`t_z`, and two from the sign of :math:`t_{x,\mathrm{max}} - t_z`. In most cases, taking the negative square root is desirable as this minimises the time :math:`t_z`. However, the negative square root may lead to :math:`t_z < 0`, which must be rejected. The sign of :math:`t_{x,\mathrm{max}} - t_z` indicates the need to manually slow down the horizontal motion (by taking a longer curve or stop strafing altogether). Namely, :math:`t_{x,\mathrm{max}} < t_z` implies reaching the final :math:`x` position before reaching the final :math:`z` position. Therefore, the horizontal motion needs to be slowed, and no subsequent computation needs to be done. If :math:`t_{x,\mathrm{max}} > t_z`, then the horizontal speed is not sufficiently high, and therefore the initial horizontal velocity is nonzero and an additional step is needed to compute its value.

In the last case, we must solve for the initial horizontal velocity :math:`v_{i,x}` from the time constraint equation. The time constraints equation cannot be solved analytically with any ease, therefore a numerical solution should be computed using any root finding algorithm. For example, the Newton's method appears to work in many cases. For reference, the derivative of the time constraint equation needed for Newton's method is

.. math:: \frac{2}{K} v_{i,x} \left( v_{i,x} \left( v_{i,x}^3 + \frac{3}{2} Kx_f \right)^{-1/3} - 1 \right)

An alternative to the Newton's method, but still require a numerical solution, is to solve the quartic equation

.. math:: 3t_z v_{i,x}^4 - 3x_fv_{i,x}^3 + 3t_z^2Kv_{i,x}^2 + t_z^3K^2 - \frac{9}{4} x_f^2K = 0

using a standard polynomial solver. Typically, there are two complex roots that do not satisfy the time constraint equation, and a root that is negative.

Given :math:`v_{f,z}`
~~~~~~~~~~~~~~~~~~~~~

It is common to have the final vertical velocity given as well. For example, this gives the minimum required initial velocity to reach a the given height. Or, with :math:`v_{f,z} = 180` this gives the maximum initial velocity such that the player is barely onground when landing on some platform.

The approach to solving this problem is very similar to that when given the initial vertical velocity. The only difference is the equation for :math:`t_z`, which must be rewritten in terms of :math:`v_{f,z}`, giving

.. math:: t_z = \frac{v_{f,z} \pm \sqrt{v_{f,z}^2 + 2gz_f}}{g}
