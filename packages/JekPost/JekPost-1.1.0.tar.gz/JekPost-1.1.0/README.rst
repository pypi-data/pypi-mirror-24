 JekPost
=========

A command-line utility to create a Jekyll posts file with appropriate filename and headers.


USAGE
=====

**Ensure that the directory where you installed JekPost is in your `$PATH`.**

To create a new Jekyll post:

::

  $ jekpost_create.py 'Post Title' dir

`dir` is the directory name where you wish to save the new post to, relative to the directory from which you run this command.
This is usually the `_posts` directory.

JekPost currently supports adding in an optional Disqus shortname. To create a post with support for Disqus comments:

::

  $ jekpost_create.py 'Post Title' dir --disqus 'your-disqus-shortname'
