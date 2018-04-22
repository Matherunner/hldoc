.. FIXME FIXME
   ===================================

   OK There's a problem with this. The way we include xi in the equation and
   epsilon becomes the tiny error (rather than fractional part), makes thing
   very hard to prove. Have to deal with the case that, floor((beta + theta +
   epsilon) / u) may get +1 or -1, and this would mean the assumption that
   tilde{Phi} > Phi may not be true. Just plot the graph of Phi against epsilon,
   and you'll see a saw tooth wave. And you'll see that indeed, when the floor
   gets +1 or -1, Phi becomes wildly off.

   I think it's just easier to ignore xi in the equation, or just write xi =
   qu + r where r is the fractional part. Then we'll find that r = Phi as
   expected, and the xi-table is to find the closest r'.


Movement automation
===================

In this chapter we will discuss a few algorithms or implementations of movement
automation in a typical TAS tool.

Vectorial compensation
----------------------

In :ref:`strafing`, we discussed various ways to "strafe" with differing
objectives, most commonly maximum-acceleration strafing and speed-preserving
strafing. In each of these methods, we must derive a formula or, at least, an
implicit equation for the angle :math:`\theta` between :math:`\mathbf{v}` and
:math:`\mathbf{\hat{a}}` to realise the desired strafing objective.
Unfortunately, Half-Life does not allow us to realise the angles to a very high
precision. This is because Half-life uses the DELTA mechanism (see :ref:`delta`)
to transmit information across the network from client to server and vice versa.
Looking at the default ``delta.lst`` included in vanilla Half-Life, we see the
following line defined under ``usercmd_t``::

  DEFINE_DELTA( viewangles[1], DT_ANGLE, 16, 1.0 ),

This shows that the yaw angle is somehow lossily compressed to 16 bits. This
means that, to transmit some angle :math:`a` in degrees, it is first converted
at the client side to the 16-bit integer representing

.. math:: \operatorname{int}\left( \frac{65536}{360} a \right) =
          \operatorname{int}\left( \frac{a}{u_d} \right)

where :math:`\operatorname{int}(x)` is the integer part of some real number
:math:`x`. When the server receives this integer, it is then converted back to
the floating point number

.. math:: \frac{360}{65536} \left( \operatorname{int}\left( \frac{65536}{360} a
          \right) \mathbin{\mathtt{AND}} 65535 \right)

This expression looks familiar! Indeed, this entire operation is equivalent to
the anglemod function, first described in :ref:`anglemod`. Given our
understanding of anglemod, we know that there are only exactly 65536 possible
angles. Although this is already very precise, in the sense that any angle can
be realised with only about 0.0015% absolute error, it is possible to do better
by controlling the yaw angle :math:`\vartheta` *in combination* with :math:`F`
and :math:`S`.

By controlling :math:`F` and :math:`S`, we can change the direction of the unit
acceleration vector :math:`\mathbf{\hat{a}}` (see :ref:`player air ground`)
without changing the yaw angle. To see why, recall that :math:`\mathbf{a} = F
\mathbf{\hat{f}} + S \mathbf{\hat{s}}`, and even keeping
:math:`\mathbf{\hat{f}}` and :math:`\mathbf{\hat{s}}` constant, we can change
the "weights" :math:`F` and :math:`S` to make the vector sum point to any
desired direction, and therefore realise any angle :math:`\theta` between
:math:`\mathbf{v}` and :math:`\mathbf{\hat{a}}`. Unfortunately, again, looking
at the file ``delta.lst``, we see the following lines::

  DEFINE_DELTA( forwardmove, DT_SIGNED | DT_FLOAT, 12, 1.0 ),
  ...
  DEFINE_DELTA( sidemove, DT_SIGNED | DT_FLOAT, 12, 1.0 ),
  DEFINE_DELTA( upmove, DT_SIGNED | DT_FLOAT, 12, 1.0 ),

Here, the ``12`` indicates that the client side :math:`\tilde{F}`,
:math:`\tilde{S}`, and :math:`\tilde{U}` (see :ref:`FSU` for their definitions)
will be truncated to 12 bits and integer precision. Since :math:`2^{12} = 4096`,
and a signed integer transmitted across the network is *not* represented in
two's complement, each of these values will be clamped to :math:`[-2047, 2047]`.

Nevertheless, despite each of :math:`\vartheta`, :math:`F`, and :math:`S` being
truncated, we can still combine them to obtain a more accurate angle realisation
method than possible using only the yaw or the FSU.

Unconstrained compensation
~~~~~~~~~~~~~~~~~~~~~~~~~~

Suppose we have computed the desired angle :math:`\theta` between the velocity
:math:`\mathbf{v}` and the ideal unit acceleration vector
:math:`\mathbf{\hat{a}}`. To "realise" this angle is to strafe such that the
ideal unit acceleration :math:`\mathbf{\hat{a}}` is attained by changing the
:math:`\vartheta`, :math:`F`, and :math:`S`. However, due to the slight
imprecision in each of these values, the ideal :math:`\mathbf{\hat{a}}` can
never be attained exactly. Instead, we compute the "best" approximation to it,
which may be written as

.. math:: \mathbf{\tilde{\hat{a}}} = \mathbf{\hat{f}} R(\theta)

where :math:`\mathbf{\hat{f}}` is the two dimensional unit forward vector (see
:ref:`view vectors`), and :math:`R(\theta)` is the rotation matrix. We may then
define the "best" approximation such that the angle between
:math:`\mathbf{\hat{a}}` and :math:`\mathbf{\tilde{\hat{a}}}` is minimised. In
the ideal case, the angle between the two vectors is zero, meaning the desired
unit acceleration vector is attained exactly. However, in practice, there will
be a small difference in angle :math:`\epsilon` such that

.. math:: \Pi = \mathbf{\hat{a}} \cdot \mathbf{\tilde{\hat{a}}} = \cos\epsilon

Writing out the dot product and simplifying, we obtain

.. math:: \Pi = a_x \cos(\vartheta + \xi) + a_y \sin(\vartheta + \xi)

where

.. math:: \xi = \operatorname{atan2}(S, F)

Now, to minimise the angle :math:`\epsilon` is to maximise :math:`\cos\epsilon`,
and therefore maximising :math:`\Pi`. We may compute the maximum point of
:math:`\Pi` [#maxpoint]_ by solving

.. math:: \frac{d\Pi}{d(\vartheta + \xi)} = -a_x \sin(\vartheta + \xi) + a_y
          \cos(\vartheta + \xi) = 0

yielding

.. math:: \tan(\vartheta + \xi) = \frac{a_y}{a_x}

Note that :math:`\vartheta = uY` for some integer :math:`Y \in [0, 65535]`.
Inverting the tangent function and computing the remainder when divided by
:math:`u` (i.e. modulo :math:`u`),

.. math:: \xi - \left\lfloor \frac{\xi}{u} \right\rfloor u =
          \operatorname{atan2}(a_y, a_x) - \left\lfloor \frac{1}{u}
          \operatorname{atan2}(a_y, a_x) \right\rfloor u

Notice that the yaw :math:`\vartheta` is gone, and so is the integer yaw
:math:`Y`. This is because the yaw is always divisible by :math:`u`, and
therefore its remainder is always zero. To slightly simplify implementation,
write

.. math:: \frac{\xi}{u} - \left\lfloor \frac{\xi}{u} \right\rfloor = \frac{1}{u}
          \operatorname{atan2}(a_y, a_x) - \left\lfloor \frac{1}{u}
          \operatorname{atan2}(a_y, a_x) \right\rfloor

That is, if this equality is satisfied, then the :math:`\xi` (and an appropriate
:math:`\vartheta`) will maximise :math:`\Pi`, achieving the best approximation.
In practice, however, this equality is *rarely* satisfied, due to the
imprecision in :math:`S` and :math:`F` mentioned previously. Denote

.. math:: \tilde{\Phi} = \frac{\xi}{u} - \left\lfloor \frac{\xi}{u}
          \right\rfloor \qquad \Phi = \frac{1}{u} \operatorname{atan2}(a_y, a_x) -
          \left\lfloor \frac{1}{u} \operatorname{atan2}(a_y, a_x) \right\rfloor
   :label: Phi definition

Then, we want to find a :math:`\tilde{\Phi}` that is the *closest* to
:math:`\Phi`, subject to the constraints that :math:`S` and :math:`F` have. One
way to do this is to brute force every possible combinations of :math:`S` and
:math:`F` and computing the corresponding :math:`\tilde{\Phi}` values. However,
this is very inefficient and can take millions of iterations. Doing it once on a
fast computer may not consume a noticeable amount of time, but when implemented
in game, these computations need to be done *every frame*, and there could be
thousands of frames per second.

A better approach is to build the *vectorial compensation table* (VCT). The
details in how to compute such a table will be described in :ref:`vct
generation`. But here, we will assume that it contains 3-tuples
:math:`(\tilde{\Phi}, F, S)`, *sorted* by :math:`\tilde{\Phi}`, where
:math:`\tilde{\Phi}` is computed using :eq:`Phi definition` using the
corresponding :math:`S` and :math:`F`. To find the closest :math:`\tilde{\Phi}`
to :math:`\Phi`, we may use binary search to find entries corresponding to
:math:`\tilde{\Phi}_1` and :math:`\tilde{\Phi}_2` such that [#phi12]_

.. math:: \tilde{\Phi}_1 \le \Phi \le \tilde{\Phi}_2

Then, the value that is closest to :math:`\Phi` would simply be one of
:math:`\tilde{\Phi}_1` and :math:`\tilde{\Phi}_2`. This algorithm is very fast
because even if the VCT contains millions of entries, it takes at most about 20
iterations to find the two :math:`\tilde{\Phi}` entries. The downside is that
there will be a small but noticeable delay in generating the VCT.

As a side note, an alternative way to compute :math:`\Phi` exists. In practice,
computing :math:`\operatorname{atan2}(a_y, a_x)` may be slightly less efficient,
because obtaining :math:`\mathbf{\hat{a}}` requires computing the rotation
matrix :math:`R(\theta)`, which in turn requires computing :math:`\sin` and
:math:`\cos` along with multiple addition and multiplication operations. An
alternative method involves observing that :math:`a_x = \cos(\beta + \theta)`
and :math:`a_y = \sin(\beta + \theta)`, where

.. math:: \beta = \operatorname{atan2}(v_y, v_x)

Therefore,

.. FIXME FIXME is this + or -?

.. math:: \operatorname{atan2}(a_y, a_x) = \beta + \theta + k\pi

for some integer :math:`k`. This implies that

.. math:: \Phi = \frac{\beta + \theta + k\pi}{u} - \left\lfloor \frac{\beta +
          \theta + k\pi}{u} \right\rfloor = \frac{\beta + \theta}{u} -
          \left\lfloor \frac{\beta + \theta}{u} \right\rfloor

as :math:`u` divides :math:`k\pi`, and so the integer disappears, simplifying
the expression. This method of computing :math:`\Phi` requires only one
trigonometric computation, namely in obtaining :math:`\beta`.

.. rubric:: Footnotes

.. [#maxpoint] To verify that this is a maximum point, compute the second
               derivative and substituting,

               .. math:: \frac{d^2\Pi}{d(\vartheta + \xi)^2} = -a_x
                         \cos(\vartheta + \xi) - a_y \sin(\vartheta + \xi) = -
                         \left( \frac{a_x^2}{\sqrt{a_x^2 + a_y^2}} +
                         \frac{a_y^2}{\sqrt{a_x^2 + a_y^2}} \right)

               which is always negative.

.. [#phi12] A caveat is that when, for instance, :math:`\tilde{\Phi}_1` is
            already the largest :math:`\tilde{\Phi}` value in the VCT, therefore
            no :math:`\tilde{\Phi}_2 > \tilde{\Phi}_1` exists. In this case,
            :math:`\tilde{\Phi}_2` may be chosen to be zero, and appropriate
            :math:`\xi` and :math:`\vartheta` would need to be found separately.
            Vice versa for when :math:`\tilde{\Phi}_2` is already the smallest
            value in the VCT.
..
   Assume all angles are in **radians**. Define 3-tuple input :math:`(Y, F, S)`,
   where :math:`Y` is an integer in the range of :math:`[0, 65535]`, such that

   .. math:: uY = \vartheta, \quad u = \frac{2\pi}{65536} = \frac{\pi}{32768}

   gives the anglemod-truncated yaw angle, and :math:`F` and :math:`S` have their
   usual meaning, except they are integers in :math:`[-2047, 2047]`. The purpose of
   vectorial compensation is to find the best input to realise the desired angle as
   precisely as possible.

   Define an angular quantity representing the "direction" of :math:`F` and
   :math:`S` as such:

   .. math:: \xi = \operatorname{atan2}(S, F)

   Now, notice that :math:`\vartheta - \xi` equals the polar angle of
   :math:`\mathbf{\hat{a}}`, modulo :math:`2\pi`. In other words,

   .. math:: \vartheta - \xi \equiv \operatorname{atan2}(\hat{a}_y, \hat{a}_x) \pmod{2\pi}

   For instance, with only ``+moveright`` we get :math:`S > 0` and :math:`F = 0`,
   which is equivalent to accelerating to the right with :math:`\mathbf{\hat{a}}`
   pointing perpendicularly to the right of the camera view direction. Using the
   definition of :math:`\xi` above, we calculate that :math:`\xi = \pi/2`. And
   indeed, :math:`\vartheta - \pi/2` is exactly the polar angle of
   :math:`\mathbf{\hat{a}}`, modulo :math:`2\pi`.

   Define *velocity yaw* such that

   .. math:: \beta = \operatorname{atan2}(v_y, v_x)

   In order to realise some angle :math:`\theta`, the values :math:`\beta` and
   :math:`\theta` must be known. It can be shown that the following equation must
   be satisfied:

   .. math:: uY + \xi \equiv \beta + \theta + \epsilon \pmod{2\pi}
      :label: vc equation

   where :math:`\epsilon = \tilde{\theta} - \theta` is the deviation of realised
   angle from the desired angle, arising from the imprecision of :math:`\vartheta`
   and :math:`\xi`. Note that we want :math:`\lvert\epsilon\rvert < u`. If
   :math:`\lvert\epsilon\rvert \ge u`, then we can always change :math:`Y` until
   :math:`\lvert\epsilon\rvert < u`. We can now restate the objective of vectorial
   compensation as an attempt to minimise :math:`\epsilon`.

   To minimise this deviation, the simplest way is to search for the best 3-tuple
   :math:`(Y, F, S)` by brute force, and find the input with the smallest
   :math:`\epsilon`. However, this is rather inefficient. Even if we exploit the
   symmetries in :math:`(F, S)`, it would still take several million iterations to
   find the optimal input. This may not take a noticeable amount of time on a very
   fast computer if done just once, but when implemented in the game it must be run
   *every frame*.

   Since :math:`u` divides :math:`2\pi`, we can rewrite :eq:`vc equation` as

   .. math:: \xi \equiv \beta + \theta + \epsilon \pmod{u}

   Observe that the yaw :math:`uY` has disappeared, so we can ignore it for now. We
   may rewrite this congruence relation in equation form as

   .. math:: \frac{\xi}{u} = \frac{\beta + \theta}{u} + \frac{\epsilon}{u} + k

   for some integer :math:`k`. Taking the floor function and subtracting, we
   eliminate :math:`k` and arrive at

   .. math:: \frac{\xi}{u} - \left\lfloor \frac{\xi}{u} \right\rfloor =
             \frac{\beta + \theta}{u} + \frac{\epsilon}{u} - \left\lfloor
             \frac{\beta + \theta}{u} + \frac{\epsilon}{u} \right\rfloor
      :label: xi beta relation

   For convenience, we write

   .. math:: \tilde{\Phi} = \frac{\xi}{u} - \left\lfloor \frac{\xi}{u} \right\rfloor \qquad
             \Phi = \frac{\beta + \theta}{u} - \left\lfloor \frac{\beta + \theta}{u} \right\rfloor
      :label: Phi definition

   Since the input :math:`Y` has disappeared, the only variable we can alter here
   is :math:`\xi`. We can now choose :math:`\xi_1` and :math:`\xi_2` such that the
   corresponding :math:`\tilde{\Phi}_1` and :math:`\tilde{\Phi}_2` are closest to
   :math:`\Phi` and satisfy

   .. math:: \tilde{\Phi}_1 - \Phi < 0 \qquad \tilde{\Phi}_2 - \Phi \ge 0

   To do this efficiently, we can assume the existence of a lookup table, called
   the :math:`\xi`\ -table, which is an array of 3-tuples :math:`(\tilde{\Phi}, F,
   S)`, sorted by :math:`\tilde{\Phi}`, where :math:`\tilde{\Phi}` is computed
   using :eq:`Phi definition` and the corresponding :math:`F` and :math:`S`. To
   find the two closest :math:`\tilde{\Phi}_1` and :math:`\tilde{\Phi}_2`, we
   simply compute :math:`\Phi` using :eq:`Phi definition` given the known
   :math:`\beta` and :math:`\theta`, and perform a binary search on the
   :math:`\xi`\ -table using the computed :math:`\Phi`. Then, :math:`\Phi_1` and
   :math:`\Phi_2` are simply the two elements on the table that contains
   :math:`\tilde{\Phi}_1 \le \Phi \le \tilde{\Phi}_2`. From this, we can obtain the
   corresponding :math:`(F_1, S_1)` and :math:`(F_2, S_2)`. The binary search
   should require only a few iterations. With :math:`\xi_1` and :math:`\xi_2`, we
   can calculate :math:`Y_1`, :math:`Y_2`, :math:`\epsilon_1`, and
   :math:`\epsilon_2`. Then the best input :math:`(Y, F, S)` depends on which of
   the corresponding :math:`\epsilon_1` or :math:`\epsilon_2` is smaller.

   Remember that, the ultimate goal of vectorial compensation, as stated earlier,
   is to minimise the deviation :math:`\epsilon`. Suppose :math:`\tilde{\Phi}` is
   the closest element to :math:`\Phi` (in the sense that
   :math:`\lvert\tilde{\Phi} - \Phi\rvert` is minimal) in the :math:`\xi`\ -table.
   Why does this imply that the corresponding :math:`\lvert\epsilon\rvert` in
   :eq:`xi beta relation` would also be *minimal*? To see why, suppose
   :math:`\lvert\epsilon\rvert` is *not* minimal. Then, there must exist another
   :math:`\tilde{\Phi}'` such that the corresponding :math:`\lvert\epsilon'\rvert`
   satisfies :math:`0 \le \lvert\epsilon'\rvert < \lvert\epsilon\rvert`.

   Now, we can deduce what the sign of :math:`\epsilon` should be. Subtracting
   :math:`\Phi` from :math:`\tilde{\Phi}`,

   .. math:: \tilde{\Phi} - \Phi = \frac{\epsilon}{u}
             - \left( \left\lfloor \frac{\beta + \theta}{u} + \frac{\epsilon}{u}
             \right\rfloor - \left\lfloor \frac{\beta + \theta}{u} \right\rfloor \right)
             = \frac{\epsilon}{u} - A

   Recall that :math:`\lvert\epsilon/u\rvert < 1`. This implies that we can only
   have :math:`A = 1` or :math:`A = 0` if :math:`\epsilon \ge 0`, otherwise
   :math:`A = -1` or :math:`A = 0` if :math:`\epsilon < 0`. We can therefore
   conclude that if :math:`\tilde{\Phi} - \Phi \ge 0`, then either :math:`\epsilon
   \ge 0` and :math:`A = 0`, or :math:`\epsilon < 0` and :math:`A = -1`. On the
   other hand, if :math:`\tilde{\Phi} - \Phi < 0`, then either :math:`\epsilon < 0`
   and :math:`A = 0`, or :math:`\epsilon \ge 0` and :math:`A = 1`.

   From :eq:`xi beta relation`, we have

   .. math::
      \begin{aligned}
      \tilde{\Phi} &= \frac{\beta + \theta}{u} + \frac{\epsilon}{u}
      - \left\lfloor \frac{\beta + \theta}{u} + \frac{\epsilon}{u} \right\rfloor \\
      \tilde{\Phi}' &= \frac{\beta + \theta}{u} + \frac{\epsilon'}{u}
      - \left\lfloor \frac{\beta + \theta}{u} + \frac{\epsilon'}{u} \right\rfloor
      \end{aligned}

   Subtracting :math:`\Phi` from each,

   .. math::
      \begin{aligned}
      \tilde{\Phi} - \Phi &= \frac{\epsilon}{u}
      - \left( \left\lfloor \frac{\beta + \theta}{u} + \frac{\epsilon}{u}
      \right\rfloor - \left\lfloor \frac{\beta + \theta}{u} \right\rfloor \right) \\
      \tilde{\Phi}' - \Phi &= \frac{\epsilon'}{u}
      - \left( \left\lfloor \frac{\beta + \theta}{u} + \frac{\epsilon'}{u} \right\rfloor
      - \left\lfloor \frac{\beta + \theta}{u} \right\rfloor \right)
      \end{aligned}

   Assuming :math:`\tilde{\Phi} - \Phi \ge 0`. Then there are four possible cases:

   1. :math:`\epsilon \ge 0` and :math:`\epsilon' \ge 0`
   2. :math:`\epsilon \ge 0` and :math:`\epsilon' < 0`
   3. :math:`\epsilon < 0` and :math:`\epsilon' \ge 0`
   4. :math:`\epsilon < 0` and :math:`\epsilon' < 0`


   .. math:: \tilde{\Phi}' - \tilde{\Phi} = \frac{\epsilon - \epsilon'}{u}
             - \left( \left\lfloor \frac{\beta + \theta}{u} + \frac{\epsilon}{u} \right\rfloor
               - \left\lfloor \frac{\beta + \theta}{u} + \frac{\epsilon'}{u} \right\rfloor
                 \right)

   Then, obviously :math:`\epsilon - \epsilon'`

   TODO

.. _vct generation:

VCT generation
~~~~~~~~~~~~~~

The algorithm described in previous sections rely on a lookup table called the
vectorial compensation table (VCT). As a reminder, this is a table containing
entries of 3-tuple :math:`(\tilde{\Phi}, F, S)` sorted by :math:`\tilde{\Phi}`,
and that each entry must have a *unique* :math:`Y` and must satisfy :math:`F^2 +
S^2 \ge M_m^2`.

If we simply enumerate :math:`F` and :math:`S` by drawing each element from
:math:`[-2047, 2047]`, then the resulting :math:`\tilde{\Phi}` will not be
unique. So see why, suppose :math:`M_m = 320`, :math:`(F_1, S_1) = (400, 800)`,
and :math:`(F_2, S_2) = (800, 1600)`. Then, obviously :math:`F_1^2 + S_1^2 >
M_m^2` and :math:`F_2^2 + S_2^2 > M_m^2`, but :math:`\xi_1 = \xi_2` and
therefore :math:`\tilde{\Phi}_1 = \tilde{\Phi_2}`.

To obtain a set of unique :math:`\tilde{\Phi}`, we must therefore enumerate all
*unique* coprime pairs :math:`(F, S)`, but satisfying the constraint that
:math:`-2047 \le F,S \le 2047` and :math:`F^2 + S^2 \ge M_m^2`. The most
efficient way to enumerate this is by generating a Farey sequence. To reduce the
generation time, we can exploit symmetries in :math:`(F,S)`.

Firstly, we can restrict generation in just one quadrant, namely by considering
only positive :math:`F` and :math:`S`. This is because for all :math:`F` and
:math:`S`, we know that

.. math:: \xi = \operatorname{atan2}(S,F)
          = \operatorname{atan2}(\lvert S\rvert, \lvert F\rvert)
          + \frac{\pi}{2} k

for some integer :math:`k`. Computing the :math:`\tilde{\Phi}`,

.. math:: \tilde{\Phi}
          = \frac{\xi}{u} - \left\lfloor \frac{\xi}{u} \right\rfloor
          = \frac{\operatorname{atan2}(\lvert S\rvert, \lvert F\rvert)}{u} + 16384k
          - \left\lfloor \frac{\operatorname{atan2}(\lvert S\rvert, \lvert F\rvert)}{u} + 16384k \right\rfloor

Obviously :math:`16384k \in \mathbb{Z}`, therefore this simplifies to

.. math:: \frac{\operatorname{atan2}(\lvert S\rvert, \lvert F\rvert)}{u}
          - \left\lfloor \frac{\operatorname{atan2}(\lvert S\rvert, \lvert F\rvert)}{u} \right\rfloor
          = \frac{\operatorname{atan2}(S, F)}{u} - \left\lfloor \frac{\operatorname{atan2}(S,F)}{u} \right\rfloor

This implies that the :math:`\tilde{\Phi}`\ s computed from :math:`(F,S)` and
:math:`(\lvert F\rvert, \lvert S\rvert)` are the same.

Within a quadrant, we only need to consider :math:`\xi` in :math:`[0, \pi/4)`.
In other words, we only need to generate values within an octant. To see this,
define sets

.. math::
   U = \left\{ \tilde{\Phi}(\xi) \;\middle|\; 0 \le \xi < \frac{\pi}{4} \right\} \qquad
   V = \left\{ \tilde{\Phi}(\xi) \;\middle|\; \frac{\pi}{4} \le \xi < \frac{\pi}{2} \right\}

Then we claim that :math:`U = V`, and therefore only one of them needs to be
computed. Consider :math:`\xi \in [0, \pi/4)` in the domain of :math:`U`. Then
clearly :math:`\xi + \pi/4 \in [\pi/4, \pi/2)`, which is the domain of
:math:`V`. Compute the corresponding :math:`\tilde{\Phi}`, we have

.. math:: \frac{\xi}{u} + 8192 - \left\lfloor
          \frac{\xi}{u} + 8192 \right\rfloor
          = \frac{\xi}{u} - \left\lfloor \frac{\xi}{u} \right\rfloor

This implies that :math:`U \subseteq V`. Similarly, consider :math:`\xi' \in
[\pi/4, \pi/2)` in the domain of :math:`V`, then :math:`\xi' - \pi/4 \in [0,
\pi/4)` is in the domain of :math:`U`. It can be similarly shown that the
:math:`\tilde{\Phi}`\ s computed using :math:`\xi'` and :math:`\xi' - \pi/4` are
the same. This shows :math:`V \subseteq U`, and we conclude that :math:`U = V`.

One observation may be made regarding the relationship between different
elements in the :math:`\xi`\ -table. Define sets

.. math:: P = \left\{ \tilde{\Phi}(\xi) \;\middle|\; 0 \le \xi < \frac{\pi}{8} \right\} \qquad
          Q = \left\{ \tilde{\Phi}(\xi) \;\middle|\; \frac{\pi}{8} \le \xi < \frac{\pi}{4} \right\}

Consider some :math:`0 \le \xi < \pi/8`. Then, we have

.. math:: \tan\left( \frac{\pi}{4} - \arctan\frac{S}{F} \right)
          = \frac{1 - S/F}{1 + S/F} = \frac{F - S}{F + S}

Computing :math:`\arctan`,

.. math:: \frac{\pi}{4} - \xi = \frac{\pi}{4} - \arctan\frac{S}{F} = \arctan\frac{F - S}{F + S}
          = \arctan\frac{S'}{F'} = \xi'

Let :math:`\xi` such that :math:`\tilde{\Phi}(\xi) \in P`. Let integers :math:`p
= kS'` and :math:`q = kF'` for some :math:`k`, where :math:`\gcd(p,q) = 1`.
Namely, :math:`p/q` is the completely reduced fraction of :math:`S'/F'`. Then if
:math:`q \le 2047` is satisfied, we have :math:`\tilde{\Phi}(\xi') \in Q`. In
addition, we also have

.. math:: \tilde{\Phi}' = \left\lceil \frac{\xi}{u} \right\rceil - \frac{\xi}{u}

Line strafing
-------------

Automatic actions
-----------------
