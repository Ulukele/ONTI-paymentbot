from web3 import Web3, HTTPProvider, exceptions
from utils import config
from decimal import Decimal


web3 = Web3(HTTPProvider(config.WEB3_PROVIDER))

CHAIN_ID = web3.eth.chainId


def checksum(address):
    return Web3.toChecksumAddress(address) 


def check_pub_key(address):
    if not address.lower().startswith('0x'):
        raise ValueError(f'address should start with 0x: {address}')
    return checksum(address)


def toWei(amount: float, unit: str):
    return web3.toWei(amount, unit)


def fromWei(amount: Decimal, unit: str):
    #if unit == "ether":
    #    a = str(a).zfill(18)

    return Decimal(web3.fromWei(int(amount), unit))

def getBalance(address):
    return web3.eth.getBalance(address)