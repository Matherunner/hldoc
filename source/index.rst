Half-Life Physics Reference
===========================

.. caution:: This documentation is work in progress! Some parts may be
   incomplete, and others may be bleeding edge research.

.. image:: images/gordon-scientist.jpg

This is an unofficial documentation for the physics governing the Half-Life_ universe. There have been many very comprehensive wikis for games in the Half-Life series, such as the `Half-Life Wikia`_ and the `Combine OverWiki`_. These wikis focus on the storyline and casual gaming aspects of the Half-Life series video games. There is also a wiki for the practical speedrunning aspects of these games, namely the `SourceRuns Wiki`_, though it has been virtually abandoned with little to no updates. Despite the wealth of strategy guides available for Half-Life, it is almost impossible to find documentations describing the physics of the game with a satisfying level of technical accuracy.

.. _Half-Life: https://en.wikipedia.org/wiki/Half-Life_(video_game)
.. _Half-Life Wikia: http://half-life.wikia.com/wiki/Main_Page
.. _Combine OverWiki: http://combineoverwiki.net/wiki/Main_Page
.. _SourceRuns Wiki: http://wiki.sourceruns.org/wiki/Main_Page

Knowledge about the physics of Half-Life is important for developing tools for Half-Life TAS production and for the process of TASing itself. Highly precise tools are required to exploit the in-game physics to the fullest extent. Perhaps more importantly, developing an understanding and intuition for Half-Life physics is vital in producing a highly optimised TAS for the game and resolving tricky physics issues arising out of speedrunning.

Thus, this documentation strives to detail all aspects of the physics in a way that would help any curious minds to gain a much deeper appreciation for Half-Life and its speedruns. The potential tool developers will also find this documentation a helpful guide. This documentation aims to serve as a definitive reference material for Half-Life physics.

Frequently asked questions
--------------------------

**Who are you?** I'm someone who played Half-Life as a kid, and became deeply
fascinated by its physics much later when this_ monumental single-segment run
was published in 2011 by quadrazid. I sought to understand how every trick in
the run worked, which necessitated the study of the physics of the entire game.

.. _this: https://youtu.be/AKIpyz0EjuY

**Would I be able to understand this documentation?** It depends on how much
mathematics and programming you know. You are assumed to have an *intermediate*
level of understanding of the latest Half-Life SDK, and have it available at all
times when you need to reference it. By extension, you are assumed to be
proficient in C or C++. Since this documentation is heavy in mathematics, you
are assumed to be fluent in vector algebra and some linear algebra, along with a
high proficiency in trigonometry. Some knowledge of calculus is also assumed.

**Couldn't you write this documentation in a simpler way?** Our goal with this
documentation is to describe the physics of Half-Life as precisely as possible.
Many of the concepts in Half-Life are highly intricate and precise. Attempts to
simplify these concepts may help in many situations, but the simplified
explanations will fail under some edge cases. It is often these edge cases that
we seek to exploit in a TAS. A quote often attributed to Albert Einstein sums
this up aptly:

   *Everything should be made as simple as possible, but no simpler.*

**Are the equations made up from thin air?** We do not conjure up any equation
based on conjectures or guesswork, unless *clearly* stated otherwise. All
equations and mathematics in this documentation are ultimately derived from the
Half-Life SDK or the reverse-engineered engine code. Empirically derived
equations will also be stated clearly.

**How did you create this documentation?** We experimented with many different
tools, including LaTeX, but ultimately settled on reStructuredText with Sphinx_
in combination with `pre-rendered`_ MathJax_. Sphinx is a really good system for
generating highly structured documentations. In fact, it is used to document
most Python modules, including the heavy hitters like numpy_, requests_, etc. In
addition, reStructuredText is the most extensible and structured markup language
that is not LaTeX, rivalled only by AsciiDoc or AsciiDoctor. For mathematical
typesetting, MathJax is by far the most mature for the web which runs well on
many browsers. Prominent sites such as MathOverflow_ use it. By pre-rendering
MathJax, the loading times of pages can be dramatically reduced.

.. _Sphinx: http://www.sphinx-doc.org/en/master/
.. _pre-rendered: https://github.com/mathjax/MathJax-node
.. _MathJax: https://www.mathjax.org
.. _numpy: http://www.numpy.org
.. _requests: http://docs.python-requests.org/en/master/
.. _MathOverflow: https://mathoverflow.net

.. _notations:

Notations Used
--------------

One of the most important mathematical objects in discussions of Half-Life physics is the Euclidean vector. All vectors are in either :math:`\mathbb{R}^2` or :math:`\mathbb{R}^3`, where :math:`\mathbb{R}` denotes the real numbers. This is sometimes not specified explicitly if the contextual clues are sufficient for disambiguation.

All vectors are written in boldface like so:

.. math:: \mathbf{v}

Every vector has an associated length, which is referred to as the *norm*. The norm of some vector :math:`\mathbf{v}` is thus denoted as

.. math:: \lVert\mathbf{v}\rVert

A vector of length one is called a *unit vector*. So the unit vector in the direction of some vector :math:`\mathbf{v}` is written with a hat:

.. math:: \mathbf{\hat{v}} = \frac{\mathbf{v}}{\lVert\mathbf{v}\rVert}

There are three special unit vectors, namely

.. math:: \mathbf{\hat{i}} \quad \mathbf{\hat{j}} \quad \mathbf{\hat{k}}

These vectors point towards the positive :math:`x`, :math:`y` and :math:`z` axes respectively.

Every vector also has components in each axis. For a vector in :math:`\mathbb{R}^2`, it has an :math:`x` component and a :math:`y` component. A vector in :math:`\mathbb{R}^3` has an additional :math:`z` component. To write out the components of a vector explicitly, we have

.. math:: \mathbf{v} = \langle v_x, v_y, v_z\rangle

This is equivalent to writing :math:`\mathbf{v} = v_x \mathbf{\hat{i}} + v_y \mathbf{\hat{j}} + v_z \mathbf{\hat{k}}`. However, we never write out the components this way in this documentation as it is tedious. Notice that we are writing vectors as row vectors. This will be important to keep in mind when we apply matrix transformations to vectors.

The dot product between two vectors :math:`\mathbf{a}` and :math:`\mathbf{b}` is written as

.. math:: \mathbf{a} \cdot \mathbf{b}

On the other hand, the cross product between :math:`\mathbf{a}` and :math:`\mathbf{b}` is

.. math:: \mathbf{a} \times \mathbf{b}

Contact
-------

This documentation is currently a one-man project. `Contact me`_.

.. _Contact me: jw@jwchong.com

Contents
--------

.. toctree::
   :numbered:
   :maxdepth: 2

   game
   entity
   player
   movement
   duckjump
   strafing
   gravitymotion
   surfing
   ladder
   automation
   damage
   explosions
   weapons
   monsters
   triggers
   funcs
   casestudies
   practical
   othergames
   glossary
