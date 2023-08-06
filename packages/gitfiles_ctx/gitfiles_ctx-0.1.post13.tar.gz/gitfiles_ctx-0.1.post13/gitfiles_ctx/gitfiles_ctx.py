#! /usr/bin/env python

import git, logging, logtool, os, shutil, tempfile
from path import Path

LOG = logging.getLogger (__name__)
# https://stackoverflow.com/questions/28291909/gitpython-and-ssh-keys
# https://stackoverflow.com/questions/28803626/get-all-revisions-for-a-specific-file-in-gitpython

class GitFiles_Ctx (object):

  @logtool.log_call
  def __init__ (self, url, ssh_keypath, prefix = "gitfiles_ctx__",
                branch = "master"):
    self.ssh_keypath = ssh_keypath
    self.prefix = prefix
    self.fpath = None
    self.url = url
    self.branch = branch

  @logtool.log_call
  def __enter__ (self):
    self.fpath = tempfile.mkdtemp (prefix = self.prefix) + "/repo"
    ssh_cmd = "ssh -i {keypath}".format (keypath = self.ssh_keypath)
    os.environ["GIT_SSH_COMMAND"] = ssh_cmd
    git.Repo.clone_from (self.url, self.fpath,
                         env = {"GIT_SSH_COMMAND": ssh_cmd},
                         branch = self.branch)
    return self

  @logtool.log_call (log_exc = True)
  def __exit__ (self, exc_type, exc_val, exc_tb):
    shutil.rmtree (self.fpath)

  @logtool.log_call
  def read (self, fname):
    return file (Path (self.fpath) / fname).read ()
