.. _strafing:

Strafing
========

*Strafing* in the context of Half-Life speedrunning refers to the technique of pressing the correct movement keys (usually the WASD keys) and moving the mouse left and right in a precise way to increase the player speed beyond what the developers intended or make sharp turns without sacrificing too much speed. Strafing as a technique can be achieved similarly in the air and on the ground. If there is a need to distinguish between them, we refer to the former as "airstrafing" and the latter as "groundstrafing". Strafing is commonly accompanied by a series of jumps intended to keep the player off the ground, as there is friction when moving on the ground. For the purpose of our discussions, the sole act of jumping repeatedly like a rabbit, regardless of whether strafing is done concurrently, is *bunnyhopping*, although the reader will find some in the community who include airstrafing when the term "bunnyhopping" is used. In this chapter, we will only discuss strafing and not bunnyhopping.

While this chapter is not the first mathematical treatment of this topic, it is the goal of the author to write the definitive analysis and optimisation of strafing in a significantly greater level of precision and thoroughness than seen in other sources. This chapter shall serve as the starting point and baseline for further discussions and analysis of strafing-related techniques and physics. Other attempts at mathematical treatments of strafing like `this by injx`_, `this by flafla2`_, `this by Kared13`_, `this by ZdrytchX`_, `this by jrsala`_, and `this by Matt's Ramblings`_, are ad-hoc and suffer from flaws that make them less suited for further analyses (e.g. surfing analysis, speed-preserving strafing, curvature analysis, minimal-time paths), gaining a deeper understanding of strafing, or indeed for practical implementations.

.. _`this by injx`: https://web.archive.org/web/20190428135531/http://www.funender.com/quake/articles/strafing_theory.html
.. _`this by flafla2`: http://flafla2.github.io/2015/02/14/bunnyhop.html
.. _`this by Kared13`: https://steamcommunity.com/sharedfiles/filedetails/?id=184184420
.. _`this by ZdrytchX`: https://sites.google.com/site/zdrytchx/how-to/strafe-jumping-physics-the-real-mathematics
.. _`this by jrsala`: https://gamedev.stackexchange.com/a/45656
.. _`this by Matt's Ramblings`: https://youtu.be/rTsXO6Zicls

Strafing is so fundamental to speedrunning, that a speedrunner ought to "get it out of the way" while focusing on other techniques. Strafing should be viewed as a building block that is used as a basis for other speedrunning techniques and tricks. If we do not cannot perform strafing near optimally, the entire speedrun falls apart. This applies to TASes as well: we want to optimise strafing as much as possible so that we can "forget about it" when constructing a TAS and permitting us to concentrate on the planning, the "general picture", and executing specific tricks.

.. tip:: Be sure to familiarise yourself with the fundamentals of player movement described in :ref:`player movement`. Without the prerequisite knowledge, this chapter can be hard to follow.

Basic intuition
---------------

Before delving into the mathematics, it may be helpful to have a geometric intuition of how strafing works. In Half-Life, and indeed in real-life classical mechanics, the velocity and acceleration are defined as Euclidean vectors with a length (or magnitude) and a direction, typically drawn as an arrow in the Euclidean space. In the strafing context, we are only interested in vectors drawn on a 2D space. When a body in Half-Life accelerates in a frame, the acceleration vector, scaled by frame time, is added to the velocity vector to obtain a new velocity vector,

.. math:: \mathbf{v}' = \mathbf{v} + \tau\mathbf{a}

This may be interpreted geometrically as putting the acceleration arrow after the velocity arrow to obtain a new velocity arrow. The diagram looks like a triangle, as seen in :numref:`strafing intuition 1`. Now, notice that the new velocity arrow is *longer* than the previous velocity arrow. This means that the *speed* (represented by the arrow length) has been increased.

.. figure:: images/strafing-intuition-1.png
   :name: strafing intuition 1
   :scale: 50%

   Depiction of how strafing increases speed (i.e. the length of the velocity
   vector). On the left, the directions of the vectors have significance. On the
   right, we have rotated the vectors to that they line up, but therefore do not
   point to the correct direction (though having the correct length or
   magnitude).

In Half-Life physics, the magnitude or length of the acceleration vector :math:`\mathbf{a}` depends on the current speed and the angle between the velocity and itself, which in turn is controlled by the viewangles, as explained in :ref:`player air ground`. The task of finding the optimal angles to achieve a certain goal is the topic of this chapter.

.. _strafe building blocks:

Building blocks
---------------

Regardless of the objective of strafing, its physics is governed by the fundamental movement equation (FME). We will construct several few mathematical building blocks to aid further analyses. Firstly, write :math:`\lVert\mathbf{v}'\rVert = \sqrt{\mathbf{v}' \cdot \mathbf{v}'}`, where :math:`\mathbf{v}'` is already given in :ref:`player air ground`. Expanding each :math:`\mathbf{v}'` yields

.. math:: \lVert\mathbf{v}'\rVert
   = \sqrt{(\lambda(\mathbf{v}) + \mu\mathbf{\hat{a}}) \cdot (\lambda(\mathbf{v}) + \mu\mathbf{\hat{a}})}
   = \sqrt{\lVert\lambda(\mathbf{v})\rVert^2 + \mu^2 + 2 \lVert\lambda(\mathbf{v})\rVert \mu \cos\theta}
   :label: nextspeed

This can be done because the dot product satisfies the distributive law. Very quickly, we obtained :eq:`nextspeed` which is sometimes called the *scalar FME*, often used in practical applications as the most general way to compute new *speeds* (as opposed to velocity vectors) given :math:`\theta`.

.. tip:: This is a very common and useful trick that can be used to quickly
         yield an expression for the magnitude of vectorial outputs without
         explicit vectorial computations or geometric analyses. Half-Life
         physicists ought to learn this technique well.

From equation :eq:`nextspeed`, we can further write down the equations by assuming :math:`\mu = \gamma_1` and :math:`\mu = \gamma_2` respectively, to eliminate :math:`\mu`. These new equations can be found by expanding :math:`\mu`, again already given previously. We get

.. math::
   \begin{aligned}
   \lVert\mathbf{v}'_{\mu = \gamma_1}\rVert &= \sqrt{\lVert\lambda(\mathbf{v})\rVert^2 +
   k_e \tau MA \left( k_e \tau MA + 2 \lVert\lambda(\mathbf{v})\rVert \cos\theta \right)} \\
   \lVert\mathbf{v}'_{\mu = \gamma_2}\rVert &= \sqrt{\lVert\lambda(\mathbf{v})\rVert^2 \sin^2 \theta + L^2}
   \end{aligned}
   :label: nextspeed gammas

Note that when :math:`\gamma_1 = \gamma_2`, we have :math:`\lVert\mathbf{v}'_{\mu=\gamma_1}\rVert = \lVert\mathbf{v}'_{\mu=\gamma_2}\rVert`. Define :math:`\zeta` such that

.. math:: \cos\zeta = \frac{L - k_e\tau MA}{\lVert\lambda(\mathbf{v})\rVert}

Assuming :math:`\gamma_2 \ge 0`, then if :math:`\cos\theta \le \cos\zeta`, we have :math:`\mu = \gamma_1`. If :math:`\cos\theta \ge \cos\zeta`, then :math:`\mu = \gamma_2`. Define also :math:`\bar{\zeta}` such that :math:`\gamma_2 < 0` and therefore :math:`\mu = 0`, as

.. math:: \cos\bar{\zeta} = \frac{L}{\lVert\lambda(\mathbf{v})\rVert}

.. note:: Note that we permit :math:`\lvert\cos\zeta\rvert > 1` and :math:`\lvert\cos\bar{\zeta}\rvert > 1`, but restricts :math:`\lvert\cos\theta\rvert \le 1`. We never need to invert the cosines to obtain :math:`\zeta` and :math:`\bar{\zeta}` in theoretical and practical computations when their absolute values are greater than 1. However, had we really done it, :math:`\zeta` and :math:`\bar{\zeta}` would have imaginary parts.

Putting these together, we can write the :math:`\mu` more explicitly as a piecewise-defined function

.. math::
   \mu =
   \begin{cases}
   0 & \cos\theta \ge \cos\bar{\zeta} \\
   \gamma_2 & \cos\theta < \cos\bar{\zeta} \land \cos\theta \ge \cos\zeta \\
   \gamma_1 & \cos\theta < \cos\bar{\zeta} \land \cos\theta \le \cos\zeta
   \end{cases}
   :label: piecewise mu

The new speed :math:`\lVert\mathbf{v}'\rVert` can also be correspondingly written as a piecewise-defined function by substituting :math:`\mu` with :eq:`piecewise mu`. These equations will be important in the exploitative analyses of the FME shortly.

However, computing speeds is sometimes not sufficient. We sometimes want to also compute velocity *vectors* endowed with both directionality and magnitude, but without worrying about player viewangles and :math:`\mathbf{\hat{a}}`. We can achieve this by parametrising :math:`\mathbf{\hat{a}}` in terms of a rotation of :math:`\mathbf{\hat{v}}` by an angle of :math:`\theta`. This may be expressed as

.. math:: \mathbf{\hat{a}} = \mathbf{\hat{v}} R_z(\theta)

This is a matrix multiplication of :math:`\mathbf{\hat{v}}` by a rotation matrix. The benefit of writing the FME in this form is that we no longer need to worry about calculating :math:`\mathbf{\hat{f}}` and :math:`\mathbf{\hat{s}}`, which, recalling from :ref:`view vectors`, depend on the yaw angle :math:`\vartheta` in the 2D case. We also no longer need to worry about :math:`F`, :math:`S`, and :math:`M` needed to compute :math:`\mathbf{\hat{a}}`. All we need to know is the angle :math:`\theta` between velocity and acceleration vectors. This can make efficient computations easier as well, because the angle :math:`\theta` is easily computed (as we will see shortly) in just a few lines of code.

.. caution:: Remember from :ref:`notations` that vectors in this documentation are *row vectors*. Therefore, the order of multiplication is different from those in standard linear algebra textbooks. In fact, the components in :math:`R_z(\theta)` are also ordered differently.

With this idea in mind, we can rewrite the FME as

.. math:: \mathbf{v}' = \lambda(\mathbf{v}) + \mu\mathbf{\hat{v}}
   \begin{bmatrix}
   \cos\theta & -\sin\theta \\
   \sin\theta & \cos\theta
   \end{bmatrix}
   \quad\quad (\mathbf{v} \ne \mathbf{0})
   :label: newvelmat

Note that the precaution :math:`\mathbf{v} \ne \mathbf{0}` is needed so that the unit vector :math:`\mathbf{\hat{v}} = \mathbf{v} / \lVert\mathbf{v}\rVert` is well defined. In other words, the directionality of :math:`\mathbf{v}` is lost when it is zero. This is therefore one downside of parametrising in terms of :math:`\theta`, where the special case of zero velocity must be handled separately by replacing :math:`\mathbf{\hat{v}} = \mathbf{\hat{f}}` (and assuming :math:`\varphi = 0` as usual) in :eq:`newvelmat`, thereby involving the viewangles in the computations.

When written in the form of :eq:`newvelmat`, positive :math:`\theta` gives *clockwise* rotations, while negative :math:`\theta` gives *anticlockwise* rotations. If this convention is inconvenient for a particular application, one can easily reverse the directionality by reversing the signs of the :math:`\sin\theta` elements in the rotation matrix.

.. _maxaccel:

Maximum acceleration
--------------------

Airstrafing to continuously gain speed beyond what the developers intended is one of the oldest speedrunning tricks. It is of no surprise that one of the earliest inquiries into Half-Life physics is related to the question of how to airstrafe with the maximum acceleration, when research began circa 2012 by the author of this documentation. In this section, we will provide precise mathematical descriptions of how maximum-acceleration strafing works in a way that will provide a baseline for further analyses and also can readily be implemented in TAS tools.

We must define our metric for "maximum acceleration" in a mathematically precise way. Specifically, we want to maximise the *average scalar acceleration* over some period of time :math:`t`. The average scalar acceleration may in turn be defined as

.. math:: \overline{\lVert\mathbf{a}\rVert} = \frac{\Delta\lVert\mathbf{v}\rVert}{t} = \frac{\lVert\mathbf{v}_t\rVert - \lVert\mathbf{v}_0\rVert}{t}

where :math:`\lVert\mathbf{v}_t\rVert` is the speed at time :math:`t` and :math:`\lVert\mathbf{v}_0\rVert` is the initial speed. We believe this is a valid metric because it reflects the intention of the speedrunner better in the field: namely, to increase the speed as much as possible over some time, which automatically also increases the distance travelled within the same period of time, since the distance travelled is simply the sum of all the speeds in every frame within the period of time in question.

Arguments of the maxima
~~~~~~~~~~~~~~~~~~~~~~~

Let :math:`\mathbf{v}` be the current player velocity, :math:`\mathbf{v}'` the velocity after strafing, and :math:`\tau_g` the game frame time (see :ref:`frame rate`). To maximise the average scalar acceleration, it is sufficient to maximise the per-frame scalar acceleration

.. math:: \frac{\lVert\mathbf{v}'\rVert - \lVert\mathbf{v}\rVert}{\tau_g}

It turns out that maximising the per-frame acceleration "greedily" also maximises the global average acceleration over the span of some time :math:`t`. In other words, optimising only the individual frames result in the optimal "overall" acceleration as well. This is perhaps owing to good luck, because it is by no means a universal rule that local maxima yield a global maximum in other instances. We will prove this assertion in a later section.

Now, we will assume :math:`\lVert\mathbf{v}\rVert` and :math:`\tau_g` are independent of any other variables. Therefore, we can ignore them, and the task of maximising acceleration boils down to maximising solely the new speed :math:`\lVert\mathbf{v}'\rVert`. Looking at :eq:`nextspeed gammas`, observe that the new speed is invariant to the transformation :math:`\theta \mapsto -\theta`, because both :math:`\cos\theta` and :math:`\sin^2\theta` are `even functions`_. Without loss of generality, we will consider only :math:`0 \le \theta \le \pi`.

.. _`even functions`: https://en.wikipedia.org/wiki/Even_and_odd_functions

Before we search for the global optimum, we must understand the behaviours of the piecewise :math:`\lVert\mathbf{v}'\rVert`. Observe that the maximum of :math:`\lVert\mathbf{v}'_{\mu=\gamma_2}\rVert` occurs at :math:`\sin\theta = 1` or :math:`\cos\theta = 0`, if we consider the entire domain of :math:`-1 \le \cos\theta \le 1`, or

.. math:: \underset{\cos\theta}{\operatorname{argmax}} \lVert\mathbf{v}'_{\mu=\gamma_2}\rVert = 0

In addition, we also see that :math:`\lVert\mathbf{v}'_{\mu=\gamma_2}\rVert` is strictly increasing in :math:`-1 \le \cos\theta \le 0` and strictly decreasing in :math:`0 \le \cos\theta \le 1`. Indeed, the plot for :math:`\lVert\mathbf{v}'_{\mu=\gamma_2}\rVert` against :math:`\cos\theta` forms a semi-ellipse except in degenerate cases.

.. TODO: maybe plot a graph for this?

On the other hand, the maximum of :math:`\lVert\mathbf{v}'_{\mu=\gamma_1}\rVert`, however, depends on the sign of :math:`k_e\tau MA`. The symbols here have already been defined in :ref:`player air ground`.

.. math:: \underset{\cos\theta}{\operatorname{argmax}} \lVert\mathbf{v}'_{\mu=\gamma_1}\rVert =
   \begin{cases}
   1 & k_e\tau MA > 0 \\
   -1 & k_e\tau MA < 0 \\
   [-1, 1] & k_e\tau MA = 0
   \end{cases}

If :math:`k_e\tau MA > 0`, then :math:`\lVert\mathbf{v}'_{\mu=\gamma_1}\rVert` is strictly increasing. If :math:`k_e\tau MA < 0`, then :math:`\lVert\mathbf{v}'_{\mu=\gamma_1}\rVert` is strictly decreasing.

The relative sizes of :math:`\{ 0, \cos\zeta, \cos\bar{\zeta} \}` can vary in various ways, and there are in total :math:`3! = 6` permutations we must consider in order to study the behaviour of the new speed :math:`\lVert\mathbf{v}'\rVert` and therefore the maximum point.

.. FIXME: need to go through these to think about the edge cases at -1, 1, cos\bar\zeta etc

:math:`0 \le \cos\zeta \le \cos\bar{\zeta}`
   If and only if :math:`L - k_e\tau MA \ge 0`, :math:`L \ge 0`, and :math:`k_e\tau MA \ge 0`. In :math:`-1 \le \cos\theta \le \cos\zeta`, :math:`\lVert\mathbf{v}'\rVert = \lVert\mathbf{v}'_{\mu=\gamma_1}\rVert` is strictly increasing with a maximum point at :math:`\cos\theta = \cos\zeta`. In :math:`\cos\zeta \le \cos\theta \le \cos\bar{\zeta}`, :math:`\lVert\mathbf{v}'\rVert = \lVert\mathbf{v}'_{\mu=\gamma_2}\rVert` is strictly decreasing. However, if :math:`\cos\zeta > 1`, then :math:`\mu = \gamma_1` for the entire range. We conclude that

   .. math:: \underset{\cos\theta}{\operatorname{argmax}} \lVert\mathbf{v}'\rVert = \min(1, \cos\zeta), \quad \mu = \gamma_1

:math:`0 \le \cos\bar{\zeta} \le \cos\zeta`
   If and only if :math:`L - k_e\tau MA \ge 0`, :math:`L \ge 0`, and :math:`k_e\tau MA \le 0`. In :math:`-1 \le \cos\theta \le \cos\bar{\zeta}`, :math:`\lVert\mathbf{v}'\rVert = \lVert\mathbf{v}'_{\mu=\gamma_1}\rVert` is strictly decreasing with a maximum point at :math:`\cos\theta = -1`. In :math:`\cos\bar{\zeta} \le \cos\theta \le \cos\zeta`, :math:`\lVert\mathbf{v}'\rVert = \lVert\lambda(\mathbf{v})\rVert`. Therefore, we always have

   .. math:: \underset{\cos\theta}{\operatorname{argmax}} \lVert\mathbf{v}'\rVert = -1, \quad \mu = \gamma_1

:math:`\cos\zeta \le 0 \le \cos\bar{\zeta}`
   If and only if :math:`L - k_e\tau MA \le 0`, :math:`L \ge 0`, and :math:`k_e\tau MA \ge 0`. In :math:`-1 \le \cos\theta \le \cos\zeta`, :math:`\lVert\mathbf{v}'\rVert = \lVert\mathbf{v}'_{\mu=\gamma_1}\rVert` is strictly increasing. In :math:`\cos\zeta \le \cos\theta \le \cos\bar{\zeta}`, the maximum occurs at :math:`\cos\zeta = 0`. This implies

   .. math:: \underset{\cos\theta}{\operatorname{argmax}} \lVert\mathbf{v}'\rVert = 0, \quad \mu = \gamma_2

:math:`\cos\bar{\zeta} \le 0 \le \cos\zeta`
   If and only if :math:`L - k_e\tau MA \ge 0`, :math:`L \le 0`, and :math:`k_e\tau MA \le 0`. In :math:`-1 \le \cos\theta \le \cos\bar{\zeta} \le \cos\zeta`, we have :math:`\lVert\mathbf{v}'\rVert = \lVert\mathbf{v}'_{\mu=\gamma_1}\rVert`, which is strictly decreasing because :math:`k_e\tau MA \le 0`. Therefore, the maximum point is at

   .. math:: \underset{\cos\theta}{\operatorname{argmax}} \lVert\mathbf{v}'\rVert =
      \begin{cases}
      -1 & \cos\bar{\zeta} > -1 \\
      [-1, 1] & \cos\bar{\zeta} \le -1
      \end{cases} \qquad \mu = \gamma_1

:math:`\cos\zeta \le \cos\bar{\zeta} \le 0`
   If and only if :math:`L - k_e\tau MA \le 0`, :math:`L \le 0`, and :math:`k_e\tau MA \ge 0`. In :math:`-1 \le \cos\theta \le \cos\zeta`, :math:`\lVert\mathbf{v}'\rVert = \lVert\mathbf{v}'_{\mu=\gamma_1}\rVert` is strictly increasing. In :math:`\cos\zeta \le \cos\theta \le \cos\bar{\zeta} \le 0`, :math:`\lVert\mathbf{v}'\rVert = \lVert\mathbf{v}_{\mu=\gamma_2}\rVert` is also strictly increasing. But since :math:`\lVert\mathbf{v}'_{\mu=\gamma_2}\rVert = 0` at :math:`\cos\theta = \cos\bar{\zeta}`, we conclude that

   .. math:: \underset{\cos\theta}{\operatorname{argmax}} \lVert\mathbf{v}'\rVert = [\max(-1, \cos\bar{\zeta}), 1], \quad \mu = 0

   As we will see later, this case actually yields :math:`\lVert\mathbf{v}'\rVert = \lVert\mathbf{v}\rVert`, which is useless. But we will include this case for the sake of completeness.

:math:`\cos\bar{\zeta} \le \cos\zeta \le 0`
   If and only if :Math:`L - k_e\tau MA \le 0`, :math:`L \le 0`, :math:`k_e\tau MA \le 0`. The rest of the analysis and the result are exactly the same as that in the :math:`\cos\bar{\zeta} \le 0 \le \cos\zeta` case.

Given the case-by-case study of these six permutations, we can summarise that the maximum point of :math:`\lVert\mathbf{v}'\rVert` occurs at

.. math::
   \begin{aligned}
   & \cos\theta = \cos\Theta \in
   \underset{\cos\theta}{\operatorname{argmax}} \lVert\mathbf{v}'\rVert \\
   &=
   \begin{cases}
   \min(1, \cos\zeta) & k_e\tau MA \ge 0 \land L - k_e\tau MA \ge 0 \land L \ge 0 \\
   0 & k_e\tau MA \ge 0 \land L - k_e\tau MA \le 0 \land L \ge 0 \\
   [\max(-1, \cos\bar{\zeta}), 1] & k_e\tau MA \ge 0 \land L - k_e\tau MA \le 0 \land L \le 0 \\
   [-1, 1] & k_e\tau MA \le 0 \land \cos\bar{\zeta} \le -1 \\
   -1 & k_e\tau MA \le 0 \land \cos\bar{\zeta} > -1
   \end{cases}
   \end{aligned}
   :label: maxaccel theta

To implement :eq:`maxaccel theta`, care must be taken when computing :math:`\cos\zeta` and :math:`\cos\bar{\zeta}`. This is because when :math:`\lVert\lambda(\mathbf{v})\rVert = 0`, we have :math:`\cos\zeta = \pm\infty` and :math:`\cos\bar{\zeta} = \pm\infty`.

Optimality
~~~~~~~~~~

We show that the angles given in :eq:`maxaccel theta` actually gives the highest average acceleration over some time :math:`t`, more than just the maximum speed after one frame of strafing. After one frame of strafing, the average acceleration is given by

.. math:: \frac{\lVert\mathbf{v}_1\rVert - \lVert\mathbf{v}_0\rVert}{\tau_g}

Since the only variable is :math:`\lVert\mathbf{v}_1\rVert`, clearly the angles in :eq:`maxaccel theta` maximises the acceleration. Now suppose the player has strafed for
some time :math:`t` at a *maximum* average acceleration possible :math:`\bar{a}` so that the final speed is some :math:`\lVert\mathbf{v}_n\rVert = \bar{a} t`, and it is required to strafe another frame. The new average acceleration after another frame is then

.. math:: \frac{\lVert\mathbf{v}_{n+1}\rVert - \lVert\mathbf{v}_0\rVert}{t + \tau_g}

where :math:`\lVert\mathbf{v}_{n+1}\rVert` is given by the FME with :math:`\lVert\mathbf{v}_n\rVert` as the starting speed. Since the only variable is again :math:`\lVert\mathbf{v}_{n+1}\rVert`, clearly :eq:`maxaccel theta` gives the maximum :math:`\lVert\mathbf{v}_{n+1}\rVert`. We conclude by induction that :eq:`maxaccel theta` gives the maximum average acceleration over some time :math:`t`.

On top of that, we also show that :eq:`maxaccel theta` gives the highest average *speed* over some time :math:`t`. In other words, it admits the shortest time possible to travel any distance :math:`d`. Given an initial speed of :math:`\lVert\mathbf{v}_0\rVert`, the average speed after one frame of strafing is

.. math:: \frac{\lVert\mathbf{v}_1\rVert \tau}{\tau_g}

Clearly :eq:`maxaccel theta` gives the maximum average speed because :math:`\lVert\mathbf{v}_1\rVert` is the only variable. Now, suppose the player has strafed for some time :math:`t` at the maximum possible average speed :math:`\bar{v}` with some final speed :math:`\lVert\mathbf{v}_n\rVert`. After another frame of strafing, the new average speed is

.. math:: \frac{\bar{v} t + \lVert\mathbf{v}_{n+1}\rVert \tau}{t + \tau_g}

where :math:`\lVert\mathbf{v}_{n+1}\rVert` is given by the FME with :math:`\lVert\mathbf{v}_n\rVert` as the starting speed and is the only variable. Again, the angles given by :eq:`maxaccel theta` maximises :math:`\lVert\mathbf{v}_{n+1}\rVert`.

Speed equations
~~~~~~~~~~~~~~~

Using :eq:`maxaccel theta` we obtain the optimal :math:`\cos\theta` under various situations. We can proceed to eliminate :math:`\theta` and :math:`\mu` from :eq:`nextspeed` to obtain a clean formulae for speed after one frame. Further, we can also obtain formulae for the speed after :math:`n` frames, assuming all the movement variables are held constant.

.. math:: \lVert\mathbf{v}'\rVert =
          \begin{cases}
          \sqrt{\lVert\lambda(\mathbf{v})\rVert^2 + k_e \tau MA \left(2L - k_e \tau MA\right)} & \text{case 1} \land \cos\Theta = \cos\zeta \\
          \lVert\lambda(\mathbf{v})\rVert + k_e\tau MA & \text{case 1} \land \cos\Theta = 1 \\
          \sqrt{\lVert\lambda(\mathbf{v})\rVert^2 + L^2} & \text{case 2} \\
          \lVert\lambda(\mathbf{v})\rVert & \text{case 3 & 4} \\
          \lVert\lambda(\mathbf{v})\rVert - k_e \tau MA & \text{case 5}
          \end{cases}
   :label: maxaccel speed

For airstrafing where there is no friction (namely :math:`\lambda(\mathbf{v}) = \mathbf{v}`), we can solve the recurrence relations easily and obtain formulae for the speed after :math:`n` frames of strafing as follows:

.. math:: \lVert\mathbf{v}_n\rVert =
          \begin{cases}
          \sqrt{\lVert\mathbf{v}_0\rVert^2 + nk_e \tau MA \left(2L - k_e \tau MA\right)} & \text{case 1} \land \cos\Theta = \cos\zeta \\
          \lVert\mathbf{v}_0\rVert + nk_e\tau MA & \text{case 1} \land \cos\Theta = 1 \\
          \sqrt{\lVert\mathbf{v}_0\rVert^2 + nL^2} & \text{case 2} \\
          \lVert\mathbf{v}_0\rVert & \text{case 3 & 4} \\
          \lVert\mathbf{v}_0\rVert - nk_e \tau MA & \text{case 5}
          \end{cases}
   :label: air maxaccel speed

These equations can be quite useful in planning.  For example, to calculate the number of frames required to airstrafe from :math:`320` ups to :math:`1000` ups at default Half-Life settings and 1000 fps, we solve

.. math:: 1000^2 = 320^2 + n \cdot 0.001 \cdot 320 \cdot 10 \cdot (60 - 0.001 \cdot 320 \cdot 10)
          \implies n \approx 4938

In addition, under airstrafing again, we can integrate the speed equations to obtain distance-time equations. Before doing this, we must make a change of variables by assuming continuous time and writing :math:`t = n\tau`. Then we compute

.. math:: d_t = \int_0^{t} \lVert\mathbf{v}_{t'}\rVert \; dt'

for each case.

For groundstrafing, however, the presence of friction means simple substitutions may not work. In more complex cases, it may be desirable to simply calculate the speeds frame by frame using the scalar FME.

Effects of frame rate
~~~~~~~~~~~~~~~~~~~~~

The frame rate can affect the acceleration significantly. Looking at the second case of :eq:`maxaccel theta`, the acceleration per frame is

.. math:: \frac{\sqrt{\lVert\lambda(\mathbf{v})\rVert^2 + L^2} - \lVert\lambda(\mathbf{v})\rVert}{\tau_g}

One can immediately see that the lower the :math:`\tau_g` (that is, the higher the game frame rate), the higher the acceleration. The first case of :eq:`maxaccel theta` and :math:`\cos\Theta = \cos\zeta` also provides greater accelerations at greater game frame rates. The other cases, however, do not admit greater accelerations at higher frame rates.

.. FIXME: similar to the frame rate section, this is misleading because it implies newer engines do not round tau_p.

When :math:`\eta \ne 1`
+++++++++++++++++++++++

Recall in :ref:`frame rate` that, on older game engines, the player frame rate :math:`\tau_p` is the game frame rate rounded towards zero to the nearest 0.001. This is not normally a problem, because speedruns are often run at frame rates such that :math:`\tau_p = \tau_g`, thus eliminating any slowdown. However, at the time of writing (July 2020), there exists an area of contention regarding the WON version of Blue Shift, where the default frame rate is 72 fps and some community rules forbid raising it further via console commands. Clearly, the slowdown factor at 72 fps is less than 1. There is a question of whether it is optimal to

1. use a lower :math:`\tau_g` such that :math:`\tau_p = \tau_g` (which would be :math:`\tau_g = 0.014` or :math:`f_g \approx 71.43` in the WON Blue Shift case), or
2. use :math:`\tau_g = 1/72` and :math:`\tau_p = 0.013` in some of the frames and switch to :math:`\tau_p = \tau_g = 0.014` in other frames

We claim that it is better to always lower :math:`\tau_g` such that :math:`\tau_p = \tau_g` and :math:`\eta = 1`. Precisely, we claim that the *average speed* over some real time :math:`t` is maximised when :math:`\eta = 1` throughout time :math:`t`. To see why, recall that the average speed is simply the total distance travelled divided by the time taken. The average speed in the first frame is

.. math:: V_1 = \frac{\tau_{p,1} \sqrt{\lVert\mathbf{v}_0\rVert^2 + K^2}}{\tau_{g,1}} = \eta_1 \sqrt{\lVert\mathbf{v}_0\rVert^2 + K^2}

Immediately, we can see that to maximise the average speed, we must have :math:`\tau_{p,1} = \tau_{g,1}` so that :math:`\eta = 1` is as big as possible. Now suppose the player has already travelled for some distance at a *maximum* average speed :math:`V_n`, taking some real time :math:`t`. We need to strafe another frame. The new average speed is then given by

.. math:: V_{n+1} = \frac{tV_n + \tau_{p,n+1} \lVert\mathbf{v}_{n+1}\rVert}{t + \tau_{g,n+1}}

Recall that :math:`\tau_{p,n+1} = 1000^{-1} \left\lfloor 1000 \tau_{g,n+1} \right\rfloor`. Write :math:`\tau_{g,n+1} = \tau_{p,n+1} + \epsilon` for some :math:`0 \le \epsilon < 0.001`. Eliminating :math:`\tau_{g,n+1}`, the new average speed may be rewritten as

.. math:: V_{n+1} = \frac{tV_n + \tau_{p,n+1} \lVert\mathbf{v}_{n+1}\rVert}{t + \tau_{p,n+1} + \epsilon}

Observe that to maximise :math:`V_{n+1}`, we must have :math:`\epsilon = 0` which implies :math:`\tau_{g,n+1} = \tau_{p,n+1}`. By induction, we have proved our claim stated earlier.

Effects of friction
~~~~~~~~~~~~~~~~~~~

There is a limit to the speed achievable by maximum-acceleration groundstrafing alone. There will be a critical speed such that the increase in speed exactly cancels the friction, so that :math:`\lVert\mathbf{v}_{k + 1}\rVert = \lVert\mathbf{v}_k\rVert`, namely the speed reaches a steady state. For the common example of default game settings, suppose the :math:`\cos\Theta = \cos\zeta` (the first case of :eq:`maxaccel speed`), :math:`L = M` (see :ref:`player air ground`), and geometric friction (see :ref:`player friction`) is at play. Then we may write

.. math:: \lVert\mathbf{v}\rVert^2 = (1 - \tau k)^2 \lVert\mathbf{v}\rVert^2 + k_e \tau M^2 A (2 - k_e \tau A)

Solving for :math:`\lVert\mathbf{v}\rVert`, we obtain the maximum groundstrafe speed for this particular configuration, keeping in mind that :math:`k` is dependent on :math:`k_e`:

.. math:: M \sqrt{\frac{k_e A (2 - \tau k_e A)}{k (2 - \tau k)}}

Take the case of default Half-Life settings at 1000 fps, we calculate

.. math:: 320 \sqrt{\frac{1 \cdot 10 \cdot (2 - 0.001 \cdot 1 \cdot 10)}{4 \cdot (2 - 0.001 \cdot 4)}} \approx 505.2

This is then the absolute maximum speed achievable by groundstrafing alone in vanilla Half-Life. At another common frame rate of 100 fps, we instead obtain the steady state speed of :math:`\approx 498.2`. There is nothing we can do to groundstrafe beyond this speed!

Interestingly, when there is edge friction, the game sets :math:`k = 8` with the default settings, and the maximum groundstrafe speed is drastically reduced to :math:`\approx 357.6`, which is indeed devastating as previously claimed in :ref:`edgefriction`, because it is not significantly more than the normal running speed of 320.

We also see that when the entity friction :math:`k_e` is less than 1, the effect on the maximum groundstrafe speed is very small. For instance, if :math:`k_e = 0.5`, then :math:`k = 2`. This yields the maximum groundstrafe speed of :math:`\approx 505.6`, barely larger than the normal groundstrafe speed.

Traditionally, jumping is done repeatedly to lift off from the ground to avoid the effects of ground friction. However, the presence of the bunnyhop cap (see :ref:`bunnyhop cap`) compels speedrunners to opt for ducktapping (see :ref:`ducktapping`) instead. Ducktapping has a downside of requiring one frame of ground contact, which introduces one frame of friction. The effect of this one frame of friction can be completely eliminated by setting the frame rate to an extremely high value in that frame alone, which forces :math:`\tau_p = 0` while the player is on the ground. If this is not possible, or forbidden, then the one frame of friction is unavoidable.

It turns out that the single frame of ground friction can be devastating, especially in lower frame rates. In fact, under most circumstances and combinations of movement variables, there exists a fixed point or steady state speed which acts as a limit to the speed a player can maintain indefinitely using only ducktapping and strafing alone. Let :math:`\lVert\mathbf{v}\rVert_S` be this steady state speed. Let :math:`\operatorname{MaxAccel}(\text{type}, v_0, n)` be a function that gives the speed after :math:`n` frames of maximum-acceleration strafing from an initial speed of :math:`v_0`. Denote :math:`T_D` the ducktap "period", or the time the player spends in the air after a ducktap. Define functions

.. math::
   \begin{aligned}
   V_A(v_0) &:= \operatorname{MaxAccel}(\text{air}, v_0, T_D \tau^{-1}) \\
   V_G(v_0) &:= \operatorname{MaxAccel}(\text{ground}, \lambda(V_A(v_0)), 1)
   \end{aligned}

Then :math:`V_G` gives the speed when the player lands on the ground after a ducktap and airstrafing. In general, to find the steady state speed :math:`\lVert\mathbf{v}\rVert_S`, we solve the equation

.. math:: V_G(\lVert\mathbf{v}\rVert_S) = \lVert\mathbf{v}\rVert_S
   :label: ducktap steady state

To give some concrete examples, consider ducktapping and strafing in a typical 1000 fps TAS with default Half-Life settings. Assuming :math:`\lVert\mathbf{v}\rVert_S > E` so that the geometric friction is in effect. Then :eq:`ducktap steady state` can be rewritten using :eq:`maxaccel speed` and :eq:`general friction` as

.. math:: \sqrt{\left( \lVert\mathbf{v}\rVert_S^2 + T_D C_A \right) \left(1 - k \tau\right)^2 + C_G} = \lVert\mathbf{v}\rVert_S

where

.. math:: C_A = k_e MA_A \left( 60 - k_e\tau MA_A \right), \quad C_G = k_e\tau M^2 A_G \left( 2 - k_e\tau A_G\right)

Assuming :math:`T_D = 0.2`, we obtain :math:`\lVert\mathbf{v}\rVert_S \approx 2184`. This implies that the player is able to maintain at least the default ``sv_maxvelocity`` at 1000 fps by ducktapping and strafing. Consider, however, ducktapping and strafing at 100 fps, which is a restriction some in the community are in favour of imposing. Here, :eq:`ducktap steady state` may instead be rewritten as

.. math:: \sqrt{\left( \lVert\mathbf{v}\rVert_S^2 + T_D \tau^{-1} 900 \right) \left(1 - k \tau\right)^2 + C_G} = \lVert\mathbf{v}\rVert_S

With :math:`\tau = 0.01` and solving, we instead obtain :math:`\lVert\mathbf{v}\rVert_S \approx 678`, which is substantially lower than that at 1000 fps.

.. _maxaccel growth:

Growth of speed
~~~~~~~~~~~~~~~

By obtaining :eq:`air maxaccel speed`, we can immediately make a few important observations. In the absence of friction and if :math:`\lvert\cos\Theta\rvert \ne 1`, the speed over time grows sublinearly, or :math:`O(\sqrt{n})`. This implies that the acceleration gradually decreases over time, but never reaches zero. It is notable that the acceleration at lower speeds can be substantial (more than linear acceleration) compared to that at higher speeds. To see why, write new speed :math:`v_t = \sqrt{v_0^2 + tK}`, then taking the derivative with respective to :math:`t` to obtain acceleration, yielding

.. math:: a_t = \frac{dv_t}{dt} = \frac{K}{2 \sqrt{v_0^2 + tK}}

for some :math:`K`. Now observe that, at :math:`t = 0`, the acceleration :math:`a_t \to \infty` as initial speed decreases :math:`v_0 \to 0`.

When :math:`\lvert\cos\Theta\rvert = 1`, however, possibly in the first case and the fifth case of :eq:`maxaccel theta`, the growth of speed is linear. Even with the presence of ground friction, the growth of speed can be linear under an arithmetic friction. For example, in the default game settings, :math:`\cos\Theta = 1` on the ground when :math:`\lVert\mathbf{v}\rVert \le M \left(1 - k_e\tau A\right)`. In addition, the arithmetic friction is at play when :math:`\lVert\mathbf{v}\rVert < E`. Therefore, the speed at the :math:`n`-th frame is

.. math:: \lVert\mathbf{v}_n\rVert = \lVert\mathbf{v}_0\rVert + n\tau \left( k_eMA - Ek \right)

as long as :math:`\lVert\mathbf{v}_n\rVert < \min(E, M\left( 1 - k_e\tau A \right))`.

.. _agst:

Air-ground speed threshold
~~~~~~~~~~~~~~~~~~~~~~~~~~

The acceleration of groundstrafe is usually greater than that of airstrafe. It
is for this reason that groundstrafing is used to initiate bunnyhopping.
However, once the speed increases beyond :math:`E` the acceleration will begin
to decrease, as the friction grows proportionally with the speed. There will be
a critical speed beyond which the acceleration of airstrafe exceeds that of
groundstrafe. This is called the *air-ground speed threshold* (AGST), admittedly
a rather non-descriptive name.

Analytic solutions for AGST are always available, but they are cumbersome to
write and code. Sometimes the speed curves for airstrafe and groundstrafe
intersects several times, depending even on the initial speed itself. A more
practical solution in practice is to simply use Equation :eq:`nextspeed` to
compute the new airstrafe and groundstrafe speeds then comparing them.

It is also important to note that, even if the air acceleration is greater than the ground acceleration for a given speed, it does not mean that it is optimal to actually leave the ground for air acceleration at that particular time. To illustrate, assume the default Half-Life settings and :math:`\tau = 0.001`. Suppose also the player is on the ground, and the speed is very low at :math:`\lVert\mathbf{v}\rVert = 30`. After one frame of groundstrafing, the new speed would be

.. math:: \lVert\mathbf{v}'_\text{ground}\rVert = \lVert\mathbf{v}\rVert + \tau \left( k_eMA - Ek\right) = 30 + 0.001 \cdot \left( 1 \cdot 320 \cdot 10 - 100 \cdot 4 \right) = 32.8

On the other hand, the player could also ducktap or jump to get into the air and airstrafe, which would have yielded a speed of

.. math::
   \begin{aligned}
   \lVert\mathbf{v}'_\text{air}\rVert &= \sqrt{\lVert\mathbf{v}\rVert^2 + k_e\tau MA\left(2L - k_e\tau MA\right)} \\
   &= \sqrt{30^2 + 1 \cdot 0.001 \cdot 320 \cdot 10 \left( 60 - 1 \cdot 0.001 \cdot 320 \cdot 10 \right)} \\
   &\approx 32.89
   \end{aligned}

We have :math:`\lVert\mathbf{v}'_\text{air}\rVert > \lVert\mathbf{v}'_\text{ground}\rVert`. If the player actually ducktaps to leave the ground, it would have taken the player approximately 0.25s to land back onto the ground. However, before the player could have done so, the air acceleration would have already diminished owing to the sublinear growth mentioned in :ref:`maxaccel growth`. For example, even with :math:`\lVert\mathbf{v}\rVert = 40`, the next speed is :math:`\approx 42.2` for a speed difference of :math:`\approx 2.2`, which is lower than what would be obtained from groundstrafing.

Effects of bunnyhop cap
~~~~~~~~~~~~~~~~~~~~~~~

It is impossible to avoid the bunnyhop cap (see :ref:`bunnyhop cap`) when jumping in later official releases of the game. To lift off the ground and avoid the effects of ground friction, one alternative would be to ducktap instead (see :ref:`ducktapping`). However, each ducktap requires the player to slide on the ground for one frame. Without using very high frame rates to force the frame to be :math:`\tau_p = 0`, the player will lose speed due to friction, especially at lower frame rates. In addition, the player cannot ducktap if there is insufficient clearance above the player. In such cases, jumping is the only way to maintain speed, though there are different possible ways to approach this. Regardless of the movement strategy, we must not trigger the cap itself when jumping, because that would cause an instant and significant reduction in speed.

.. constant-speed
..    The constant-speed strategy is simply maintaining a constant horizontal speed of :math:`1.7M_m`, just below the cap, without performing any type of strafing that changes the speed. This strategy is the simplest to execute. If we need to turn left or right, we simply strafe in a speed-preserving way (see :ref:`speed preserving strafing`).

.. maximum-acceleration on both air and ground
..    Immediately after a jump, the player begins to perform maximum-acceleration strafing in the air. Eventually, gravity will pull the player back onto the ground, this time with a speed higher than the cap of :math:`1.7 M_m`. The player must not jump at this point to avoid triggering the speed reduction. Instead, the player continues to perform maximum-acceleration groundstrafe. If the landing speed is higher than the air-ground speed threshold (see:`agst`), then the speed on the ground will decay nonetheless, in spite of the "maximum-acceleration" strafing. Once the speed reaches back to :math:`1.7 M_m`, the player jumps again to repeat the cycle.

.. maximum-acceleration in the air, friction on the ground
..    Blah

.. maximum-acceleration in the air, maximum-deceleration on the ground
..    Blah

.. maximum-acceleration in the air, maximum-deceleration in the air
..    Blah


.. One way would be to move at constant horizontal speed, which is :math:`1.7M_m`.
.. The second way would be to accelerate while in the air, then backpedal after
.. landing on the ground until the speed reduces to :math:`1.7M_m` before jumping
.. off again.  Yet another way would be to accelerate in the air *and* on the
.. ground, though the speed will still decrease while on the ground as long as the
.. speed is greater than the maximum groundstrafe speed.  To the determine the
.. most optimal method we must compare the distance travelled for a given number
.. of frames.  We will assume that the maximum groundstrafe speed is lower than
.. :math:`1.7M_m`.

It turns out that the answer is not as straightforward as we may have thought and would require more investigations.

Maximum deceleration
--------------------

It is often the case that the player needs to rapidly decelerate in the air or on the ground without any aid using weapons, damage, or solid entities. When the player is on the ground, deceleration is easy to achieve by simply issuing the ``+use`` command, which would exponentially reduce the velocity by a factor of 0.3 per frame. When the player is in the air, however, the player must rely on the pure air movement physics to decelerate as much as possible.

Arguments of the minima
~~~~~~~~~~~~~~~~~~~~~~~

Using the tools and partial results we built earlier in :ref:`maxaccel`, we can perform a similar case-by-case analysis for the different permutations of :math:`\{0, \cos\zeta, \cos\bar{\zeta}\}`. We will not repeat some of the steps in the following analyses.

:math:`0 \le \cos\zeta \le \cos\bar{\zeta}`
   If :math:`\cos\zeta \ge 1`, then the minimum point is simply at :math:`\cos\theta = -1` since :math:`\mu = \gamma_1` for all :math:`-1 \le \cos\theta \le 1`.

   Suppose :math:`\cos\zeta < 1` and :math:`\cos\bar{\zeta} > 1`. Then, :math:`\lVert\mathbf{v}'\rVert = \lVert\mathbf{v}'_{\mu=\gamma_2}\rVert` is strictly decreasing in :math:`\cos\zeta \le \cos\theta \le 1`, so we must consider the points :math:`\cos\theta = \pm 1`. We show that the global minimum is still at :math:`\cos\theta = -1`. Calculate the local minima at :math:`\cos\theta = -1` and :math:`\cos\theta = 1`:

   .. math::
      \begin{aligned}
      \lVert\mathbf{v}'(\cos\theta=-1)\rVert &= \big\lvert \lVert\lambda(\mathbf{v})\rVert - k_e\tau MA \big\rvert \\
      \lVert\mathbf{v}'(\cos\theta=1)\rVert &= L
      \end{aligned}

   Suppose the minimum point is at :math:`\cos\theta = 1`. This implies

   .. math::
      \begin{aligned}
      \lVert\mathbf{v}'(\cos\theta=1)\rVert &\le \lVert\mathbf{v}'(\cos\theta=-1)\rVert \\
      L &\le \big\lvert \lVert\lambda(\mathbf{v})\rVert - k_e\tau MA \big\rvert
      \end{aligned}

   Assume :math:`\lVert\lambda(\mathbf{v})\rVert - k_e\tau MA \ge 0`. Then this implies

   .. math:: L + k_e\tau MA \le \lVert\lambda(\mathbf{v})\rVert

   which is a contradiction, because our supposition that :math:`\cos\bar{\zeta} > 1` implies :math:`\lVert\lambda(\mathbf{v})\rVert < L`. Assume instead that :math:`\lVert\lambda(\mathbf{v})\rVert - k_e\tau MA \le 0`. Then we obtain

   .. math:: -\left( L - k_e\tau MA \right) \ge \lVert\lambda(\mathbf{v})\rVert

   But :math:`0 \le \cos\zeta` implies :math:`L - k_e\tau MA \ge 0` and clearly :math:`\lVert\lambda(\mathbf{v})\rVert \ge 0`, which is a contradiction. This concludes the proof.

   Suppose :math:`\cos\zeta \le \cos\bar{\zeta} \le 1`. Then in :math:`-1 \le \cos\theta \le \cos\zeta`, :math:`\lVert\mathbf{v}'\rVert = \lVert\mathbf{v}'_{\mu=\gamma_1}\rVert` is strictly increasing with a minimum point at :math:`\cos\theta = -1`. In :math:`\cos\zeta \le \cos\theta \le \cos\bar{\zeta}`, :math:`\lVert\mathbf{v}'\rVert = \lVert\mathbf{v}'_{\mu=\gamma_2}\rVert` is strictly decreasing with a minimum point at :math:`\cos\theta = \cos\bar{\zeta}` and a minimum value of :math:`\lVert\mathbf{v}'\rVert = \lVert\lambda(\mathbf{v})\rVert` corresponding to :math:`\mu = 0`. In :math:`\cos\bar{\zeta} \le \cos\theta \le 1`, the value stays at :math:`\lVert\mathbf{v}'\rVert = \lVert\lambda(\mathbf{v})\rVert`. We show that the global minimum is yet again at :math:`\cos\theta = -1`. Calculate the local minima corresponding to :math:`\cos\theta = -1` and :math:`\cos\theta \in [\cos\bar{\zeta}, 1]`. We have

   .. math::
      \begin{aligned}
      \lVert\mathbf{v}'(\cos\theta=-1)\rVert &= \big\lvert \lVert\lambda(\mathbf{v})\rVert - k_e\tau MA \big\rvert \\
      \lVert\mathbf{v}'(\cos\theta \in [\cos\bar{\zeta},1])\rVert &= \lVert\lambda(\mathbf{v})\rVert
      \end{aligned}

   Suppose the global minimum is at :math:`\cos\theta \in [\cos\bar{\zeta}, 1]`. This implies

   .. math:: \lVert\lambda(\mathbf{v})\rVert \le \big\lvert \lVert\lambda(\mathbf{v})\rVert - k_e\tau MA \big\rvert

   Assume :math:`\lVert\lambda(\mathbf{v})\rVert - k_e\tau MA \ge 0`. Then we obtain

   .. math:: 0 \ge k_e\tau MA

   which is a contradiction. Assume instead that :math:`\lVert\lambda(\mathbf{v})\rVert - k_e\tau MA \le 0`, which implies

   .. math:: \lVert\lambda(\mathbf{v})\rVert \le \frac{1}{2} k_e\tau MA

   But :math:`\cos\bar{\zeta} \le 1` implies :math:`L \le \lVert\lambda(\mathbf{v})\rVert`. Putting these inequalities together yields

   .. math:: L - \frac{1}{2} k_e\tau MA \le 0

   Since :math:`L \ge 0` and :math:`k_e\tau MA \ge 0`, this further implies that

   .. math:: L - k_e\tau MA < L - \frac{1}{2} k_e\tau MA \le 0

   But :math:`0 \le \cos\zeta` implies :math:`L - k_e\tau MA \ge 0`, which is a contradiction. This concludes the proof.

   We conclude that

   .. math:: \underset{\cos\theta}{\operatorname{argmin}} \lVert\mathbf{v}'\rVert = -1

:math:`0 \le \cos\bar{\zeta} \le \cos\zeta`
   In :math:`-1 \le \cos\theta \le \cos\bar{\zeta}`, :math:`\lVert\mathbf{v}'\rVert = \lVert\mathbf{v}'_{\mu=\gamma_1}\rVert` is strictly decreasing. In :math:`\cos\bar{\zeta} \le \cos\theta \le 1`, we have :math:`\lVert\mathbf{v}'\rVert = \lVert\lambda(\mathbf{v})\rVert`. If :math:`\cos\bar{\zeta} > 1`, the minimum point is at :math:`\cos\theta = 1` because :math:`\lVert\mathbf{v}'_{\mu=\gamma_1}\rVert` is strictly decreasing. We conclude that

   .. math:: \underset{\cos\theta}{\operatorname{argmin}} \lVert\mathbf{v}'\rVert = [\min(1,\cos\bar{\zeta}), 1]

:math:`\cos\zeta \le 0 \le \cos\bar{\zeta}`
   Suppose :math:`\cos\zeta < -1` and :math:`\cos\bar{\zeta} > 1`. Then :math:`\lVert\mathbf{v}'\rVert = \lVert\mathbf{v}'_{\mu=\gamma_2}\rVert` for all :math:`-1 \le \cos\theta \le 1`. Since :math:`\lVert\mathbf{v}'_{\mu=\gamma_2}` is an even function in :math:`\cos\theta`, we have

   .. math:: \underset{\cos\theta}{\operatorname{argmin}} \lVert\mathbf{v}'\rVert = \{-1, 1\}

   Suppose :math:`\cos\zeta \ge -1` and :math:`\cos\bar{\zeta} > 1`. Then :math:`\lVert\mathbf{v}'\rVert = \lVert\mathbf{v}'_{\mu=\gamma_1}\rVert` is strictly increasing in :math:`-1 \le \cos\theta \le \cos\zeta`, therefore there are also two local minima at :math:`\cos\theta = -1` and :math:`\cos\theta = 1`. We claim that the global minimum is at :math:`\cos\theta = -1`. Suppose the contrary, that is the global minimum is at :math:`\cos\theta = 1`. This implies

   .. math::
      \begin{aligned}
      \lVert\mathbf{v}'_{\mu=\gamma_2}(\cos\theta=1)\rVert &\le \lVert\mathbf{v}'_{\mu=\gamma_1}(\cos\theta=-1)\rVert \\
      L &\le \big\lvert \lVert\lambda(\mathbf{v})\rVert - k_e\tau MA \big\rvert
      \end{aligned}

   Assume :math:`\lVert\lambda(\mathbf{v})\rVert - k_e\tau MA \ge 0`. Then we have

   .. math:: L + k_e\tau MA \le \lVert\lambda(\mathbf{v})\rVert

   But :math:`\cos\bar{\zeta} \ge 1` implies :math:`\lVert\lambda(\mathbf{v})\rVert \le L`. Putting these inequalities together yields

   .. math:: k_e\tau MA \le 0

   This contradicts :math:`\cos\zeta \le \cos\bar{\zeta}`. Assume instead that :math:`\lVert\lambda(\mathbf{v})\rVert - k_e\tau MA \le 0`. Then we have

   .. math:: -\left( L - k_e\tau MA \right) \ge \lVert\lambda(\mathbf{v})\rVert

   But :math:`-1 \le \cos\zeta \le 0` implies that :math:`\lvert L - k_e\tau MA\rvert = -\left( L - k_e\tau MA \right) \le \lVert\lambda(\mathbf{v})\rVert`, which is a contradiction. This concludes the proof.

   Suppose :math:`\cos\zeta < -1` and :math:`\cos\bar{\zeta} \le 1`. In :math:`-1 \le \cos\theta \le \cos\bar{\zeta}`, :math:`\lVert\mathbf{v}'\rVert = \lVert\mathbf{v}'_{\mu=\gamma_2}\rVert`. In :math:`\cos\bar{\zeta} \le \cos\theta \le 1`, we simply have :math:`\lVert\mathbf{v}'\rVert = \lVert\lambda(\mathbf{v})\rVert`. We claim that the global minimum is always at :math:`\cos\theta = -1`. Suppose the contrary, that the global minimum is at :math:`\cos\theta \in [\cos\bar{\zeta}, 1]`. This implies that

   .. math:: \lVert\lambda(\mathbf{v})\rVert \le \lVert\mathbf{v}'_{\mu=\gamma_2}(\cos\theta=-1)\rVert = L

   This contradicts the assumption that :math:`\cos\bar{\zeta} \le 1` from which we deduce that :math:`\lVert\lambda(\mathbf{v})\rVert \ge L`. End of proof.

   Finally, suppose :math:`\cos\zeta \ge -1` and :math:`\cos\bar{\zeta} \le 1`. Then we again claim that the global minimum occurs at :math:`\cos\theta = -1`. Suppose the contrary, that the global minima occur at :math:`\cos\theta \in [\cos\bar{\zeta}, 1]`. Then this implies that

   .. math:: \lVert\lambda(\mathbf{v})\rVert \le \lVert\mathbf{v}'_{\mu=\gamma_1}(\cos\theta=-1)\rVert = \big\lvert \lVert\lambda(\mathbf{v})\rVert - k_e\tau MA \big\rvert

   Assume that :math:`\lVert\lambda(\mathbf{v})\rVert - k_e\tau MA \ge 0`. Then we have

   .. math:: \ge k_e\tau MA \le 0

   which contradicts :math:`\cos\zeta \le \cos\bar{\zeta}`. Assume otherwise that :math:`\lVert\lambda(\mathbf{v})\rVert - k_e\tau MA \le 0`. Then we obtain

   .. math:: \lVert\lambda(\mathbf{v})\rVert \le \frac{1}{2} k_e\tau MA

   On the other hand, :math:`\cos\zeta \ge -1` implies

   .. math::
      \begin{aligned}
      -\left( L - k_e\tau MA \right) &\le \lVert\lambda(\mathbf{v})\rVert \\
      L &\ge \frac{1}{2} k_e\tau MA
      \end{aligned}

   But :math:`\cos\bar{\zeta} \le -1` also implies

   .. math:: \lVert\lambda(\mathbf{v})\rVert \ge L \ge \frac{1}{2} k_e\tau MA

   which is a contradiction. End of proof.

   We conclude that

   .. math:: \underset{\cos\theta}{\operatorname{argmin}} \lVert\mathbf{v}'\rVert =
      \begin{cases}
      \{ -1, 1 \} & \cos\zeta < -1 \land \cos\bar{\zeta} > 1 \\
      -1 & \cos\zeta \ge -1 \lor \cos\bar{\zeta} \le 1
      \end{cases}

:math:`\cos\bar{\zeta} \le 0 \le \cos\zeta`
   In :math:`-1 \le \cos\theta \le \cos\bar{\zeta}`, :math:`\lVert\mathbf{v}'\rVert = \lVert\mathbf{v}'_{\mu=\gamma_1}\rVert` is strictly decreasing. In :math:`\cos\bar{\zeta} \le \cos\theta \le 1`, :math:`\lVert\mathbf{v}'\rVert = \lVert\lambda(\mathbf{v})\rVert`. We conclude that

   .. math:: \underset{\cos\theta}{\operatorname{argmin}} \lVert\mathbf{v}'\rVert = [\max(-1, \cos\bar{\zeta}), 1]

:math:`\cos\zeta \le \cos\bar{\zeta} \le 0`
   In :math:`-1 \le \cos\theta \le \cos\zeta`, :math:`\lVert\mathbf{v}'\rVert = \lVert\mathbf{v}'_{\mu=\gamma_1}\rVert` is strictly increasing. In :math:`\cos\zeta \le \cos\theta \le \cos\bar{\zeta}`, :math:`\lVert\mathbf{v}'\rVert = \lVert\mathbf{v}'_{\mu=\gamma_2}\rVert` is also strictly increasing and ends with :math:`\lVert\mathbf{v}'\rVert = \lVert\lambda(\mathbf{v})\rVert` at :math:`\cos\theta = \cos\bar{\zeta}`. In :math:`\cos\bar{\zeta} \le \cos\theta \le 1`, we have :math:`\lVert\mathbf{v}'\rVert = \lVert\lambda(\mathbf{v})\rVert`. We conclude that

   .. math:: \underset{\cos\theta}{\operatorname{argmin}} \lVert\mathbf{v}'\rVert =
      \begin{cases}
      -1 & \cos\bar{\zeta} > -1 \\
      [-1, 1] & \cos\bar{\zeta} \le -1 \\
      \end{cases}

:math:`\cos\bar{\zeta} \le \cos\zeta \le 0`
   The analysis and result is exactly the same as that in the :math:`\cos\bar{\zeta} \le 0 \le \cos\zeta` case.

Combining the above case-by-case findings, we have the global minimum at

.. math::
   \begin{aligned}
   & \underset{\cos\theta}{\operatorname{argmin}} \lVert\mathbf{v}'\rVert = \\
   & \begin{cases}
   -1 & k_e\tau MA \ge 0 \land L \ge 0 \land L - k_e\tau MA \ge 0 \\
   -1 & k_e\tau MA \ge 0 \land L \ge 0 \land L - k_e\tau MA \le 0 \land (\cos\zeta \ge -1 \lor \cos\bar{\zeta} \le 1) \\
   \{ -1, 1 \} & k_e\tau MA \ge 0 \land L \ge 0 \land L - k_e\tau MA \le 0 \land \cos\zeta < -1 \land \cos\bar{\zeta} > 1 \\
   -1 & k_e\tau MA \ge 0 \land L \le 0 \land L - k_e\tau MA \le 0 \land \cos\bar{\zeta} > -1 \\
   [-1, 1] & k_e\tau MA \ge 0 \land L \le 0 \land L - k_e\tau MA \le 0 \land \cos\bar{\zeta} \le -1 \\
   [\min(\max(-1, \cos\bar{\zeta}), 1), 1] & k_e\tau MA \le 0
   \end{cases}
   \end{aligned}
   :label: maxdecel theta

Effects of frame rate
~~~~~~~~~~~~~~~~~~~~~

In every case in :eq:`maxdecel theta`, the frame rate has no effect on the deceleration if we ignore the effects of friction. For example, suppose :math:`\cos\theta = -1` in the first case. Then the speed in the next frame may be written as

.. math:: \lVert\mathbf{v}'\rVert = \big\lvert \lVert\lambda(\mathbf{v})\rVert - k_e\tau MA \big\rvert

Assuming :math:`\tau = \tau_g`, the absence of friction, and :math:`\lVert\lambda(\mathbf{v})\rVert - k_e\tau MA \ge 0`, then the deceleration in one frame is therefore

.. math:: \frac{\lVert\mathbf{v}\rVert - k_e\tau MA  - \lVert\mathbf{v}\rVert}{\tau_g} = -k_eMA

which is independent of the frame rate.

.. TODO:

.. Maximum projected acceleration
.. ------------------------------

.. Intuitively, it appears that the objective function in the analysis in :ref:`maxaccel` is flawed in practical applications, because it optimises for *speed* in any direction, rather than the speed projected onto some direction vector that points towards the destination.

.. _speed preserving strafing:

Speed preserving strafing
-------------------------

Speed preserving strafing can be useful when we are strafing at high :math:`A`. It takes only about 4.4s to reach 2000 ups from rest at :math:`A = 100`. While making turns at 2000 ups, if the velocity is not parallel to the global axes the speed will exceed ``sv_maxvelocity``. Occasionally, this can prove cumbersome as the curvature decreases with increasing speed, making the player liable to collision with walls or other obstacles. Besides, as the velocity gradually becomes parallel to one of the global axes again, the speed will drop back to ``sv_maxvelocity``. This means, under certain situations, that the slight speed increase in the process of making the turn has little benefit. Therefore, it can sometimes be helpful to simply make turns at a constant ``sv_maxvelocity``. This is where the technique of *speed preserving strafing* comes into play. Another situation might be that we want to groundstrafe at a constant speed. When the speed is relatively low, constant speed groundstrafing can produce a very sharp curve, which is sometimes desirable in a very confined space.

We first consider the case where friction is absent. Setting :math:`\lVert\mathbf{v}'\rVert = \lVert\mathbf{v}\rVert` in Equation :eq:`nextspeed` and solving,

.. math:: \cos\theta = -\frac{\mu}{2\lVert\mathbf{v}\rVert}

If :math:`\mu = \gamma_1` then we must have :math:`\gamma_1 \le \gamma_2`, or

.. math:: k_e \tau MA \le L - \lVert\mathbf{v}\rVert \cos\theta \implies k_e \tau MA \le 2L

At this point we can go ahead and write out the full formula for :math:`\theta` that preserves speed while strafing

.. math:: \cos\theta =
          \begin{cases}
          -\displaystyle\frac{k_e \tau MA}{2\lVert\mathbf{v}\rVert} & k_e \tau MA \le 2L \\
          -\displaystyle\frac{L}{\lVert\mathbf{v}\rVert} & k_e \tau MA > 2L
          \end{cases}

On the other hand, if friction is present, then we have

.. math:: \lVert\mathbf{v}\rVert^2 = \lVert\lambda(\mathbf{v})\rVert^2 + \mu^2 + 2 \mu
          \lVert\lambda(\mathbf{v})\rVert \cos\theta

By the usual line of attack, we force :math:`\mu = \gamma_1` which implies that
:math:`\gamma_1 \le \gamma_2`, giving the formula

.. math:: \cos\theta = \frac{1}{2\lVert\lambda(\mathbf{v})\rVert} \left(
          \frac{\lVert\mathbf{v}\rVert^2 - \lVert\lambda(\mathbf{v})\rVert^2}{k_e \tau MA} -
          k_e \tau MA \right)

and the necessary condition

.. math:: \frac{\lVert\mathbf{v}\rVert^2 - \lVert\lambda(\mathbf{v})\rVert^2}{k_e \tau
          MA} + k_e \tau MA\le 2L

We can check that if friction is absent, then :math:`\lVert\mathbf{v}\rVert = \lVert\lambda(\mathbf{v})\rVert` and the condition becomes what we have obtained earlier. If this condition failed, however, then we instead have

.. math:: \cos\theta = -\frac{\sqrt{L^2 - \left( \lVert\mathbf{v}\rVert^2 -
          \lVert\lambda(\mathbf{v})\rVert^2 \right)}}{\lVert\lambda(\mathbf{v})\rVert}

Note that we took the negative square root, because :math:`\theta` needs to be
as large as possible so that the curvature of the strafing path is maximised,
which is one of the purposes of speed preserving strafing.  To derive the
necessary condition for the formula above, we again employ the standard
strategy, yielding

.. math:: k_e \tau MA - L > \sqrt{L^2 - \left( \lVert\mathbf{v}\rVert^2 -
          \lVert\lambda(\mathbf{v})\rVert^2 \right)}

Observe that we need :math:`k_e \tau MA > L` and :math:`L^2 \ge
\lVert\mathbf{v}\rVert^2 - \lVert\lambda(\mathbf{v})\rVert^2`.  Then we square the
inequality to yield the converse of the condition for :math:`\mu = \gamma_1`,
as expected.  Putting these results together, we obtain

.. math:: \cos\theta =
          \begin{cases}
          \displaystyle \frac{1}{2\lVert\lambda(\mathbf{v})\rVert} \left(
          \frac{\lVert\mathbf{v}\rVert^2 - \lVert\lambda(\mathbf{v})\rVert^2}{k_e \tau MA} -
          k_e \tau MA \right) & \displaystyle \text{if } \frac{\lVert\mathbf{v}\rVert^2 -
          \lVert\lambda(\mathbf{v})\rVert^2}{k_e \tau MA} + k_e \tau MA\le 2L \\
          \displaystyle -\frac{\sqrt{L^2 - \left( \lVert\mathbf{v}\rVert^2 -
          \lVert\lambda(\mathbf{v})\rVert^2 \right)}}{\lVert\lambda(\mathbf{v})\rVert} &
          \displaystyle \text{otherwise, if } k_e \tau MA > L \text{ and } L^2 \ge
          \lVert\mathbf{v}\rVert^2 - \lVert\lambda(\mathbf{v})\rVert^2
          \end{cases}

Note that, regardless of whether friction is present, if
:math:`\lvert\cos\theta\rvert > 1` then we might resort to using the optimal
angle to strafe instead.  This can happen when, for instance, the speed is so
small that the player will always gain speed regardless of strafing direction.
Or it could be that the effect of friction exceeds that of strafing, rendering
it impossible to prevent the speed reduction.  If
:math:`\lVert\mathbf{v}\rVert` is greater than the maximum groundstrafe speed,
then the angle that minimises the inevitable speed loss is obviously the
optimal strafing angle.

Curvature
---------

The locus of a point obtained by strafing is a spiral. Intuitively, at any given speed there is a limit to how sharp a turn can be made without lowering acceleration. It is commonly known that this limit grows harsher with higher speed. As tight turns are common in Half-Life, this becomes an important consideration that preoccupies speedrunners at almost every moment. Learning how navigate through tight corners by strafing without losing speed is a make-or-break skill in speedrunning.

It is natural to ask exactly how this limit can be quantified for the benefit of TASing. The simplest way to do so is to consider the *radius of curvature* of the path. Obviously, this quantity is not constant with time, except for speed preserving strafing. Therefore, when we talk about the radius of curvature, precisely we are referring to the *instantaneous* radius of curvature, namely the radius at a given instant in time. But time is discrete in Half-Life, so this is approximated by the radius in a given frame.

90 degrees turns
~~~~~~~~~~~~~~~~

Passageways in Half-Life commonly bend perpendicularly, so we frequently make 90
degrees turns by strafing. We intuitively understand how the width of a passage
limits the maximum radius of curvature one can sustain without colliding with
the walls. This implies that the speed is limited as well. When planning for
speedruns, it can prove useful to be able to estimate this limit for a given
turn without running a simulation or strafing by hand. In particular, we want to
compute the maximum speed for a given passage width.

.. figure:: images/90-degrees-bend-c2a2e.jpg
   :name: 90 degrees c2a2e

   A common 90 degrees bend in the On A Rail chapter in Half-Life. Shown in this
   figure is one such example in the map ``c2a2e``. In an optimised speedrun,
   the player would be moving extremely fast in this section due to an earlier
   boost.

.. figure:: images/90-degrees-strafe-radius.png
   :name: 90 degrees strafe radius
   :scale: 50%

   Simplifying model of a common scenario similar to the one shown in
   :numref:`90 degrees c2a2e`.

We start by making some simplifying assumptions that will greatly reduce the
difficulty of analysis while closely modelling actual situations in practice.
Referring to :numref:`90 degrees strafe radius`, the first assumption we make is
that the width of the corridor is the same before and after the turn. This width
is denoted as :math:`d`, as one can see in the figure. This assumption is
justified because this is often true or approximately true in Half-Life maps.
The second assumption is that the path is circular. The centre of this circle,
also named the *centre of curvature*, is at point :math:`C`. As noted earlier,
the strafing path is in general a spiral with varying radius of curvature.
Nevertheless, the total time required to make such a turn is typically very
small. Within such short time frame, the radius would not have changed
significantly. Therefore it is not absurd to assume that the radius of curvature
is constant while making the turn. The third assumption is that the positions of
the player before and after making the turn coincide with the walls. This
assumption is arguably less realistic, but the resulting path is the larger
circular arc one can fit in this space.

By trivial applications of the Pythagorean theorem, it can be shown that the relationship between the radius of curvature :math:`r` and the width of the corridor :math:`d` is given by

.. math:: r = \left( 2 + \sqrt{2} \right) d \approx 3.414 d

This formula may be used to estimate the maximum radius of curvature for making such a turn without collision. However, the radius of curvature by itself is not very useful. We may wish to further estimate the maximum speed corresponding to this :math:`r`.

Radius-speed relationship
~~~~~~~~~~~~~~~~~~~~~~~~~

The following figure depicts the positions of the player at times :math:`t = 0`, :math:`t = \tau` and :math:`t = 2\tau`. The initial speed is :math:`\lVert\mathbf{v}\rVert`. All other symbols have their usual meaning.

.. image:: images/radius-estimate-xy.png
   :height: 775px
   :width: 1135px
   :scale: 50%

Based on the figure, the radius of curvature may be approximated as the :math:`y`-intercept, or :math:`c`. Obviously, a more accurate approximation may be achieved by averaging :math:`c` and :math:`\mathit{BC}`. However, this results in a clumsy formula with little benefit. Empirically, the approximation by calculating :math:`c` is sufficiently accurate in practice. In consideration of this, it can be calculated that

.. math:: r \approx c = \frac{\tau}{\sin\theta} \left( \frac{2}{\mu} \lVert\mathbf{v}\rVert^2 + 3 \lVert\mathbf{v}\rVert \cos\theta + \mu \right)
  :label: radius-speed-relationship

Note that this is the most general formula, applicable to any type of strafing. From this equation, observe that the radius of curvature grows with the square of speed. This is a fairly rapid growth. On the other hand, under maximum speed strafing, the speed grows with the square root of time. Informally, the result of these two growth rates conspiring with one another is that the radius of curvature grows linearly with time. We also observe that the radius of curvature is directly influenced by :math:`\tau`, as experienced strafers would expect. Namely, we can make sharper turns at higher frame rates.

From Equation :eq:`radius-speed-relationship` we can derive formulae for various types of strafing by eliminating :math:`\theta`. For instance, in Type 2 strafing we have :math:`\theta = \pi/2`. Substituting, we obtain a very simple expression for the radius:

.. math:: r \approx \tau \left( \frac{2}{L} \lVert\mathbf{v}\rVert^2 + L \right)

Or, solving for :math:`\lVert\mathbf{v}\rVert`, we obtain a more useful equation:

.. math:: \lVert\mathbf{v}\rVert \approx \sqrt{\frac{L}{2} \left( \frac{r}{\tau} - L \right)}

For Type 1 strafing, the formula is clumsier. Recall that we have :math:`\mu = k_e \tau MA` and

.. math:: \cos\theta = \frac{L - k_e \tau MA}{\lVert\mathbf{v}\rVert}

To eliminate :math:`\sin\theta`, we can trivially rewrite the :math:`\cos\theta` equation in this form

.. math:: \sin\theta = \frac{\sqrt{\lVert\mathbf{v}\rVert^2 - (L - k_e \tau MA)^2}}{\lVert\mathbf{v}\rVert}

Then we proceed by substituting, yielding

.. math:: r \approx \frac{\tau \lVert\mathbf{v}\rVert}{\sqrt{\lVert\mathbf{v}\rVert^2 - (L - k_e \tau MA)^2}} \left( \frac{2}{k_e \tau MA} \lVert\mathbf{v}\rVert^2 + 3L - 2 k_e \tau MA \right)

We cannot simplify this equation further. In fact, solving for :math:`\lVert\mathbf{v}\rVert` is non-trivial as it requires finding a root to a relatively high order polynomial equation. As per the usual strategy when facing similar difficulties, we resort to iterative methods.
