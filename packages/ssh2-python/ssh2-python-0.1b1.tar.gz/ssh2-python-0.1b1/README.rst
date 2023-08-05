ssh2-python
============

Fast Python SSH library
------------------------

Fast SSH2 protocol library. `ssh2-python` provides Python bindings for `libssh2`_.

Features
---------

Majority of the `libssh2`_ API has been implemented as Python native code extensions. `ssh2-python` aims to be a thin wrapper of `libssh2`_, so code examples can be ported straight over to Python with only few changes.

SSH Functionality provided
++++++++++++++++++++++++++++

* SSH channel operations (exec,shell,subsystem)
* SSH port forward and tunnelling
* SSH agent
* Public key authentication and management
* SFTP
* SCP
* Non-blocking mode
* Listener for port forwarding

And more, per `libssh2`_ functionality.

.. _libssh2: https://www.libssh2.org
