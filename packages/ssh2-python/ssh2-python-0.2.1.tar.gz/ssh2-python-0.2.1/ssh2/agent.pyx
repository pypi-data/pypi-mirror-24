# This file is part of ssh2-python.
# Copyright (C) 2017 Panos Kittenis

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, version 2.1.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

cimport c_ssh2
from pkey cimport PublicKey, PyPublicKey
from exceptions cimport AgentConnectError, AgentListIdentitiesError, \
    AgentGetIdentityError, AgentAuthenticationError


cdef int auth_identity(const char *username,
                       c_ssh2.LIBSSH2_AGENT *agent,
                       c_ssh2.libssh2_agent_publickey **identity,
                       c_ssh2.libssh2_agent_publickey *prev) nogil except -1:
    cdef int rc
    rc = c_ssh2.libssh2_agent_get_identity(
        agent, identity, prev)
    if rc == 1:
        clear_agent(agent)
        with gil:
            raise AgentAuthenticationError(
                "No identities match for user %s",
                username)
    elif rc < 0:
        clear_agent(agent)
        with gil:
            raise AgentGetIdentityError(
                "Failure getting identity for user %s from agent",
                username)
    return rc


cdef void clear_agent(c_ssh2.LIBSSH2_AGENT *agent) nogil:
    c_ssh2.libssh2_agent_disconnect(agent)
    c_ssh2.libssh2_agent_free(agent)


cdef object PyAgent(c_ssh2.LIBSSH2_AGENT *agent):
    cdef Agent _agent = Agent()
    _agent._agent = agent
    return _agent


cdef class Agent:
    # TODO - Needs session reference

    def __cinit__(self):
        self._agent = NULL

    def __dealloc__(self):
        with nogil:
            clear_agent(self._agent)

    def list_identities(self):
        """This method is a no-op - use get_identities to list and retrieve
        identities
        """
        pass

    def get_identities(self, const char *username):
        """List and get identities from agent

        :rtype: list(:py:class:`PublicKey`)
        """
        cdef int rc
        cdef list identities = []
        cdef c_ssh2.libssh2_agent_publickey *identity = NULL
        cdef c_ssh2.libssh2_agent_publickey *prev = NULL
        with nogil:
            if c_ssh2.libssh2_agent_list_identities(self._agent) != 0:
                with gil:
                    raise AgentListIdentitiesError(
                        "Failure requesting identities from agent." \
                        "Agent must be connected first")
            while c_ssh2.libssh2_agent_get_identity(
                    self._agent, &identity, prev) == 0:
                with gil:
                    identities.append(PyPublicKey(identity))
                prev = identity
        return identities

    def userauth(self, const char *username,
                 PublicKey pkey):
        """Perform user authentication with specific public key

        :param username: User name to authenticate as
        :type username: str
        :param pkey: Public key to authenticate with
        :type pkey: py:class:`PublicKey`
        """
        cdef int rc
        with nogil:
            rc = c_ssh2.libssh2_agent_userauth(
                self._agent, username, pkey._pkey)
        return rc

    def disconnect(self):
        cdef int rc
        with nogil:
            rc = c_ssh2.libssh2_agent_disconnect(self._agent)
        return rc

    def connect(self):
        with nogil:
            if c_ssh2.libssh2_agent_connect(self._agent) != 0:
                with gil:
                    raise AgentConnectError("Unable to connect to agent")
