***
ryd
***

``ryd`` ( /rɑɪt/, pronounced like the verb "write" ) is a preprocessor for written
documents that builds upon the multi-document capabilities of the YAML file format.

``ryd`` allows for clear separation between document text and programs referenced
in those text, making it possible to run (c.q. compile) the program parts of a
document, e.g. to check whether they are syntactically correct. It can also capture the
*actual* output of those programs to be included in the document.

This allows for easier maintanance of (correct) programs sources like
reStructuredText, LaTeX, etc.

Example
=======

A ``.ryd`` file consists of multiple YAML documents in one, standard, YAML file.

In the normal case, the first of these documents has, at the top-level, a
mapping. This mapping defines the metadata: version, output and other configuration
information. The following documents are block style literal scalars with an
optional tag. The tag influences how the scalar string is processed within the
output system selected in the metadata::

  ---
  version: 0.1
  output: rst
  fix_inline_single_backquotes: true
  --- |
  Example Python program
  ++++++++++++++++++++++

  This is an example of a python program
  --- !python |
  n = 7
  print(n**2 - n)
  --- !stdout |
  The answer is::

this will generate (``pyd convert test.ryd``) the following ``test.rst``::

  Example Python program
  ++++++++++++++++++++++

  This is an example of a python program
  ::

    n = 7
    print(n**2 - n)

  The answer is::

    42

Because of the special meaning of ``---`` (and ``...``) at the beginning of a line,
followed by newline or space, the section under/over-line characters used in
``.ryd`` files that are source for ``.rst`` should not use ``-`` or ``.``
sequences if a any of those sections consist of three letters (e.g. a section
named API or RST). It is recommended to use the following scheme::

   Sections, subsections, etc. in .ryd files
    # with overline, for parts
    * with overline, for chapters
    =, for sections
    +, for subsections
    ^, for subsubsections
    ", for paragraphs

Single backquotes
+++++++++++++++++

The ``fix_inline_single_backquotes: true`` tells ``ryd`` to indicate lines that have
single backquotes that need fixing (by replacing them with double backquotes)::

  README.ryd
  47: this will generate (`pyd convert test.ryd`) the following
                        --^
                                             --^

RST
===

The output to ``.rst`` expects non-code YAML documents to be valid
reStructeredText. Any non-tagged document, i.e. those starting with::

  --- |

is assumed to be text input.

Python
++++++

Python code is indicated by::

  --- !python |

The document is inserted into the ``.rst`` with a two space indent. If the
previous block does not end in ``::`` this and a newline is explicitly inserted
before the program. The difference being that a text block ending in ``::`` will
have a ``:`` rendered, a ``::`` on a line of its own will not. An empty line between
the preceding text and the code is inserted when needed.

If your program relies on specific packages, those packages, need to
be available in the environment in which ``ryd`` is started (which can e.g. be a
specifically set up ``virtualenv``)


It is possible to have "partial programs" by preceding a python document with
e.g.::

  --- !python-pre |
  from __future__ import print_function
  import sys
  import ruamel.yaml
  from ruamel.std.pathlib import Path, pushd, popd, PathLibConversionHelper
  pl = PathLibConversionHelper()

Such a block is pre-pended to all following ``--- !python |`` documents (until
superseded by another ``--- !python-pre |`` block)


Captured output
+++++++++++++++

The output from the last program that was run (``--- !python |``) is stored and
can be post-pended to a reStrucuteredText document by tagging it with ``!stdout``
(i.e. ``--- !stdout |``)

Non-running code
++++++++++++++++

A document tagged ``!code`` will be represented as one tagged ``!python``, but
the code will not be run (and hence the output used for ``!stdout`` not changed).

Raw include
+++++++++++

Us ``--- !incraw |`` with list of filenames to include (non-recursive, the files
are **not** parsed as .ryd files).

Comments
========

Block style literal scalars do not allow YAML comments. To insert comments in a
text, either use the format acceptable by the output, e.g. when generating ``.rst`` use::

   .. comment
      this will show up in the resulting .rst file, but will
      not render

Alternatively you can create a comment YAML document (``--- !comment |``) for
which the text will not be represented in the output file format **at all**.


History
=======

``ryd`` grew out of an in-house solution where sections of restructured text files were
udpated, in-place, by running Python programs specified in seperate files. Also
allowing the inclusion of the (error) output.

An example of this can be seen in `this
<https://bitbucket.org/ruamel/yaml/raw/0be7d3cb8449b15d9ac9b097322f09e52b92f868/_doc/example.rst>`_
old version of the ``example.rst`` file of the ``ruamel.yaml`` package::

  Basic round trip of parsing YAML to Python objects, modifying
  and generating YAML::

    import sys
    from ruamel.yaml import YAML

    inp = """\
    # example
    name:
      # details
      family: Smith   # very common
      given: Alice    # one of the siblings
    """

    yaml = YAML()
    code = yaml.load(inp)
    code['name']['given'] = 'Bob'

    yaml.dump(code, sys.stdout)

  .. example code small.py

  Resulting in ::

    # example
    name:
      # details
      family: Smith   # very common
      given: Bob      # one of the siblings


  .. example output small.py


The program was inserted before the ``.. example code`` line and its output before
``.. example output``, replacing all the text starting after the previous ``::``

The ``small.py`` referenced a seperate file for this piece of code.
This resulted in multiple source files that were associated with a single
``.rst`` file. There was no mechanism to have partial programs that could be
tested by execution, which precluded getting output from such program as well.

Although the code could have been edited in place, and used to get the output,
this would force one to use the extra indentation required by reST's ``::``.

Once this system came under review, the solution with a structured YAML header, as used
with various file formats, combined with multiple document consisting of
(tagged) top level, non-indented, block style literal scalars, was chosen instead.


