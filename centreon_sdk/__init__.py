"""
This program is a library to communicate with the Centreon REST API

Copyright (C) 2019 Niklas Pfister, contact@omikron.pw

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

from centreon_sdk.centreon import Centreon
from centreon_sdk.network.network import HTTPVerb
from centreon_sdk.objects.base.acl_group import ACLGroupParam


if __name__ == '__main__':
    centreon = Centreon("REST", "HpcuwG4T", "https://centreon.omikron.pw/centreon/api/index.php", verify=False)
    result = centreon.instance_show()
    if isinstance(result, list):
        for item in result:
            print(item.__dict__)
    else:
        print(result)
