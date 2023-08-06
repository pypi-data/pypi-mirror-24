# -*- coding: utf-8 -*-
# privilege_policies.py
# Copyright (C) 2013 LEAP
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Helpers to determine if the needed policies for privilege escalation
are operative under this client run.
"""

import commands
import os
import subprocess
import platform
import time

from abc import ABCMeta, abstractmethod

from twisted.logger import Logger
from twisted.python.procutils import which

from leap.bitmask.util import STANDALONE, here

from .constants import IS_LINUX

log = Logger()


# TODO wrap the install/uninstall helper functions around the policychecker
# classes below.


def install_helpers():
    _helper_installer('install')


def uninstall_helpers():
    _helper_installer('uninstall')


def _helper_installer(action):
    if action not in ('install', 'uninstall'):
        raise Exception('Wrong action: %s' % action)

    if IS_LINUX:
        cmd = 'bitmask_helpers ' + action
        if STANDALONE:
            binary_path = os.path.join(here(), "bitmask")
            cmd = "%s %s" % (binary_path, cmd)
        if os.getuid() != 0:
            cmd = 'pkexec ' + cmd
        retcode, output = commands.getstatusoutput(cmd)
        if retcode != 0:
            log.error('Error installing/uninstalling helpers: %s' % output)
            log.error('Command was: %s' % cmd)
            raise Exception('Could not install/install helpers')
    else:
        raise Exception('No install mechanism for this platform')


class NoPolkitAuthAgentAvailable(Exception):
    message = 'No polkit authentication agent available. Please run one.'


class NoPkexecAvailable(Exception):
    message = 'Could not find pkexec in the system'


# TODO rename to privileged_runner or something like that
def is_missing_policy_permissions():
    """
    Returns True if we do not have implemented a policy checker for this
    platform, or if the policy checker exists but it cannot find the
    appropriate policy mechanisms in place.

    :rtype: bool
    """
    _system = platform.system()
    platform_checker = _system + "PolicyChecker"
    policy_checker = globals().get(platform_checker, None)
    if not policy_checker:
        # it is true that we miss permission to escalate
        # privileges without asking for password each time.
        log.debug('we could not find a policy checker implementation '
                  'for %s' % (_system,))
        return True
    return policy_checker().is_missing_policy_permissions()


class PolicyChecker:
    """
    Abstract PolicyChecker class
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def is_missing_policy_permissions(self):
        """
        Returns True if we could not find any policy mechanisms that
        are defined to be in used for this particular platform.

        :rtype: bool
        """
        return True


class LinuxPolicyChecker(PolicyChecker):
    """
    PolicyChecker for Linux
    """
    LINUX_POLKIT_FILE = ("/usr/share/polkit-1/actions/"
                         "se.leap.bitmask.policy")
    LINUX_POLKIT_FILE_BUNDLE = ("/usr/share/polkit-1/actions/"
                                "se.leap.bitmask.bundle.policy")
    PKEXEC_BIN = 'pkexec'

    @classmethod
    def get_polkit_path(self):
        """
        Returns the polkit file path.

        :rtype: str
        """
        return (self.LINUX_POLKIT_FILE_BUNDLE if STANDALONE
                else self.LINUX_POLKIT_FILE)

    def is_missing_policy_permissions(self):
        # FIXME this name is quite confusing, it does not have anything to do
        # with file permissions.
        """
        Returns True if we could not find the appropriate policykit file
        in place

        :rtype: bool
        """
        path = self.get_polkit_path()
        return not os.path.isfile(path)

    @classmethod
    def maybe_pkexec(self):
        """
        Checks whether pkexec is available in the system, and
        returns the path if found.

        Might raise:
            NoPkexecAvailable,
            NoPolkitAuthAgentAvailable.

        :returns: a list of the paths where pkexec is to be found
        :rtype: list
        """
        if self._is_pkexec_in_system():
            if not self.is_up():
                self.launch()
                time.sleep(2)
            if self.is_up():
                pkexec_possibilities = which(self.PKEXEC_BIN)
                if not pkexec_possibilities:
                    raise Exception("We couldn't find pkexec")
                return pkexec_possibilities
            else:
                log.warn('No polkit auth agent found. pkexec ' +
                         'will use its own auth agent.')
                raise NoPolkitAuthAgentAvailable()
        else:
            log.warn('System has no pkexec')
            raise NoPkexecAvailable()

    @classmethod
    def launch(self):
        """
        Tries to launch polkit agent.
        """
        if not self.is_up():
            try:
                # We need to quote the command because subprocess call
                # will do "sh -c 'foo'", so if we do not quoute it we'll end
                # up with a invocation to the python interpreter. And that
                # is bad.
                log.debug('Trying to launch polkit agent')
                subprocess.call(
                    ["python -m leap.bitmask.vpn.helpers.linux.polkit_agent"],
                    shell=True)
            except Exception:
                log.failure('Error while launching vpn')

    @classmethod
    def is_up(self):
        """
        Checks if a polkit daemon is running.

        :return: True if it's running, False if it's not.
        :rtype: boolean
        """
        # Note that gnome-shell does not uses a separate process for the
        # polkit-agent, it uses a polkit-agent within its own process so we
        # can't ps-grep a polkit process, we can ps-grep gnome-shell itself.

        # the square brackets are to avoid grep match itself
        polkit_options = [
            'ps aux | grep "polkit-[g]nome-authentication-agent-1"',
            'ps aux | grep "polkit-[k]de-authentication-agent-1"',
            'ps aux | grep "polkit-[m]ate-authentication-agent-1"',
            'ps aux | grep "[l]xpolkit"',
            'ps aux | grep "[l]xsession"',
            'ps aux | grep "[g]nome-shell"',
            'ps aux | grep "[f]ingerprint-polkit-agent"',
            'ps aux | grep "[x]fce-polkit"',
        ]
        is_running = [commands.getoutput(cmd) for cmd in polkit_options]

        return any(is_running)

    @classmethod
    def _is_pkexec_in_system(self):
        """
        Checks the existence of the pkexec binary in system.
        """
        pkexec_path = which('pkexec')
        if len(pkexec_path) == 0:
            return False
        return True
