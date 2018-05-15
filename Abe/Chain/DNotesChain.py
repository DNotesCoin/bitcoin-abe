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

from . import BaseChain
from .. import deserialize

class DNotesChain(BaseChain):
    """
    The DNtoes blockchain.
    """
    def ds_parse_transaction(chain, ds):
        return DNotesChain.parse_Transaction(ds)

    def parse_Transaction(vds):
        d = {}
        start_pos = vds.read_cursor
        d['version'] = vds.read_int32()
        d['nTime'] = vds.read_uint32()
        n_vin = vds.read_compact_size()
        d['txIn'] = []
        for i in xrange(n_vin):
            d['txIn'].append(deserialize.parse_TxIn(vds))
        n_vout = vds.read_compact_size()
        d['txOut'] = []
        for i in xrange(n_vout):
            d['txOut'].append(DNotesChain.parse_TxOut(vds))
        d['lockTime'] = vds.read_uint32()
        d['__data__'] = vds.input[start_pos:vds.read_cursor]
        return d

    def parse_TxOut(vds):
        d = {}
        d['value'] = vds.read_int64()
        d['invoice'] = vds.read_string()
        d['scriptPubKey'] = vds.read_bytes(vds.read_compact_size())
        return d

    def block_header_hash(chain, header):
        b = chain.parse_block_header(header)
        if (b['version'] > 6):
            from .. import util
            return util.double_sha256(header)
        import x13_hash
        return x13_hash.getPoWHash(header)

    def ds_parse_block_header(chain, ds):
        d = {}
        header_start = ds.read_cursor
        d['version'] = ds.read_int32()
        d['hashPrev'] = ds.read_bytes(32)
        d['hashMerkleRoot'] = ds.read_bytes(32)
        d['nTime'] = ds.read_uint32()
        d['nBits'] = ds.read_uint32()
        d['nNonce'] = ds.read_uint32()
        numAddresses = ds.read_compact_size()
        for i in xrange(numAddresses):
            ds.read_compact_size() #variant type
            ds.read_bytes(20) #address
            ds.read_int64() #balance
        header_end = ds.read_cursor
        d['__header__'] = ds.input[header_start:header_end]
