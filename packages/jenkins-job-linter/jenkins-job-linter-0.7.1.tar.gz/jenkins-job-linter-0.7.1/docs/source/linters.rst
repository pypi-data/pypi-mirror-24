.. _linters:

Linters
=======

``ensure_timestamps``
---------------------

Ensure that a job is configured to produce timestamps in its console
output.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

No configuration options.

``check_for_empty_shell``
-------------------------

Ensure that all shell builders in a job have some content.

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

``check_shebang``
-----------------

Ensure that all shell builders in a job have an appropriate shebang.

This will ignore non-shell shebangs, and ensure that any shell shebangs
have all of `-eux` set.  The Jenkins default shebang is accepted, but
this can be configured (see below).

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

``allow_default_shebang``
    A boolean defining whether the default Jenkins shebang should be
    permitted in shell builders (i.e. should shell builders be
    permitted to have no shebang).  Defaults to True.

``required_shell_options``
    A string of the shell options that are required to be present in
    the shebang of shell builders.  Defaults to "eux".
