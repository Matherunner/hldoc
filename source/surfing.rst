Surfing and wallstrafing
========================

Surfing is a very specialised technique in Half-Life that is crucial in *surf maps*. The act of surfing involves accelerating against a sloped wall, thereby allowing some control over the vertical position of the player that is not possible by pure strafing alone. On the other hand, wallstrafing refers to the act of accelerating against a vertical wall, ideally with as much horizontal acceleration as possible.

While these two techniques are seemingly different, at least in their objectives, wallstrafing can be considered a degenerative case where the wall is perfectly vertical rather than sloped. The techniques for analysis is somewhat similar for the two cases, at least for the simplest cases, therefore we will discuss the two techniques in the same chapter.

.. TODO: Note, however, that surfing is a very complex phenomena with no elegant analytical solutions. Except for the simplest cases, a global optimisation algorithm must be used for computing the strafe angles :math:`\theta` in each frame. The simulations may need to be done offline and not in-game, the latter of which is dramatically slower, due to the intense computational resources required.

Wallstrafing
------------

.. note:: TODO: reword

The collision equation is

.. math:: \mathbf{v}_c = \mathbf{v}' - b (\mathbf{v}' \cdot \mathbf{\hat{n}}) \mathbf{\hat{n}}

where :math:`\mathbf{v}'` is the velocity produced by the FME. Assuming :math:`b = 1`, the speed is given by

.. math:: \lVert\mathbf{v}_c\rVert^2 = \mathbf{v}_c \cdot \mathbf{v}_c = \lVert\mathbf{v}'\rVert^2 - (\mathbf{v}' \cdot \mathbf{\hat{n}})^2

On the other hand, from the FME we have

.. math:: \mathbf{v}' = \mathbf{v} + \mu\mathbf{\hat{v}} R(\theta)

where :math:`R(\theta)` is the rotation matrix. Performing dot product with the plane normal :math:`\mathbf{\hat{n}}` gives

.. math:: \mathbf{v}' \cdot \mathbf{\hat{n}} = \mathbf{v} \cdot \mathbf{\hat{n}} + \mu \mathbf{\hat{v}} R(\theta) \cdot \mathbf{\hat{n}}

Assuming the initial velocity :math:`\mathbf{v}` lies on the plane, we have :math:`\mathbf{v} \cdot \mathbf{\hat{n}} = 0`. On the other hand, :math:`\mathbf{\hat{v}} R(\theta) \cdot \mathbf{\hat{n}} \ne 0` because :math:`\mathbf{\hat{v}}` is being rotated out of the collision plane by :math:`\theta` radians. It follows that the angle between the rotated :math:`\mathbf{\hat{v}}` and :math:`\mathbf{\hat{n}}` must be :math:`\pi/2 + \theta`, or

.. math:: \mathbf{v}' \cdot \mathbf{\hat{n}} = \mu \cos\left( \frac{\pi}{2} + \theta \right) = -\mu \sin\theta

As usual, the speed as a result of the FME is given by

.. math:: \lVert\mathbf{v}'\rVert^2 = \lVert\mathbf{v}\rVert^2 + \mu^2 + 2 \lVert\mathbf{v}\rVert \mu \cos\theta

Substituting back to the collision equation and simplifying yields

.. math:: \lVert\mathbf{v}_c\rVert^2 = \lVert\mathbf{v}\rVert^2 + \mu^2 \cos^2 \theta + 2 \lVert\mathbf{v}\rVert \mu \cos\theta

Let :math:`\mu = \gamma_1`, then we can see that the speed is strictly decreasing in :math:`0 \le \theta \le \pi`.

Similarly, let :math:`\mu = \gamma_2`, setting the derivative to zero and simplifying, we obtain,

.. math:: 0 = (L - 2 \lVert\mathbf{v}\rVert \cos\theta) (\lVert\mathbf{v}\rVert \cos^2\theta - L \cos\theta - \lVert\mathbf{v}\rVert)

It can be shown that

.. math:: \cos\theta = \frac{L}{2\lVert\mathbf{v}\rVert}

gives the maximum of the function.

.. note:: TODO: more commentary

Pure sliding
------------

Pure sliding turns out to be one of the fastest ways to gain horizontal speed down a sloped wall. One gains horizontal speed much faster asymptotically than strafing. This is not surprising when we consider the fact that the horizontal speed due to strafing increases roughly in proportion to the square root of time. By sliding down a plane, however, both the horizontal and vertical speed can potentially increase linearly with time, or constant acceleration.

Recall from the general collision equation (GCE) (see :ref:`collision`) that

.. math:: \mathbf{v}_c = \mathbf{v}' - b (\mathbf{v}' \cdot \mathbf{\hat{n}}) \mathbf{\hat{n}}

where :math:`\mathbf{v}'` is the speed due to strafing and gravity and :math:`b = 1` is the assumed bounce coefficient. If no strafing is performed, we simply have

.. math:: \mathbf{v}' = \mathbf{v} - \langle 0, 0, m_g g \tau\rangle

where :math:`m_g` is :math:`1/2` in the first frame and :math:`1` for subsequent frame, to account for the `leapfrog integrated`_ gravitational field, as described in :ref:`player gravity`. To compute the GCE, we need to compute the dot product :math:`\mathbf{v}' \cdot \mathbf{\hat{n}}`. Assuming the initial velocity :math:`\mathbf{v}` lies on the plane, then :math:`\mathbf{v} \cdot \mathbf{\hat{n}} = 0`. If the plane normal makes an angle of :math:`0 \le \alpha \le \pi/2` with the horizontal plane, then we can write :math:`n_z = \sin\alpha`. What remains is therefore

.. _`leapfrog integrated`: https://en.wikipedia.org/wiki/Leapfrog_integration

.. math:: \mathbf{v}' \cdot \mathbf{\hat{n}} = m_g g \tau \cos \left( \frac{\pi}{2} + \alpha \right)
   = -m_g g\tau \sin\alpha

Eliminating the dot product and :math:`\mathbf{v}'` from the GCE yields

.. math:: \mathbf{v}_c = \mathbf{v} - \langle 0,0, m_g g\tau\rangle + \mathbf{\hat{n}} m_g g\tau \sin\alpha

Here we can see that

.. math:: v_{c,z} = v_z - m_g g\tau \cos^2 \alpha

while the horizontal speed is

.. math:: \lVert\langle v_{c,x}, v_{c,y}\rangle\rVert = \sqrt{A^2 + AB \cos\beta + \frac{1}{4} B^2}

where :math:`A = \sqrt{v_x^2 + v_y^2}`, :math:`B = m_g g \tau \sin 2\alpha`, and :math:`\beta` is the angle between the projected velocity on the horizontal plane :math:`\langle v_x, v_y\rangle` and the projected plane normal :math:`\langle n_x, n_y\rangle`. In the worst case where :math:`\beta = \pi/2`, the horizontal speed increases roughly square root with time, but not for long, because :math:`\beta` gradually decreases over time as the component of velocity in the direction of the plane normal accelerates. In the best case where :math:`\beta = 0`, the expression simplifies to

.. math:: \lVert\langle v_{c,x}, v_{c,y}\rangle\rVert = A + \frac{1}{2} B

That is, the horizontal speed accelerates linearly with time. This is also the steady state expression as :math:`\beta` drifts towards zero over time.

Vertical balance surfing
------------------------

Before tackling the harder issues on surfing, let's tackle a basic movement strategy. When surfing on a slope, one can move vertically up or down depending on the strafing angle :math:`\theta`. There must exist a critical :math:`\theta` such that the vertical velocity will remain zero throughout, resulting in no vertical movement. As we shall see later, the horizontal speed would usually increase as usual, though at a lower acceleration than pure strafing.

In the GCE, the velocity :math:`\mathbf{v}'` is due to the fundamental movement equation (FME) (described in detail in :ref:`player air ground`) added to the gravitational step. Namely,

.. math:: \mathbf{v}' = \left( \mathbf{v} + \mu \frac{\mathbf{v}}{\sqrt{v_x^2 + v_y^2}}
   R_z(\theta) \right) \operatorname{diag}(1,1,0)
   + \langle 0, 0, v_z - m_g g\tau\rangle

A few notes to be made here. First, :math:`\mathbf{v}` is a three-dimensional vector here, unlike the vectors in a typically written FME. Therefore, the rotation matrix is specifically a rotation about the :math:`z` axis, written as :math:`R_z(\theta)`. Second, :math:`\operatorname{diag}(a_1,\ldots,a_n)` means a diagonal matrix with entries :math:`a_1,\ldots,a_n`. By multiplying a vector with :math:`\operatorname{diag}(0,0,1)`, for example, we effectively zero out the :math:`x` and :math:`y` components. Indeed, the horizontal acceleration portion is multiplied by :math:`\operatorname{diag}(1,1,0)` because the vertical component of the velocities are ignored in strafing and horizontal acceleration in general. Third, the gravity time step has a :math:`m_g`, which has a value of :math:`m_g = 1/2` for the first frame and :math:`m_g = 1` for subsequent frames.

We now substitute :math:`\mathbf{v}'` into the GCE. To compute the GCE, we perform the dot product :math:`\mathbf{v}' \cdot \mathbf{\hat{n}}`. The first term from the product may be written as

.. math:: \left( \mathbf{v} + \mu\frac{\mathbf{v}}{\sqrt{v_x^2 + v_y^2}} R_z(\theta) \right) \operatorname{diag}(1,1,0) \cdot \mathbf{\hat{n}}

Assume that the initial velocity :math:`\mathbf{v}` lies on the plane, which makes :math:`\mathbf{v} \cdot \mathbf{\hat{n}} = 0`. Now :math:`\mathbf{v} R_z(\theta) \operatorname{diag}(1,1,0) \cdot \mathbf{\hat{n}} \ne 0` because the velocity vector is being rotated away or into the plane. It follows that the angle between the two vectors is :math:`\pi/2 + \lvert\theta\rvert` when projected onto the horizontal plane. The absolute value of :math:`\theta` must be taken because the strafing angle can be negative. On the other hand, note that the plane normal projected onto the horizontal plane is no longer a unit vector, but rather, a vector of length :math:`\cos\alpha` where :math:`\alpha` is the angle between the plane normal and the horizontal plane.

Using these observations, we find that the first term is equivalent to

.. math:: \mu\cos\left( \frac{\pi}{2} + \lvert\theta\rvert \right) \cos\alpha = -\mu\sin\lvert\theta\rvert \cos\alpha

The second term is easier to find. It is simply

.. math:: (v_z - m_g g\tau) \sin\alpha

From the GCE, the final vertical velocity is given by

.. math:: v_{c,z} = v_z' - (\mathbf{v}' \cdot \mathbf{\hat{n}}) n_z
   = v_z - m_g g\tau - \left( -\mu\sin\lvert\theta\rvert \cos\alpha + (v_z - m_g g\tau) \sin\alpha \right) \sin\alpha

Assume that :math:`v_z = v_{c,z} = 0`, which is the steady state where no vertical movement occurs, the equation simplifies to

.. math:: \mu \sin\lvert\theta\rvert \sin\alpha - m_g g\tau \cos\alpha = 0

This assumes :math:`\alpha \ne \pi/2`, which holds as long as the plane is not horizontal. Here, the usual analysis can be performed by assuming :math:`\mu = \gamma_1` or :math:`\mu = \gamma_2` and proceed to solve the equation. Empirical observations indicate that :math:`\mu = \gamma_2` is most frequently the admissible solution. Unfortunately, as is common in surfing analysis, writing down the solutions analytically is very difficult because it requires finding the roots of a quartic polynomial. It is much more practical to use a robust numerical method such as Brent's method to find a solution, or by computing the eigenvalues of the associated companion matrix.

Maximum per-frame horizontal acceleration
-----------------------------------------

This section describes an attempt to optimise the horizontal acceleration on a surf plane. This approach involves maximising the horizontal acceleration on a per-frame basis. That is, this approach only considers the current frame without accounting for the acceleration in future frames. In isolation, as it turns out, it does not give us a global optimum. This serves to illustrate the danger of thinking in per-frame terms as is common in pure strafing, where, by luck, per-frame optimisations happen to also yield a global optimum. Attempting to maximise the accelerate per frame is a greedy algorithm, which in general is not guaranteed to give the most optimal configurations.

To illustrate this point, we will not derive an analytical expression for per-frame maximum acceleration. It suffices to use a numerical algorithm on a common Half-Life configuration, which consists of :math:`A = 100`, :math:`\tau = 0.01` (for 100 fps), :math:`M = 320`, and a surf plane of :math:`\alpha = 30^\circ` such that :math:`\langle n_x, n_y, n_z\rangle = \langle 0, \cos\alpha, \sin\alpha\rangle`. Assume an initial velocity of :math:`\mathbf{v} = \langle 500, 0, 0\rangle`. One can check that the velocity and the plane normal are perpendicular.

Minimal time path
-----------------
