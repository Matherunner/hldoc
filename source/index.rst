Half-Life Physics Reference
===========================

.. caution:: This documentation is work in progress! Some parts may be
   incomplete, and others may be bleeding edge research.

.. image:: images/gordon-scientist.jpg

Welcome to the unofficial technical reference for the physics governing the Half-Life_ universe!

While the community has produced very comprehensive resources for games in the Half-Life series, such as the `Half-Life Wiki`_ and the `Combine OverWiki`_, *these wikis primarily prioritise narrative lore and casual gameplay*. In addition, while both the `old <old SourceRuns Wiki_>`_ and the `new SourceRuns Wiki`_ do address the practicalities of speedrunning and provide technical descriptions of tricks aimed to help speedrunners gain a working knowledge or operational understanding of them, they leave a void in precision and formality at the level of mathematics and code. Despite the abundance of strategy guides, there remains a distinct lack of resources that describe the game's underlying physics with a satisfying level of rigour.

.. _Half-Life: https://en.wikipedia.org/wiki/Half-Life_(video_game)
.. _Half-Life Wiki: https://half-life.fandom.com/wiki/Main_Page
.. _Combine OverWiki: https://combineoverwiki.net/wiki/Main_Page
.. _old SourceRuns Wiki: https://wiki.sourceruns.org/Main-Page.html
.. _new SourceRuns Wiki: https://wiki.openag.pro/

Understanding the mechanics of Half-Life is essential for the development of tool-assisted speedruns (TAS) utilities and the execution of the runs themselves. Exploiting the engine to its fullest extent requires high-precision tools, but perhaps more importantly, it requires a deep intuition for how the game processes various complex mechanics such as :ref:`strafing`, :ref:`nuking` etc. Developing this understanding is vital for optimising routes, along with problem solving and troubleshooting tricky physics issues that arise during speedrunning.

Thus, this documentation strives to detail all aspects of the engine's physics to provide curious minds with a much deeper appreciation for the technical side of Half-Life and the breathtaking speedruns produced by multiple generations of the community over the years. Whether you are a tool developer seeking a guide or a runner looking to master the game's inner workings, this material aims to be your primary reference.

Contact
-------

This documentation is currently a one-man project maintained by `Jiangwei Chong <https://jwchong.com>`_, a software engineer. Feel free to reach out via the following for questions, feedback, suggestions, ideas, or anything you'd like to talk about:

- **Matherunner** at `Discord <https://discord.gg/sourceruns>`_
- jw@jwchong.com

Frequently asked questions
--------------------------

**Who are you?** I'm someone who played Half-Life as a kid and became deeply fascinated by its physics much later when quadrazid published `this monumental single-segment run <quadrazid single-segment_>`_ in 2011. My drive to understand how every trick in that run functioned necessitated a deep dive into the physics and mathematics of the game engine.

.. _quadrazid single-segment: https://youtu.be/AKIpyz0EjuY

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
simplify these concepts may help in general play and manual speedrunning, but the simplified
explanations may fail to account for the edge cases. It is often these edge cases that
we seek to exploit in a TAS. A quote often attributed to Albert Einstein sums
this up aptly:

   "*Everything should be made as simple as possible, but no simpler.*"

**Are the equations made up from thin air?** We do not conjure up any equation
based on conjectures or guesswork, unless *clearly* stated otherwise. All
equations and mathematics in this documentation are ultimately derived from the
Half-Life SDK or the reverse-engineered engine code. Empirically derived
equations will also be explicitly identified as such.

**How did you create this documentation?** We experimented with various
tools, including LaTeX, but ultimately settled on reStructuredText with Sphinx_
in combination with pre-rendered MathJax_. Sphinx is an exceptional system for
generating highly structured documentations. In fact, it is used to document
most Python modules, including the heavy hitters like numpy_, requests_, etc. In
addition, reStructuredText is the most extensible and structured markup language
that is not LaTeX, rivalled only by AsciiDoc or AsciiDoctor. For mathematical
typesetting, MathJax is by far the most mature for the web which runs well on
many browsers. Prominent sites such as MathOverflow_ use it. By pre-rendering
MathJax, we have significantly reduced page loading times.

.. _Sphinx: http://www.sphinx-doc.org/en/master/
.. _MathJax: https://docs.mathjax.org/en/latest/
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

We do not use the prime notation as in :math:`x'` to mean :math:`dx/dt`. Generally, the prime version of a variable denotes the *next state* of the variable, whatever "next" may be. If we intend to notate differentiation, we always write out :math:`dx/dt` explicitly.

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
