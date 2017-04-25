Strafing
========

Here we will be discussing movement physics primarily associated with the
player.  Physics of other entities such as monster and boxes are presumed to
share some similarities with the player, though they are usually not important.


Fundamental movement equation
-----------------------------

For subsequence analyses that involve mathematics, we will not concern
ourselves with the details of how they were implemented in ``PM_AirMove`` and
``PM_WalkMove``.  For example, we will not be thinking in terms of ``wishvel``,
``addspeed``, ``pmove->right`` and so on.

Denote :math:`\mathbf{v}` the player velocity in the current frame and
:math:`\mathbf{v}'` the new velocity.  Denote :math:`\mathbf{\hat{a}}` the unit
acceleration vector.  Let :math:`\theta` the angle between :math:`\mathbf{v}`
and :math:`\mathbf{\hat{a}}`.  Then

.. math:: \mathbf{v}' = \mathbf{v} + \mu\mathbf{\hat{a}}
   :label: newvel

with

.. math:: \mu =
          \begin{cases}
          \min(\gamma_1, \gamma_2) & \text{if } \gamma_2 > 0 \\
          0 & \text{otherwise}
          \end{cases}
          \quad\quad
          M = \min\left( M_m, \sqrt{F^2 + S^2} \right) \\
          \gamma_1 = k_e \tau MA
          \quad\quad
          \gamma_2 = L - \mathbf{v} \cdot \mathbf{\hat{a}} = L - \lVert\mathbf{v}\rVert \cos\theta
   :nowrap:

where :math:`\tau` is called the *frame time*, which is just the inverse of
frame rate.  :math:`L = 30` when airstrafing and :math:`L = M` when
groundstrafing.  :math:`A` is the value of ``sv_airaccelerate`` when
airstrafing and ``sv_accelerate`` when groundstrafing.  Lastly, :math:`k_e` is
called the *environmental friction* which is usually 1 and will be explained in
:ref:`friction`.

Ignoring the roll angle, the unit acceleration vector is such that
:math:`\mathbf{a} = F \mathbf{\hat{f}} + S \mathbf{\hat{s}}`, which is in
:math:`\mathbb{R}^2`.  We have unit forward vector :math:`\mathbf{\hat{f}} =
\langle\cos\vartheta, \sin\vartheta\rangle` where :math:`\vartheta` is the yaw
angle.  This means :math:`\mathbf{\hat{f}}` is essentially directed parallel to
the player view.  :math:`\mathbf{\hat{s}}` is directed perpendicular to
:math:`\mathbf{\hat{f}}` rightward, or :math:`\mathbf{\hat{s}} =
\langle\sin\vartheta, -\cos\vartheta\rangle`.  The magnitude of
:math:`\mathbf{a}` is simply :math:`\sqrt{F^2 + S^2}`.  In the following
analysis we will not concern ourselves with the components of
:math:`\mathbf{a}`, but instead parameterise the entire equation in
:math:`\theta`.

Besides, we will assume that :math:`\lVert\langle F,S\rangle\rVert \ge M`.  If
this is not the case, we must replace :math:`M \mapsto \lVert\langle
F,S\rangle\rVert` for all appearances of :math:`M` below.  Throughout this
document we will assume that :math:`M`, :math:`A`, :math:`\tau`, :math:`k`,
:math:`k_e` and :math:`E` are positive.


Optimal strafing
----------------

The new speed :math:`\lVert\mathbf{v}'\rVert` can be expressed as

.. math:: \lVert\mathbf{v}'\rVert = \sqrt{\mathbf{v}' \cdot \mathbf{v}'} =
          \sqrt{(\mathbf{v} + \mu\mathbf{\hat{a}}) \cdot (\mathbf{v} + \mu\mathbf{\hat{a}})} =
          \sqrt{\lVert\mathbf{v}\rVert^2 + \mu^2 + 2\lVert\mathbf{v}\rVert \mu \cos\theta}
   :label: nextspeed

Equation :eq:`nextspeed`, sometimes called the *scalar FME*, is often used in
practical applications as the general way to compute new speeds, if
:math:`\theta` is known.  To compute new velocity vectors, given
:math:`\theta`, we can rewrite Equation :eq:`newvel` as

.. math:: \mathbf{v}' = \mathbf{v} + \mu\mathbf{\hat{v}}
          \begin{pmatrix}
          \cos\theta & \mp\sin\theta \\
          \pm\sin\theta & \cos\theta
          \end{pmatrix} \quad\quad \text{if } \mathbf{v} \ne \mathbf{0}
   :label: newvelmat

which expresses :math:`\mathbf{\hat{a}}` as a rotation of
:math:`\mathbf{\hat{v}}` clockwise or anticlockwise, depending on the signs of
:math:`\sin\theta`.  Equation :eq:`newvelmat` can be useful when computing line
strafing.

If :math:`\mu = \gamma_1` and :math:`\mu = \gamma_2` we have

.. math:: \begin{align*}
          \lVert\mathbf{v}'\rVert_{\mu = \gamma_1} &= \sqrt{\lVert\mathbf{v}\rVert^2 +
          k_e \tau MA \left( k_e \tau MA + 2 \lVert\mathbf{v}\rVert \cos\theta \right)} \\
          \lVert\mathbf{v}'\rVert_{\mu = \gamma_2} &= \sqrt{\lVert\mathbf{v}\rVert^2 \sin^2 \theta + L^2}
          \end{align*}

respectively.  Let :math:`\theta` the independent variable, then notice that
these functions are invariant under the transformation :math:`\theta \mapsto
-\theta`.  Hence we will consider only :math:`\theta \ge 0` for simplicity.
Observe that

1. :math:`\lVert\mathbf{v}'\rVert_{\mu = \gamma_1}` and
   :math:`\lVert\mathbf{v}'\rVert_{\mu = \gamma_2}` intersects only at
   :math:`\theta = \zeta` where :math:`\cos\zeta = (L - k_e \tau MA)
   \lVert\mathbf{v}\rVert^{-1}` is obtained by solving :math:`\gamma_1 =
   \gamma_2`

2. :math:`\lVert\mathbf{v}'\rVert_{\mu = \gamma_1}` is decreasing in :math:`0
   \le \theta \le \pi`

3. :math:`\lVert\mathbf{v}'\rVert_{\mu = \gamma_2}` is increasing in :math:`0
   \le \theta \le \pi/2` and decreasing in :math:`\pi/2 \le \theta \le \pi`

4. :math:`\mu = \gamma_2` if :math:`0 \le \theta \le \zeta`, and :math:`\mu =
   \gamma_1` if :math:`\zeta < \theta \le \pi`.

Therefore, we claim that to maximise :math:`\lVert\mathbf{v}'\rVert` we have
optimal angle

.. math:: \theta =
          \begin{cases}
          \pi/2 & \text{if } L - k_e \tau MA \le 0 \\
          \zeta & \text{if } 0 < L - k_e \tau MA \le \lVert\mathbf{v}\rVert \\
          0 & \text{otherwise}
          \end{cases}

.. index:: Type 1 strafing

To see this, suppose :math:`0 < \theta < \pi/2`.  This implies the second
condition described above.  When this is the case, the always decreasing curve
of :math:`\lVert\mathbf{v}'\rVert_{\mu=\gamma_1}` intersects that of
:math:`\lVert\mathbf{v}'\rVert_{\mu=\gamma_2}` at the point where the latter
curve is increasing.  To the left of this point is the domain of the latter
curve, which is increasing until we reach the discontinuity at the point of
intersection, beyond which is the domain of the former curve.  Therefore the
optimal angle is simply at the peak: the point of intersection :math:`\theta =
\zeta`.

.. index:: Type 2 strafing

If :math:`\theta \ge \pi/2`, the former curve intersects the latter curve at
the point where the latter is decreasing.  :math:`0 \le \theta \le \zeta` is
the domain of the latter curve which contains the maximum point at
:math:`\pi/2`.  Have a look at the graphs below:

.. image:: static/optang-1.png

Note that these are sketches of the real graphs, therefore they are by no means
accurate.  However, they do illustrate the four observations made above
accurately.  The green dashed lines represent the curve of
:math:`\lVert\mathbf{v}'\rVert_{\mu=\gamma_1}`, which is always decreasing
(observation 2).  The blue dashed lines represent
:math:`\lVert\mathbf{v}'\rVert_{\mu=\gamma_2}`, which fits observation 3.  Now
focus on the red lines: they represent the graph of
:math:`\lVert\mathbf{v}'\rVert` if the restriction :math:`\mu = \min(\gamma_1,
\gamma_2)` is factored in, rather than considering each case in isolation.  In
other words, the red lines are what we expect to obtain if we sketch them using
Equation :eq:`nextspeed`.  Notice that the region :math:`0 \le \theta \le
\zeta` is indeed the domain of :math:`\lVert\mathbf{v}'\rVert_{\mu=\gamma_2}`,
and vice versa (observation 4).  Finally, the blue line and green line
intersect only at one point.  Now it is clear where the maximum points are,
along with the optimal :math:`\theta`\ s associated with them.

Having these results, for airstrafing it is a matter of simple substitutions to
obtain

.. math:: \lVert\mathbf{v}_n\rVert =
          \begin{cases}
          \sqrt{\lVert\mathbf{v}\rVert^2 + 900n} & \text{if } \theta = \pi/2 \\
          \sqrt{\lVert\mathbf{v}\rVert^2 + nk_e \tau MA_a (60 - k_e \tau MA_a)} & \text{if } \theta = \zeta \\
          \lVert\mathbf{v}\rVert + nk_e \tau MA_a & \text{if } \theta = 0
          \end{cases}

These equations can be quite useful in planning.  For example, to calculate the
number of frames required to airstrafe from :math:`320` ups to :math:`1000` ups
at default Half-Life settings, we solve

.. math:: 1000^2 = 320^2 + n \cdot 0.001 \cdot 320 \cdot 10 \cdot (60 - 0.001 \cdot 320 \cdot 10) \\
          \implies n \approx 4938
   :nowrap:

For groundstrafing, however, the presence of friction means simple substitution
may not work.


.. _friction:

Friction
--------

Let :math:`k` the friction coefficient, :math:`k_e` the environmental friction
and :math:`E` the stopspeed.  The value of :math:`k` in the game
``sv_friction`` while :math:`E` is ``sv_stopspeed``.  As mentioned previously,
in most cases :math:`k_e = 1` unless the player is standing on a friction
modifier.  If friction is present, then before any physics computation is done,
the velocity must be multiplied by :math:`\lambda` such that

.. math:: \lambda = \max(1 - \max(1, E \lVert\mathbf{v}\rVert^{-1}) k_e k\tau, 0)
   :label: fricfunc

In :math:`Ek\tau \le \lVert\mathbf{v}\rVert \le E`, the kind of friction is
called *arithmetic friction*.  It is so named because if the player is allowed
to slide freely on the ground, the successive speeds form an arithmetic series.
In other words, given initial speed, the speed at the :math:`n`\ -th frame
:math:`\lVert\mathbf{v}_n\rVert` is

.. math:: \lVert\mathbf{v}_n\rVert = \lVert\mathbf{v}_0\rVert - nEk_ek\tau

Let :math:`t = n\tau`, then notice that the value of
:math:`\lVert\mathbf{v}_t\rVert` is independent of the frame rate.  If
:math:`\lVert\mathbf{v}\rVert > E`, however, the friction is called *geometric
friction*

.. math:: \lVert\mathbf{v}_n\rVert = \lVert\mathbf{v}_0\rVert (1 - k_ek\tau)^n

Again, let :math:`t = n\tau`, then :math:`\lVert\mathbf{v}_t\rVert =
\lVert\mathbf{v}_0\rVert (1 - k\tau)^{t/\tau}`.  Observe that

.. math:: \frac{d}{d\tau} \lVert\mathbf{v}_t\rVert = -\frac{t}{\tau}
          \lVert\mathbf{v}_t\rVert \left( \frac{k_ek}{1 - k_ek\tau} +
          \frac{\ln\lvert 1 - k_ek\tau\rvert}{\tau} \right) \le 0 \quad\text{for } t \ge 0

which means :math:`\lVert\mathbf{v}_t\rVert` is strictly increasing with
respect to :math:`\tau` at any given positive :math:`t`.  By increasing
:math:`\tau` (or decreasing the frame rate), the deceleration as a result of
geometric friction becomes larger.

.. index:: Type 1 strafing

There is a limit to the speed achievable by perfect groundstrafing alone.
There will be a critical speed such that the increase in speed exactly cancels
the friction, so that :math:`\lVert\mathbf{v}_{n + 1}\rVert =
\lVert\mathbf{v}_n\rVert`.  For example, suppose optimal :math:`\theta = \zeta`
and geometric friction is at play.  Then if

.. math:: \lVert\mathbf{v}\rVert^2 = (1 - k_e k\tau)^2 \lVert\mathbf{v}\rVert^2 + k_e \tau M^2 A_g (2 - k_e \tau A_g)

we have *maximum groundstrafe speed*

.. math:: M \sqrt{\frac{A_g (2 - k_e \tau A_g)}{k (2 - k_ek\tau)}}

Strafing at this speed effectively degenerates *perfect strafing* into *speed
preserving strafing*, which will be discussed shortly after.  If :math:`k <
A_g`, which is the case in default Half-Life settings, the smaller the
:math:`\tau` the higher the maximum groundstrafe speed. If
:math:`\theta = \pi/2` instead, then the expression becomes

.. math:: \frac{M}{\sqrt{k_ek\tau (2 - k_ek \tau)}}


Bunnyhop cap
------------

We must introduce :math:`M_m`, which is the value of ``sv_maxspeed``.  It is
not always the case that :math:`M_m = M`, since :math:`M` can be affected by
duckstate and the values of :math:`F`, :math:`S` and :math:`U`.

All Steam versions of Half-Life have an infamous "cap" on bunnyhop speed which
is triggered only when jumping with player speed greater than :math:`1.7M_m`.
Note that the aforementioned speed is not horizontal speed, but rather, the
magnitude of the entire :math:`\mathbb{R}^3` vector.  When this mechanism is
triggered, the new velocity will become :math:`1.105 M_m \mathbf{\hat{v}}`.

It is impossible to avoid this mechanism when jumping.  In speedruns a
workaround would be to ducktap instead, but each ducktap requires the player to
slide on the ground for one frame, thereby losing a bit of speed due to
friction.  In addition, a player cannot ducktap if there is insufficient space
above him.  In this case jumping is the only way to maintain speed, though
there are different possible styles to achieve this.

One way would be to move at constant horizontal speed, which is :math:`1.7M_m`.
The second way would be to accelerate while in the air, then backpedal after
landing on the ground until the speed reduces to :math:`1.7M_m` before jumping
off again.  Yet another way would be to accelerate in the air *and* on the
ground, though the speed will still decrease while on the ground as long as the
speed is greater than the maximum groundstrafe speed.  To the determine the
most optimal method we must compare the distance travelled for a given number
of frames.  We will assume that the maximum groundstrafe speed is lower than
:math:`1.7M_m`.

It turns out that the answer is not as straightforward as we may have thought.

TODO!!


Air-ground speed threshold
--------------------------

The acceleration of groundstrafe is usually greater than that of airstrafe.  It
is for this reason that groundstrafing is used to initiate bunnyhopping.
However, once the speed increases beyond :math:`E` the acceleration will begin
to decrease, as the friction grows proportionally with the speed.  There will
be a critical speed beyond which the acceleration of airstrafe exceeds that of
groundstrafe.  This is called the *air-ground speed threshold* (AGST),
admittedly a rather non-descriptive name.

Analytic solutions for AGST are always available, but they are cumbersome to
write and code.  Sometimes the speed curves for airstrafe and groundstrafe
intercepts several times, depending even on the initial speed itself.  A more
practical solution in practice is to simply use Equation :eq:`nextspeed` to
compute the new airstrafe and groundstrafe speeds then comparing them.


Speed preserving strafing
-------------------------

Speed preserving strafing can be useful when we are strafing at high :math:`A`.
It takes only about 4.4s to reach 2000 ups from rest at :math:`A = 100`.  While
making turns at 2000 ups, if the velocity is not parallel to the global axes
the speed will exceed ``sv_maxvelocity``.  Ocassionally, this can prove
cumbersome as the curvature decreases with increasing speed, making the player
liable to collision with walls or other obstacles.  Besides, as the velocity
gradually becomes parallel to one of the global axes again, the speed will drop
back to ``sv_maxvelocity``.  This means, under certain situations, that the
slight speed increase in the process of making the turn has little benefit.
Therefore, it can sometimes be helpful to simply make turns at a constant
``sv_maxvelocity``.  This is where the technique of *speed preserving strafing*
comes into play.  Another situation might be that we want to groundstrafe at a
constant speed.  When the speed is relatively low, constant speed
groundstrafing can produce a very sharp curve, which is sometimes desirable in
a very confined space.

We first consider the case where friction is absent.  Setting
:math:`\lVert\mathbf{v}'\rVert = \lVert\mathbf{v}\rVert` in Equation
:eq:`nextspeed` and solving,

.. math:: \cos\theta = -\frac{\mu}{2\lVert\mathbf{v}\rVert}

If :math:`\mu = \gamma_1` then we must have :math:`\gamma_1 \le \gamma_2`, or

.. math:: k_e \tau MA \le L - \lVert\mathbf{v}\rVert \cos\theta \implies k_e \tau MA \le 2L

At this point we can go ahead and write out the full formula for :math:`\theta`
that preserves speed while strafing

.. math:: \cos\theta =
          \begin{cases}
          -\displaystyle\frac{k_e \tau MA}{2\lVert\mathbf{v}\rVert} & \text{if } k_e \tau MA \le 2L \\
          -\displaystyle\frac{L}{\lVert\mathbf{v}\rVert} & \text{otherwise}
          \end{cases}

On the other hand, if friction is present, we let :math:`\lVert\mathbf{u}\rVert
= \lambda\lVert\mathbf{v}\rVert` be the speed immediately after friction is
applied, where :math:`\lambda` is given in :eq:`fricfunc`.  Now we have

.. math:: \lVert\mathbf{v}\rVert^2 = \lVert\mathbf{u}\rVert^2 + \mu^2 + 2 \mu
          \lVert\mathbf{u}\rVert \cos\theta

By the usual line of attack, we force :math:`\mu = \gamma_1` which implies that
:math:`\gamma_1 \le \gamma_2`, giving the formula

.. math:: \cos\theta = \frac{1}{2\lVert\mathbf{u}\rVert} \left(
          \frac{\lVert\mathbf{v}\rVert^2 - \lVert\mathbf{u}\rVert^2}{k_e \tau MA} -
          k_e \tau MA \right)

and the necessary condition

.. math:: \frac{\lVert\mathbf{v}\rVert^2 - \lVert\mathbf{u}\rVert^2}{k_e \tau
          MA} + k_e \tau MA\le 2L

If that condition failed, then we instead have

.. math:: \cos\theta = -\frac{\sqrt{L^2 - \left( \lVert\mathbf{v}\rVert^2 -
          \lVert\mathbf{u}\rVert^2 \right)}}{\lVert\mathbf{u}\rVert}

Note that we took the negative square root, because :math:`\theta` needs to be
as large as possible so that the curvature of the strafing path is maximised,
which is one of the purposes of speed preserving strafing.  To derive the
necessary condition for the formula above, we again employ the standard
strategy, yielding

.. math:: k_e \tau MA - L > \sqrt{L^2 - \left( \lVert\mathbf{v}\rVert^2 -
          \lVert\mathbf{u}\rVert^2 \right)}

Observe that we need :math:`k_e \tau MA > L` and :math:`L^2 \ge
\lVert\mathbf{v}\rVert^2 - \lVert\mathbf{u}\rVert^2`.  Then we square the
inequality to yield the converse of the condition for :math:`\mu = \gamma_1`,
as expected.  Putting these results together, we obtain

.. math:: \cos\theta =
          \begin{cases}
          \displaystyle \frac{1}{2\lVert\mathbf{u}\rVert} \left(
          \frac{\lVert\mathbf{v}\rVert^2 - \lVert\mathbf{u}\rVert^2}{k_e \tau MA} -
          k_e \tau MA \right) & \displaystyle \text{if } \frac{\lVert\mathbf{v}\rVert^2 -
          \lVert\mathbf{u}\rVert^2}{k_e \tau MA} + k_e \tau MA\le 2L \\
          \displaystyle -\frac{\sqrt{L^2 - \left( \lVert\mathbf{v}\rVert^2 -
          \lVert\mathbf{u}\rVert^2 \right)}}{\lVert\mathbf{u}\rVert} &
          \displaystyle \text{otherwise, if } k_e \tau MA > L \text{ and } L^2 \ge
          \lVert\mathbf{v}\rVert^2 - \lVert\mathbf{u}\rVert^2
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

Passageways in Half-Life commonly bend perpendicularly, so we frequently make 90 degrees turns by strafing. We can imagine how the width of a passage limits the maximum radius of curvature one can sustain without colliding with the walls. This implies that the speed is limited as well. When planning for speedruns, it can prove useful to be able to estimate this limit for a given turn without running a simulation or strafing by hand. In particular, we want to compute the maximum speed for a given passage width. We start by making some simplifying assumptions that will greatly reduce the difficulty of analysis while closely modelling actual situations in practice. Refer to the figure below.

.. figure:: static/90-degrees-strafe-radius.png
   :height: 800px
   :width: 754px
   :scale: 50%
   :align: center

The first assumption we make is that the width of the corridor is the same before and after the turn. This width is denoted as :math:`d`, as one can see in the figure. This assumption is justified because this is often true or approximately true in Half-Life maps. The second assumption is that the path is circular. The centre of this circle, also named the *centre of curvature*, is at point :math:`C`. As noted earlier, the strafing path is in general a spiral with varying radius of curvature. Nevertheless, the total time required to make such a turn is typically very small. Within such short time frame, the radius would not have changed significantly. Therefore it is not absurd to assume that the radius of curvature is constant while making the turn. The third assumption is that the positions of the player before and after making the turn coincide with the walls. This assumption is arguably less realistic, but the resulting path is the larger circular arc one can fit in this space.

By trivial applications of the Pythagorean theorem, it can be shown that the relationship between the radius of curvature :math:`r` and the width of the corridor :math:`d` is given by

.. math:: r = \left( 2 + \sqrt{2} \right) d \approx 3.414 d

This formula may be used to estimate the maximum radius of curvature for making such a turn without collision. However, the radius of curvature by itself is not very useful. We may wish to further estimate the maximum speed corresponding to this :math:`r`.

Radius-speed relationship
~~~~~~~~~~~~~~~~~~~~~~~~~

The following figure depicts the positions of the player at times :math:`t = 0`, :math:`t = \tau` and :math:`t = 2\tau`. The initial speed is :math:`\lVert\mathbf{v}\rVert`. All other symbols have their usual meaning.

.. image:: static/radius-estimate-xy.png
   :height: 775px
   :width: 1135px
   :scale: 50%
   :align: center

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

Implementation notes
--------------------

Vectorial compensation
~~~~~~~~~~~~~~~~~~~~~~
