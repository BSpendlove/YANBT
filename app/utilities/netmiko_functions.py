from app.utilities import generic_responses
from netmiko.ssh_dispatcher import CLASS_MAPPER

def get_netmiko_drivers():
    return generic_responses.data_response(list(CLASS_MAPPER.keys()))