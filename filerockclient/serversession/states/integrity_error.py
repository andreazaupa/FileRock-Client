# -*- coding: ascii -*-
#  ______ _ _      _____            _       _____ _ _            _
# |  ____(_) |    |  __ \          | |     / ____| (_)          | |
# | |__   _| | ___| |__) |___   ___| | __ | |    | |_  ___ _ __ | |_
# |  __| | | |/ _ \  _  // _ \ / __| |/ / | |    | | |/ _ \ '_ \| __|
# | |    | | |  __/ | \ \ (_) | (__|   <  | |____| | |  __/ | | | |_
# |_|    |_|_|\___|_|  \_\___/ \___|_|\_\  \_____|_|_|\___|_| |_|\__|
#
# Copyright (C) 2012 Heyware s.r.l.
#
# This file is part of FileRock Client.
#
# FileRock Client is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FileRock Client is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with FileRock Client. If not, see <http://www.gnu.org/licenses/>.
#

"""
This is the integrity_error module.




----

This module is part of the FileRock Client.

Copyright (C) 2012 - Heyware s.r.l.

FileRock Client is licensed under GPLv3 License.

"""

from filerockclient.serversession.states.abstract import ServerSessionState
from filerockclient.interfaces import GStatuses


class IntegrityErrorState(ServerSessionState):

    accepted_messages = ServerSessionState.accepted_messages

    def _receive_next_message(self):
        return self._context._input_queue.get(['usercommand'])

    def _on_entering(self):
        self.logger.debug('State changed')
        self._context._internal_facade.set_global_status(
            GStatuses.C_HASHMISMATCHONCONNECT)
        self._context._ui_controller.notify_user('hash_mismatch')
        self._context.release_network_resources()
        if not self._context.keepalive_timer.is_suspended():
            self._context.keepalive_timer.suspend_execution()
        if not self._context.filesystem_watcher.is_suspended():
            self._context.filesystem_watcher.suspend_execution()
