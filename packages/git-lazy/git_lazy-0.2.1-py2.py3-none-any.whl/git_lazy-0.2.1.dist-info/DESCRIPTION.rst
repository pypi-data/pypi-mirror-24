Git Lazy
========

Author:Tim Santor tsantor@xstudios.agency

Overview
--------

Git-Lazy is a tool for lazy developers like me. I typically work on not
only my work computer, but my home office computer or a laptop when I am
on the go. Using Git-Lazy, I can easily search directories for Git repos
and add them to a file which will be synced by Dropbox or Google Drive.
Then, when I move to another machine mentioned above, I can simply run
``git-lazy --sync`` and my current development environment will create
all the repos I need. It can also run bulk status\|push\|pull operations
on all my git repos.

Installation
------------

To install Git Lazy, simply:

::

    pip install git-lazy

Then create a config file ``^/config/git-lazy.cfg``:

::

    [default]
    ; Usernames for repos we're interesting in
    repo_users=tsantor,xstudios
    ; File to contain all repos we want to manage (preferably on a Cloud Drive)
    repo_list=^/Google Drive/Personal/repo_list.json
    ; The top-level directories we want to traverse to find repos
    search_dirs=^/Projects,^/Sandbox

Usage
-----

::

    git-lazy --find  # find all repos
    git-lazy --sync  # sync all repos

    git-lazy --add  ^/repo/dir  # Add a repo to the list
    git-lazy --remove  ^/repo/dir # Remove a repo from the list

    git-lazy -m status  # perform git status on all repos
    git-lazy -m pull  # perform git pull on all repos
    git-lazy -m push  # perform git push on all repos

    git-lazy --remove_interactive  # Remove repos

    NOTE: For all available methods run ``git-lazy -h``

Issues
------

If you experience any issues, please create an
`issue <https://bitbucket.org/tsantor/git-lazy/issues>`__ on Bitbucket.


History
=======

All notable changes to this project will be documented in this file.
This project adheres to `Semantic Versioning <http://semver.org/>`__.

0.1.0 (2016-03-01)
------------------

-  First release on PyPI.

0.1.1 (2016-03-04)
------------------

-  Do not attempt to do git operations on non-existent repos on current
   machine.

0.1.5 (2017-02-21)
------------------

-  Various enhancements

0.1.7 (2017-04-04)
------------------

-  Bug fix where using ``--find`` after already using it would only
   create a repo list of the newly found repos.

0.1.8 (2017-04-24)
------------------

-  Bug fix where using ``--find`` would add repos twice.

0.1.9 (2017-06-25)
------------------

-  Added ``--update_origins`` to update all repo urls from HTTPS to SSH

0.2.0 (2017-08-04)
------------------

-  Fixed bug with ``--find``

0.2.1 (2017-08-04)
------------------

-  Fixed bug with ``--find`` when no origin set
-  Update ``update_origins`` regex logic to handle https and ssh schemes
-  Added ``repo_users`` to config (comma-delimited)


