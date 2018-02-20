import socket
from construct import (
    Adapter,
    Array,
    Byte,
    Bytes,
    Embedded,
    Struct,
    Switch,
    Int8ub,
    Int16ub
)

alfred_tlv = Struct(
    'type' / Int8ub,
    'version' / Int8ub,
    'length' / Int16ub
)

alfred_announce_master = Struct()

alfred_request = Struct(
    'requested_type' / Int8ub,
    'transaction_id' / Int16ub
)

alfred_status_end = Struct(
    'transaction_id' / Int16ub,
    'number_of_packets' / Int16ub
)

alfred_status_error = Struct(
    'transaction_id' / Int16ub,
    'error_code' / Int16ub
)

alfred_mode_switch = Struct(
    'mode' / Int8ub
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
    'data' / Bytes(lambda ctx: ctx.length)
)

alfred_push_data = Struct(
    'transaction_id' / Int16ub,
    'sequence_number' / Int16ub,
    'alfred_data' / Array(1, alfred_data_block)
)

alfred_packet = Struct(
    'alfred_tlv' / alfred_tlv,
    'packet_body' / Switch(lambda ctx: ctx.alfred_tlv.type, {
        0: alfred_push_data,
        1: alfred_announce_master,
        2: alfred_request,
        3: alfred_status_end,
        4: alfred_status_error,
        5: alfred_mode_switch
    })
)

socket_address = '/var/run/alfred.sock'

request = alfred_packet.build({
    'alfred_tlv': {
        'type': 2,
        'version': 0,
        'length': 3,
    },
    'packet_body': {
        'requested_type': 65,
        'transaction_id': 1
    }
})

status = alfred_packet.build({
    'alfred_tlv': {
        'type': 3,
        'version': 0,
        'length': 4
    },
    'packet_body': {
        'transaction_id': 1,
        'number_of_packets': 2
    }
})

with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
    s.connect(socket_address)
    s.sendall(request)
    s.sendall(status)
    data = s.recv(65535)

print(alfred_packet.parse(data))
