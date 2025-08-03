from bitcoinlib.wallets import Wallet
from random_word import RandomWords



def validate_key(passphrase):
    r = RandomWords()
    try:
        a = r.get_random_word()
        wallet = Wallet.create(a, network="bitcoin", keys=passphrase)
        return True
    except Exception as e:
        return False