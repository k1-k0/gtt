from typing import Tuple, List
import ipaddress


class NoPortsForScanException(Exception):
    pass


def parse_args(args: List) -> Tuple[ipaddress.IPv4Address, List[int]]:
    """Returns arguments converted to the correct type"""
    ip_address = ipaddress.ip_network(args[1])
    ports = convert_ports_to_int(args[2:])

    return (ip_address, ports)

def convert_ports_to_int(ports: List[str]) -> List[int]:
    if not ports:
        raise NoPortsForScanException("Waiting for any ports to scan")
    return [int(port) for port in ports]
