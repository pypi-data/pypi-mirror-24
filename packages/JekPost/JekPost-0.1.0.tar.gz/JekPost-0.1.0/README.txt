.. image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square  :target: http://choosealicense.com/licenses/mit/

=========
 JekPost
=========
A command-line utility to make your Jekyll experience smoother.

STATUS
=====
This project is currently in its development stages.

I've been working from a Linux Fedora 24 machine. I honestly have no idea how
this is going to behave on other operating systems.

USAGE
=====

Ensure that the directory where you installed JekPost is in your :code:`$PATH`.

To create a new Jekyll post::

  $ jekpost_create.py 'Post Title' dir --disqus 'your-disqus-shortname'

:code:`dir` is the directory name where you wish to save the new post to. It
can also be relative pathnames.

JekPost currently supports adding in an optional Disqus shortname.
