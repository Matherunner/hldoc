Func entities
=============

func_pushable
-------------

Object manoeuvre
~~~~~~~~~~~~~~~~

Let :math:`V` the value of ``sv_maxvelocity``.  Define

.. math:: \operatorname{clip}(\mathbf{v}) := \left[ \min(v_x, V), \min(v_y, V), \min(v_z, V) \right]

which is basically ``PM_CheckVelocity``.  Assuming the player is not
accelerating, :math:`\lVert\mathbf{v}\rVert > E` and the use key is pressed
then with :math:`\mathbf{\tilde{v}}_0 = \mathbf{v}_0` the subsequence player
velocities :math:`\mathbf{v}_k` and object velocities :math:`\mathbf{u}_k` is
given by

.. math:: \begin{align*}
          \mathbf{v}_{k+1} &= (1 - k\tau) \operatorname{clip}(0.3\mathbf{\tilde{v}}_k) \\
          \mathbf{\tilde{v}}_{k+1} &= \mathbf{u}_k + \mathbf{v}_k \\
          \mathbf{u}_{k+1} &= (1 - k\tau) \operatorname{clip}(0.3\mathbf{\tilde{v}}_{k+1})
          \end{align*}

The physics of object boosting is well understood with trivial implementation.
A trickier technique is fast object manoeuvre, which is the act of "bringing"
an object with the player at extreme speed for a relatively long duration.

The general idea is to repeatedly activate ``+use`` for just one frame then
deactive it for subsequent :math:`n` frames while pulling an object.  Observe
that when ``+use`` is active the player velocity will be reduced significantly.
And yet, when ``+use`` is deactivated, the player velocity will be equal to the
object velocity, which may well be moving very fast.  The player will then
continue to experience friction.

One important note to make is that despite the player velocity being scaled
down by 0.3 when ``+use`` is active, the object velocity will actually increase
in magnitude.  An implication of this is that the object will gradually
overtake the player, until it goes out of the player's use radius.  To put it
another way, we say that the *mean* object speed is greater than the mean
player speed.  To control the mean player speed, :math:`n` must be adjusted.
If :math:`n` is too low or too high, the mean player speed will be very low.
Therefore there must exist an optimal :math:`n` at which the mean player speed
is maximised.

However, we do not often use the optimal :math:`n` when carrying out this
trick.  Instead, we would use the smallest possible :math:`n` so that the
object mean speed will be as high as possible while ensuring the object stays
within the use radius.  This means the object will hit an obstruction as soon
as possible, so that we can change direction as soon as that happens.

func_breakable
--------------


Item duplication
~~~~~~~~~~~~~~~~

Box item duplication is a trick useful for duplicating items dropped by crates.
To perform this trick, we simply fire a shotgun simultaneously at two adjacent
crates, one of which is explosive and the other will spawn the desired item
upon destruction.  Consequently, the desired item will be duplicated.  It seems
straightforward to understand how this trick works: the crate in question
breaks twice due to damages inflicted simultanously by the explosive crate and
the shotgun pellets.  Such explanation implies that any type of simultaneous
damages inflicted in the same frame can trigger the glitch.  Unfortunately,
this is false.  For instance, if we shoot the crate while a hand grenade
explodes in the same frame, the box items will not be duplicated.

.. TODO: rephrase

We can now make use of the knowledge we learnt above to understand how the
trick works.  Suppose we have two crates, one explosive and the other carrying
the desired item.  To perform the trick we fire the shotgun so that both crates
are simultaneously broken.  First of all, ``FireBulletsPlayer`` will be called.
The ``ClearMultiDamage`` at the beginning of the function ensures that any
leftover multidamage will not interfere with our current situation.  Suppose
the first few pellets strike the explosive crate.  For each of these pellets,
``TraceAttack`` is being called on the explosive crate.  This in turns call
``AddMultiDamage`` which accumulates the damage dealt to the explosive crate.
Suppose now the loop comes to a pellet that is set to deal damage on the
desired crate.  As a result, ``TraceAttack`` and so ``AddMultiDamage`` is
called on the desired crate, which is a *different entity* than the explosive
crate.  Since the desired crate is not the same as ``gMultiDamage->pEntity``,
``AddMultiDamage`` will call ``ApplyMultiDamage`` to inflict the accumulated
damage against the explosive crate.  This is the moment where the explosive
crate explodes.

The explosive crate calls ``RadiusDamage`` which in turn inflicts damage onto
the desired crate.  When this happens, the ``TakeDamage`` associated with the
desired crate will be called, which causes the associated item to spawn.  The
desired crate now turns into ``SOLID_NOT``.  Once ``RadiusDamage`` returns, we
go back to the last ``AddMultiDamage`` call mentioned in the previous
paragraph.  Here, ``gMultiDamage->pEntity`` will be made to point to the
desired crate, and the damage for the current pellet will be assigned to
``gMultiDamage->amount``.

Remember the ``FireBulletsPlayer`` at the beginning of this series of events?
The loop in this function will continue to iterate.  However, since the desired
crate is of ``SOLID_NOT`` type, the tracing functions will completely miss the
crate.  In other words, the rest of the shotgun pellets will not hit the
desired crate, and that in total only one pellet hits the crate.  When the loop
finally completes, the final ``ApplyMultiDamage`` then inflicts the damage
dealt by the one pellet onto the desired crate.  Since ``ApplyMultiDamage``
does not rely on tracing functions to determine the target entity, but rather,
it uses ``gMultiDamage->pEntity`` set a moment ago, the damage will be
successfully inflicted which triggers the second ``TakeDamage`` call for the
desired crate.  This will again causes it to spawn the associated item.

One assumption we made in the description above is that the loop in
``FireBulletsPlayer`` breaks the explosion crate first.  If this is not the
case, then the item will not be duplicated.  To see this, notice that the
desired crate becomes ``SOLID_NOT`` as soon as the first set of pellets breaks
it, which causes the later explosion to miss the crate.

So why does shooting the target crate when a grenade explodes not work?  To see
this, suppose the grenade explodes first.  The grenade will call
``RadiusDamage`` to inflict blast damage onto the target crate.  After that,
the crate becomes ``SOLID_NOT``.  The bullets will therefore miss the crate.
On the other hand, suppose the bullets hit the crate first.  The crate will
then break and becomes ``SOLID_NOT`` again.  When the grenade later calls
``RadiusDamage``, the tracing functions within ``RadiusDamage`` will again miss
the crate.

To put it simply, this trick does not work in cases like this because usually
there is no way for the second damage to find the crate, since they depend on
tracing functions and they do not save the pointer to the desired crate
*before* the crate becomes ``SOLID_NOT``.

func_rotating
-------------


