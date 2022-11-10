reStructuredText support for Qt5
================================

Additional Roles
----------------

This project uses custom roles to extend the range of supported text formatting,
specifically:

Underlining
"""""""""""
::

  .. role:: underline

reStructuredText doesn't natively support underlining because, to quote David
Ascher in his `2000-01-21 Doc-SIG mailing list post`_ "Docstring grammar: a
very revised proposal":

  The tagging of underlined text with _'s is suboptimal. Underlines
  shouldn't be used from a typographic perspective (underlines were designed
  to be used in manuscripts to communicate to the typesetter that the text
  should be italicized -- no well-typeset book ever uses underlines), and
  conflict with double-underscored Python variable names (__init__ and the
  like), which would get truncated and underlined when that effect is not
  desired. Note that while complete markup would prevent that truncation
  ('__init__'), I think of docstring markups much like I think of type
  annotations -- they should be optional and above all do no harm. In this
  case the underline markup does harm.

His concerns about markup of python variables do not apply to us [#]_, so you may
indicate text to be underlined like so::

    Normal text :underline:`underlined text` normal text


Strike Through
""""""""""""""
::

  .. role:: strike

Referred to Qt5 as "strike out", this delineates where a horizontal line through
the vertical-middle of text should be drawn; and may be used thusly::

    Normal text :strike:`struck text` normal text


Additional roles
""""""""""""""""

That's it for built-in roles (for now). It is planned to look into the
possibility of expanding the capabilities programatically, but that's low
priority for now.


.. [#] Nor are we so up ourselves. "[...] no well-typeset book [...]" indeed.
       The guy needs to pick up a children's book once in a while.

.. _2000-01-21 Doc-SIG mailing list post:
    https://mail.python.org/pipermail/doc-sig/2000-January/000924.html
