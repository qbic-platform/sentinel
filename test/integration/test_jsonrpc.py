import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from qbicd import QbicDaemon
from qbic_config import QbicConfig


def test_qbicd():
    config_text = QbicConfig.slurp_config_file(config.qbic_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'00000ecbba09ad38ab68c367923732bf8e6f1e9868127d842ceecd330af9c38f'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000a384129e1401ebba7f117e554378642ba7e6fa8eb627f3e47a3a1631e74'

    creds = QbicConfig.get_rpc_creds(config_text, network)
    qbicd = QbicDaemon(**creds)
    assert qbicd.rpc_command is not None

    assert hasattr(qbicd, 'rpc_connection')

    # Qbic testnet block 0 hash == 00000ecbba09ad38ab68c367923732bf8e6f1e9868127d842ceecd330af9c38f
    # test commands without arguments
    info = qbicd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert qbicd.rpc_command('getblockhash', 0) == genesis_hash
