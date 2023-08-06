# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2014, 2015, 2016 CERN.
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

"""Persistent identifier fetchers.

A proper fetcher is defined as a function that return a
:data:`invenio_pidstore.fetchers.FetchedPID` instance.

E.g.

.. code-block:: python

    def my_fetcher(record_uuid, data):
        return FetchedPID(
            provider=MyRecordIdProvider,
            pid_type=MyRecordIdProvider.pid_type,
            pid_value=extract_pid_value(data),
        )

To see more about providers see :mod:`invenio_pidstore.providers`.
"""

from __future__ import absolute_import, print_function

from collections import namedtuple

from .providers.recordid import RecordIdProvider

FetchedPID = namedtuple('FetchedPID', ['provider', 'pid_type', 'pid_value'])
"""A pid fetcher."""


def recid_fetcher(record_uuid, data):
    """Fetch a record's identifiers.

    :param record_uuid: The record UUID.
    :param data: The record metadata.
    :returns: A :data:`invenio_pidstore.fetchers.FetchedPID` instance.
    """
    return FetchedPID(
        provider=RecordIdProvider,
        pid_type=RecordIdProvider.pid_type,
        pid_value=str(data['control_number']),
    )
