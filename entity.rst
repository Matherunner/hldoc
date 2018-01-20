.. _entities:

Entities
========

.. TODO: entities get removed if moving too fast

For a more in-depth descriptions of specific entities, refer to

Basic properties
----------------

Camera
------

Not all entities can see, but for those that do, the eyes are the windows to the soul. In the Half-Life universe, an entity is called the *camera* or the *view*. The camera is located at a fixed position relative to the entity's origin, at least at server side. At client side, the player's camera position is slightly complicated by view bobbing if enabled.

.. TODO: origin, velocity, body target, etc

Movement
--------

.. TODO: how position, velocity is stepped through time

Gravity
-------

.. TODO: player gravity is computed differently, with leapfrog integration

.. _friction:

Friction
--------

Hitboxes
--------

.. TODO: hitboxes briefly but refer reader to damage chapter

.. _collision:

Collision
---------

Many entities in Half-Life collide with one another.  The velocity of the
colliding entity usually changes as a result, while the position and velocity
of the entity receiving the collision usually stay constant, countering real
world Newtonian physics.  The process of changing the velocity is usually
referred to as *velocity clipping*.  Collision is one of the most common events
in Half-Life, so it is worthwhile to study its physics.

Collision is detected by determining the planes that run into the way of a line
traced from the moving entity's position to the future position.  The future
position depends on the frame rate, the velocity and the base velocity
associated with the colliding entity.  Let :math:`\mathbf{\hat{n}}` be the
plane normal and let :math:`\mathbf{v}` be the velocity at the instant of
collision.  Let :math:`b` be the *bounce coefficient* which, under certain
conditions, depends on ``sv_bounce`` (denoted as :math:`B`) and :math:`k_e`
(see :ref:`friction`).  The bounce coefficient controls how the velocity is
reflected akin to a light ray.  If :math:`\mathbf{v}'` is the velocity
resulting from the collision, then the *general collision equation* (GCE) can
be written as

.. math:: \mathbf{v}' = \mathbf{v} - b (\mathbf{v} \cdot \mathbf{\hat{n}})
          \mathbf{\hat{n}}

Before we proceed, we must point out that this equation may be applied multiple
times per frame.  The functions responsible of actually displacing entities are
``SV_FlyMove`` for non-players and ``PM_FlyMove`` for players.  These functions
perform at most four aforementioned line tracing, each time potentially calling
the velocity clipping function.

In most cases, players have :math:`b = 1` because :math:`k_e = 1` and so is
:math:`B`.  In general, :math:`b` for players is computed by :math:`b = 1 + B
(1 - k_e)`.  The case of :math:`b \ne 1` is more common for other entities.
For example, snarks have :math:`b = 3/2` and :math:`k_e = 1/2`.  In general, if
the movement type of an entity is designated as ``MOVETYPE_BOUNCE``, then
:math:`b = 2 - k_e`.

Care must be taken when :math:`b < 1`.  To understand why, we first observe
that :math:`\mathbf{v} \cdot \mathbf{\hat{n}} < 0`, because otherwise there
would not be any collision events.  With

.. math:: \mathbf{v}' \cdot \mathbf{\hat{n}} = (1 - b) \mathbf{v} \cdot
          \mathbf{\hat{n}}

we see that if :math:`b < 1` then the angle between the resultant velocity and
the plane normal is obtuse.  As a result, collisions will occur indefinitely
with an increasing :math:`\mathbf{v}`.  To prevent this, the game utilises a
safeguard immediately after the line tracing process in the respective
``FlyMove`` functions to set :math:`\mathbf{v}' = \mathbf{0}`.

Hence, assuming :math:`b \ge 1` we employ the following trick to quickly find
:math:`\lVert\mathbf{v}'\rVert`: write :math:`\lVert\mathbf{v}'\rVert^2 =
\mathbf{v}' \cdot \mathbf{v}'` and expanding each :math:`\mathbf{v}'` in the
RHS to give

.. math:: \lVert\mathbf{v}'\rVert = \lVert\mathbf{v}\rVert \sqrt{1 - b(2 - b)
          \cos^2 \alpha}

where :math:`\alpha` is the *smallest* angle between :math:`\mathbf{v}` and
:math:`\mathbf{\hat{n}}` confined to :math:`[-\pi/2, \pi/2]`.  Observe that the
resulting speed is strictly increasing with respect to :math:`b` in :math:`[1,
\infty)`.  In fact, the curve of resultant speed against :math:`b` is
hyperbolic provided :math:`\alpha \ne 0` and :math:`\alpha \ne \pm\pi/2`.  When
:math:`\alpha` does equal zero, the resultant speed will be linear in :math:`b`
like so:

.. math:: \lVert\mathbf{v}'\rVert = \lVert\mathbf{v}\rVert (b - 1)

Again, this result assumes :math:`b \ge 1`.  On the other hand, for the very
common case of :math:`b = 1` we have

.. math:: \lVert\mathbf{v}'\rVert = \lVert\mathbf{v}\rVert \,
          \lvert\sin\alpha\rvert

Observe that the resultant velocity is always parallel to the plane, as one can
verify that :math:`\mathbf{v}' \cdot \mathbf{\hat{n}} = 0` is indeed true.

Speed preserving circular walls
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In Half-Life we can sometimes find concave walls made out of multiple planes to
approximate an arc.  Examples can be found in the ``c2a1`` map.  Circular walls
can be a blessing for speedrunners because they allow making sharp turns
without losing too much speed.  In fact, if the number of planes increases, the
approximation will improve, and so the speed loss will decrease.  Let :math:`n`
be the number of walls and let :math:`\beta` be the angle subtended by the arc
joining the midpoints of every wall.  For example, with :math:`\beta = \pi/2`
the first and the last walls will be perpendicular, and with :math:`\beta =
\pi` the they will be opposite and parallel instead.  Let :math:`\mathbf{v}_i`
be the velocity immediately after colliding with the :math:`i`-th wall, and
assuming :math:`\mathbf{v}_0` is parallel to and coincident with the first
wall.  Assume also that :math:`0 \le \beta / (n-1) \le \pi/2`, which means that
the angle between adjacent planes cannot be acute.  If the velocity does not
change due to other external factors throughout the collisions, then

.. math:: \lVert\mathbf{v}_{i+1}\rVert = \lVert\mathbf{v}_i\rVert \cos \left(
          \frac{\beta}{n - 1} \right)

The general equation is simply

.. math:: \lVert\mathbf{v}_n\rVert = \lVert\mathbf{v}_0\rVert \cos^{n-1} \left(
          \frac{\beta}{n-1} \right)

It can be verified that :math:`\lim_{n \to \infty} \lVert\mathbf{v}_n\rVert =
\lVert\mathbf{v}_0\rVert`, hence the speed preserving property of circular
walls.  Observe also that the final speed is completely independent of the
radius of the arc.  Perfectly circular walls are impossible in Half-Life due to
the inherent limitations in the map format, so some amount of speed loss is
unavoidable.  Nevertheless, even with :math:`n = 3` and :math:`\beta = \pi/2`
we can still preserve half of the original speed.
