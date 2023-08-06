# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Default values for access configuration.

.. note::

    By default no caching is enabled. For production instances it is **highly
    advisable** to enable caching as the permission checking is very query
    intensive on the database.
"""

ACCESS_CACHE = None
"""A cache instance or an importable string pointing to the cache instance."""

ACCESS_ACTION_CACHE_PREFIX = 'Permission::action::'
"""Prefix for actions cached when used in dynamic permissions."""

ACCESS_LOAD_SYSTEM_ROLE_NEEDS = True
"""Enables the loading of system role needs when users' identity change."""
