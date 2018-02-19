import socket
from construct import (
    Adapter, Array, Byte, Embedded, Struct, Int8ub, Int16ub)

alfred_tlv = Struct(
    'type' / Int8ub,
    'version' / Int8ub,
    'length' / Int16ub
)

alfred_announce_master = Struct(
    'alfred_tlv' / alfred_tlv,
)

alfred_request = Struct(
    'alfred_tlv' / Embedded(alfred_tlv),
    'requested_type' / Int8ub,
    'transaction_id' / Int16ub
)

alfred_status_end = Struct(
    'alfred_tlv' / alfred_tlv,
    'transaction_id' / Int16ub,
    'number_of_packets' / Int16ub
)


class MACAdapter(Adapter):

    def _encode(self, obj, context, path):
        pass

    def _decode(self, obj, context, path):
        return ':'.join(format(s, '02x') for s in obj)


alfred_data_block = Struct(
    'source_mac_address' / MACAdapter(Byte[6]),
    'type' / Int8ub,
    'version' / Int8ub,
    'length' / Int16ub,
    'data' / Array(
        lambda ctx: ctx.length,
        Byte)
)

'''
Container:
    type = 65
    version = 0
    length = 12
    transaction_id = 1
    sequence_number = 0
    source_mac_address_0-3 = 1583140554
    source_mac_address_4-5 = 37720
    data_0 = 29281
    data_1 = 1936745061
'''

alfred_push_data = Struct(
    'alfred_tlv' / alfred_tlv,
    'transaction_id' / Int16ub,
    'sequence_number' / Int16ub,
    'alfred_data' / Array(
        # lambda ctx: ctx.alfred_tlv.length,
        1,
        alfred_data_block)
)

socket_address = '/var/run/alfred.sock'

tlv = alfred_tlv.build({
    'type': 2,
    'version': 0,
    'length': 3
})

request = alfred_request.build({
    'type': 2,
    'version': 0,
    'length': 3,
    'requested_type': 65,
    'transaction_id': 1
})

status = alfred_status_end.build({
    'alfred_tlv': {
        'type': 3,
        'version': 0,
        'length': 4
    },
    'transaction_id': 1,
    'number_of_packets': 2
})

with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
    s.connect(socket_address)
    s.send(request)
    s.send(status)
    data = s.recv(1024)

print(alfred_push_data.parse(data))
