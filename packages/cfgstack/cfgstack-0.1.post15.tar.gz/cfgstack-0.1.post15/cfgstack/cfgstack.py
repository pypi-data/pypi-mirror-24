#! /usr/bin/env python

import copy, json, logtool, os, pprint, yaml
from addict import Dict

DEFAULT_KEY = "_default_"
INCLUDE_KEY = "_include_"

#@logtool.log_call (log_args = False)
def _dictmerge (master, update):
  for k, v in update.items():
    if (k in master and isinstance (master[k], dict)
        and isinstance (update[k], dict)):
      _dictmerge (master[k], update[k])
    elif k not in master:
      master[k] = v

class CfgStack (object):

  """Note that dictionaries inside of lists are not expanded with
  respects to _default_ and _include_.  Only the immediate tree of
  dicts is munged.  The backing premise for this is that the purpose
  is configuration data, key value pairs, not arbitrary constructs.
  """

  # pylint: disable=too-few-public-methods

  @logtool.log_call
  def __init__ (self, fname, no_defaults = False):
    # pylint: disable=too-many-nested-blocks,too-many-branches
    self.fname = fname
    self.read = self._load (fname)
    self.no_defaults = no_defaults
    self._do_includes ()
    if not no_defaults:
      self._do_defaults ()
    self.data = Dict (self.read)

  @logtool.log_call
  def _load (self, fname):
    if not isinstance (fname, basestring):
      raise ValueError ("Name: %s is not a string" % fname)
    # FIXME: Be smarter about relative paths
    if os.path.isfile (fname + ".json"):
      return json.loads (file (fname + ".json").read ())
    elif os.path.isfile (fname + ".yaml"):
      return yaml.safe_load (file (fname + ".yaml"))
    elif os.path.isfile (fname + ".yml"):
      return yaml.safe_load (file (fname + ".yml"))
    else:
      raise IOError ("CfgStack: Cannot find file for %s in %s"
                     % (fname, os.getcwd ()))

  #@logtool.log_call (log_args = False, log_rc = False)
  def _do_nesting (self, d, stack):
    if isinstance (d, dict):
      for _, v in d.items ():
        if isinstance (v, dict):
          stack.append (v)

  #@logtool.log_call (log_args = False, log_rc = False)
  def _do_includes (self):
    stack = [self.read,]
    for d in stack:
      include = d.pop (INCLUDE_KEY, [])
      if isinstance (include, list):
        for f in include:
          for k, v in CfgStack (
              f, no_defaults = True).data.items ():
            if isinstance (d.get (k), dict) and isinstance (v, dict):
              _dictmerge (d[k], v)
            else:
              d[k] = v
      self._do_nesting (d, stack)

  #@logtool.log_call (log_args = False)
  def _do_defaults (self):
    stack = [self.read,]
    for d in stack:
      default = d.get (DEFAULT_KEY, {})
      if isinstance (default, dict):
        for k, v in d.items ():
          if (isinstance (v, dict) and isinstance (default, dict)
              and default != {}):
            _dictmerge (v, default)
          if isinstance (v, dict):
            stack.append (d[k])
      d.pop (DEFAULT_KEY, {})

  @logtool.log_call
  def as_yaml (self):
    return yaml.dump (self.data.to_dict (), width = 70, indent = 2,
                      default_flow_style = False)

  @logtool.log_call
  def as_json (self, indent = 2):
    return json.dumps (self.read, indent = indent)

  @logtool.log_call
  def as_pretty (self):
    return pprint.pformat (self.data.to_dict ())
