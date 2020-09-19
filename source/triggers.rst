Triggers
========

Triggers are one of the most important entities in Half-Life. They are hidden in
plain sight, literally. A trigger typically has a BSP model associated with it,
though some map or modding tools such as the `Vluzacn's map compile tools
<https://forums.svencoop.com/forumdisplay.php/217-Vluzacn-s-Map-Compile-Tools>`_
removes the associated BSP model. If the associated model is present, then they
can be made visible in a speedrunning mod to make planning and routing easier.

.. figure:: images/triggers-c3a2c.jpg

   trigger_once and trigger_hurt in c3a2c displayed using a custom mod.

Mechanism
---------

A trigger entity usually has solid type ``SOLID_TRIGGER``. Solids of this type
do not get "touched" by conventional means where a line tracing of some sort is
done to check if the line intersects with them. Instead, these trigger entities
are maintained in a BSP tree called "area nodes", pointed to by the
``sv_areanodes`` global variable in the engine library. They are placed there by
calling ``SV_LinkEdict`` with each of them as the first argument somewhere at
the beginning of a level load. In every subsequent frame, ``SV_LinkEdict`` is
called with the player entity as the argument at some point, which causes
``SV_TouchLinks`` to get called if the second argument is set to true.

The ``SV_TouchLinks`` function walks through each of the triggers stored in the
area nodes, and checks if the player intersects with the model using hull
information. If the player and the trigger intersects, then ``DispatchTouch`` in
the game library will get called, which in turn calls the ``Touch`` member
function of the trigger in question. The ``Touch`` function then runs whatever
logic specific to the trigger type.

Some triggers, such as trigger_once, may get removed after touching, though not
immediately. Typically a trigger is scheduled to be removed after 0.1 seconds.
The reason for this delay may be illustrated by this comment in
``CBaseTrigger::ActivateMultiTrigger``:

.. code-block:: c++

   // we can't just remove (self) here, because this is a touch function
   // called while C code is looping through area links...
   SetTouch( NULL );
   pev->nextthink = gpGlobals->time + 0.1;
   SetThink(  &CBaseTrigger::SUB_Remove );

In other words, the delay is likely to prevent a crash as ``SV_TouchLinks`` is
traversing the area nodes and holding a reference to the trigger.

Base trigger
------------

The base trigger refers to the base class from which all other trigger types are
inherited. Two important properties associated with a trigger that are not so
obvious are the *delay on activation* and the *delay after use*. The property
names of these values are ``delay`` and ``wait`` respectively. The ``delay``
property is read by the superclass ``CBaseDelay`` and ``wait`` is read from
``CBaseToggle``.

trigger_multiple
----------------

This type of trigger is typically used for actions that can be triggered
multiple times. When triggered, the assigned target will be fired using
``SUB_UseTargets``. For this trigger, the delays on activation or after use
properties are important to know if hitting the trigger is important in
progressing in the run. For example, sometimes a trigger_multiple in front of a
door is activated or enabled only after something other action has been done.
This means that standing in the trigger area can result in premature firing even
before the trigger has been activated. When the trigger finally activates, the
delay after use can cause the trigger is not fire immediately, thus wasting
crucial time. To avoid this issue, we should avoid touching trigger_multiple
prematurely until we are sure they have been activated. And of course, this
requires knowing precisely when the trigger activates.

trigger_changelevel
-------------------

.. _trigger_push:

trigger_push
------------

A push trigger or a push field is associated with a basevelocity :math:`\mathbf{b}_p` set by the map designer. It imparts :math:`\mathbf{b}_p` onto the velocity of each of the entities that touches it, provided the entities in question satisfy certain conditions written in ``CTriggerPush::Touch`` in the Half-Life SDK. The push trigger also sets the ``FL_BASEVELOCITY`` flag in the entities it touches.

If the touching entities satisfy the necessary conditions, the behaviour differs slightly depending on the spawn flags of the trigger. Let :math:`\mathbf{v}` be the velocity of a touching entity. If ``SF_TRIG_PUSH_ONCE`` is set, then we have

.. math:: \mathbf{v} \gets \mathbf{v} + \mathbf{b}_p

Then, the push trigger will remove itself.

On the other hand, if ``SF_TRIG_PUSH_ONCE`` is not set, then if ``FL_BASEVELOCITY`` is set in the flags of the entity, the new velocity is given by

.. math:: \mathbf{b} \gets \mathbf{b} + \mathbf{b}_p

where :math:`\mathbf{b}` is the current basevelocity of the entity. If ``FL_BASEVELOCITY`` is not set for the entity, then we instead have

.. math:: \mathbf{b} \gets \mathbf{b}_p

Subsequently, the ``FL_BASEVELOCITY`` flag will be set for the entity, which is important for the player entity.

Boosting by rapid touching
~~~~~~~~~~~~~~~~~~~~~~~~~~

There exists a function in the closed source engine code, ``SV_CheckMovingGround``, which is called unconditionally before all of player physics. At a high level, this function modifies the player velocity and/or basevelocity depending on various conditions. One such condition is when the player stands on a conveyor belt, which is described in :ref:`func_conveyor`. Another condition is when the ``FL_BASEVELOCITY`` flag is *not* set in the player entity. In this case, the player velocity and basevelocity will be modified to be

.. math::
   \begin{aligned}
   \mathbf{v} &\gets \mathbf{v} + \left( 1 + \frac{1}{2} \tau_p \right) \mathbf{b} \\
   \mathbf{b} &\gets \mathbf{0}
   \end{aligned}
   :label: player basevelocity exit

Equation :eq:`player basevelocity exit` may be referred to as the *basevelocity exit equation*. One frame after the player exits a push field (or any entity that imparts a basevelocity), the ``FL_BASEVELOCITY`` flag will no longer be set by the ``trigger_push``. Since this flag is always reset every frame, :eq:`player basevelocity exit` will be invoked in the beginning of the next frame. If the player is able to repeatedly enter and leave a push trigger, the basevelocity will be added to the player velocity rapidly, resulting in a massive acceleration. This has been used to great effect in many Half-Life speedruns, typically achieved by ducking and unducking rapidly above a ``trigger_push``, which changes the player hull repeatedly (see :ref:`ducking`). If the ducking and unducking sequence is done at an extremely high frame rate, the resulting acceleration is one of the highest possible in the game.

trigger_hurt
------------

The hurt trigger applies damage to entities that touch it. A hurt trigger always
has a delay of half a second after it damages some entity.
