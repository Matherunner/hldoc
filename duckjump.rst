Ducking and jumping
===================

Ducking and jumping are some of the fundamental player actions. Understanding the intricacies associated with these actions is vital to writing an effecting TAS and troubleshooting issues that might arise along the way.

Ducking
-------

Ducking is one of the most important actions in playing Half-Life. And yet, it has some of the more misunderstood behaviours. Ducking can be performed with the use of the duck key, which issues ``+duck``. The subsequent behaviour depends on whether the player is onground, and how long the duck key is held before releasing.

There are three ducking states in Half-Life, namely *standing*, *in-duck*, and *ducked*. The *standing* state is simply the player's default state, when the duck key is not held. In this state, the player bounding box is set to be 72 units tall. The *in-duck* state refers to the transitional state between the standing and ducked states. Lastly, the *ducked* state is when the player is fully ducked, with a bounding box of 36 units height. The standing and ducked states are relatively straightforward, but what happens in the in-duck state is less obvious and potentially misleading.

Suppose the player presses the duck key. Suppose also the player is onground. The ducking state will instantly transition from standing to in-duck. As a result, the game will start a countdown of 0.4 seconds. Meanwhile, the game will begin to slowly animate the player vertical view offset downwards. This can be observed in-game as the camera position seemingly easing downwards when ducking. However, this is misleading: the player hull size has not changed thus far, and the height remains at 72 units throughout. Only when the 0.4 seconds time is up the game will set the ducking state to *ducked* and instantaneously set the hull height to 36 units. And only in the *following frame* does the FSU values get scaled down by a factor of 0.333 (see :ref:`FSU`). As long as the duck key is still being held, the ducking state will remain unchanged no matter what situation the player is in, and no matter how long.

On the other hand, if the player is not onground (in the air), then the game will skip the in-duck state entirely, and transition immediately to the ducked state. This means that changing hull size is instantaneously as long as the player is in the air. This allows for very quick responses when navigating around narrow terrains. For example, the player can duck in the air to immediately dodge an obstructing object. Again, the FSU values will only get scaled down in the following frame.

Now let us backtrack and assume the player is onground. What if the player releases the duck key before the 0.4 seconds is up? The game will attempt to unduck. If the player is onground, the game will consider the location 18 units above the current player position, and the game will begin player tracing from the current position to 18 units above, taking the player hull size into account (72 units height in this case). If the area 18 units above the player is clear, then the unducking process is considered successful, and the player position will be instantaneously set to 18 units above the ground. This is peculiar behaviour forms the foundation of ducktapping (see :ref:`ducktapping`).

Duckbug
~~~~~~~

The duckbug is one of the many ways of cancelling fall damage.

.. _ducktapping:

Ducktapping
~~~~~~~~~~~

.. _jumping:

Jumping
-------

When the jump bit is set, the player will jump. To be precise, the act of jumping refers to setting the vertical velocity to

.. math:: v_z = \sqrt{2 \cdot 800 \cdot 45} = 120 \sqrt{5} \approx 268.3

The unsimplified expression for the vertical velocity is how it is calculated in the code. It implies the intention of jumping to the height of 45 units with :math:`g = 800`, though all of the numbers are hardcoded constants independent of any game variables.

The condition of jumping is being onground.

.. _jumpbug:

Jumpbug
~~~~~~~

.. note:: TODO: explain what onground, position categorisation means

Fall damage is computed after the player movement functions based on the condition that, *within a frame*, the player is not onground (i.e. in the air) after the very first position categorisation in ``PM_PlayerMove`` and that the player is onground after the final position categorisation in the same function. It is possible for the player position to change momentarily to something else between the two. For example, the player could be in the air before *and* after, but onground some point in the middle. This is the loophole that allows jumpbug to work.

Assuming the player is in the air at the first position categorisation and falling towards the ground. The exact vertical velocity does not matter as long as it is negative or below 180. Observe that there is a position categorisation step at the end of ``PM_UnDuck``, which is only called by ``PM_Duck`` when the player attempts to unduck. Suppose the player duck state is *ducked* in the air, and crucially, *would* become onground after unducking due to the position categorisation in ``PM_UnDuck``. This condition will be met if the player position (i.e. the position of the centre point of the player's bounding box) is between 36 to 38 units above the ground when the unducking is done, *and* the vertical velocity is below 180. [#poscalc]_ If these conditions are met, and if the player now unducks, the player will be considered onground at the end of ``PM_UnDuck``. As a result, the subsequent player physics will be run with that assumption.

As explained in :ref:`jumping`, a player is allowed to jump only if the player is onground at the moment when ``PM_Jump`` is called. Therefore, if the player is onground after ``PM_UnDuck``, the player will be allowed to jump, regardless of what happened before unducking! By jumping, the vertical velocity will be set to the positive value given in :ref:`jumping`. Since this value is larger than the 180 ups limit for being onground, the final position categorisation (occurs after ``PM_WalkMove`` or ``PM_AirMove``) will consider the player to be in the air again. As a result, the game sees the player as being in the air before *and* after, and thus the fall damage will be completely bypassed.

The criteria for jumpbug is extremely stringent. There is a mere 2 units window for jumpbug to work. Therefore, the frame rate plays a significant role in enabling jumpbug. The higher the frame rate, the smaller the difference between player positions before and after a frame, and therefore more likely to hit the 2 units window. The exact frame rate needed depends on the height and initial falling speed.

.. rubric:: Footnotes

.. [#poscalc] The bottom position is half the height of the player's bounding box below the centre position. The height of the bounding box is 72 units, therefore half the height is 36 units. On the other hand, one condition for being onground is that the bottom of the player's bounding box lies within 2 units above the ground. It follows that the centre position must be between 36 and 38 units above the ground.

.. _duckjump:

Duckjump
~~~~~~~~

.. TODO model animation

Bunnyhop cap
~~~~~~~~~~~~
