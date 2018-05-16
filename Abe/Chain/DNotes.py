# Copyright(C) 2018 by DNotes developers.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/agpl.html>.

from .DNotesChain import DNotesChain

class DNotes(DNotesChain):
    def __init__(chain, **kwargs):
        chain.name = 'DNotes'
        chain.code3 = 'NOTE'
        chain.address_version = '\x3f'
        chain.script_addr_vers = '\x7d'
        chain.magic = '\xf5\xc1\xaf\xca'
        DNotesChain.__init__(chain, **kwargs)
