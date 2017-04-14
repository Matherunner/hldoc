Ducking and jumping
===================

Ducking
-------

Duckbug
~~~~~~~

Ducktapping
~~~~~~~~~~~

Jumping
-------

When the jump bit is set, the player will jump. To be precise, the act of jumping refers to setting the vertical velocity to

.. math:: v_z = \sqrt{2 \cdot 800 \cdot 45} = 120 \sqrt{5} \approx 268.3

The unsimplified expression for the vertical velocity is how it is calculated in the code. It implies the intention of jumping to the height of 45 units with :math:`g = 800`, though all of the numbers are hardcoded constants independent of any game variables.

The condition of jumping is being onground.

.. _jumpbug:

Jumpbug
~~~~~~~

.. _duckjump:

Duckjump
~~~~~~~~

.. TODO model animation

Bunnyhop cap
~~~~~~~~~~~~
