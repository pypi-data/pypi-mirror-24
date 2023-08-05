GitFiles_Ctx
============

This...will likely take some time to mature.  And is a hack.

The broad intent is to provide a Git repository context at the file
level (over SSH).  In essence on entering the context, a path to an
ephemeral cleartext tree (top of master) of the remote repository will
be returned, and on exit that same tree will be removed.

Intended use is for system configuration data maintained and managed
via Git -- ie update the data in git and the dependent tools
reconfigure to match when they run, sort of using Git as a hacky etcd.
