from functools import partial
from hashlib import sha3_256
from hmac import HMAC
from typing import (Union,
                    Type,
                    Callable,
                    Dict,
                    Tuple)

from Cryptodome.Cipher import AES
from Cryptodome.Util import Counter
from ecdsa import (SECP256k1,
                   SigningKey,
                   VerifyingKey)
from ecdsa.curves import Curve

from . import aes
from .coding import (decode_hex,
                     big_endian_to_int)
from .hashes import (scrypt_hash,
                     keccak_256_hash)

HashFunctionType = Callable[..., HMAC]
KeyType = Union[SigningKey,
                VerifyingKey]
KeyClsType = Union[Type[SigningKey],
                   Type[VerifyingKey]]


def hex_bytes_to_key(key_cls: KeyClsType,
                     hex_bytes: bytes,
                     *,
                     curve: Curve = SECP256k1,
                     hash_function: HashFunctionType = sha3_256
                     ) -> KeyType:
    return key_cls.from_string(hex_bytes,
                               curve=curve,
                               hashfunc=hash_function)


hex_bytes_to_signing_key = partial(hex_bytes_to_key,
                                   SigningKey)
hex_bytes_to_verifying_key = partial(hex_bytes_to_key,
                                     VerifyingKey)


def load_signing_key(key_json: Dict[str, Union[str, int, dict]],
                     password: str) -> bytes:
    try:
        crypto = key_json['crypto']
    except KeyError:
        crypto = key_json['Crypto']

    aes_key, head_mac_bytes = derived_key_parts(password=password,
                                                kdf_params=crypto['kdfparams'])
    cipher_text = decode_hex(crypto['ciphertext'])
    validate_mac(cipher_text=cipher_text,
                 head_mac_bytes=head_mac_bytes,
                 predicted_mac=decode_hex(crypto['mac']))

    cipher_params = crypto['cipherparams']
    initial_value = initial_value_str_to_int(string=cipher_params['iv'])
    counter = Counter.new(nbits=128,
                          initial_value=initial_value,
                          allow_wraparound=True)
    return aes.decrypt(text=cipher_text,
                       key=aes_key,
                       counter=counter,
                       mode=AES.MODE_CTR)


def derived_key_parts(*,
                      password: str,
                      kdf_params: Dict[str, Union[int, str]]
                      ) -> Tuple[bytes, bytes]:
    derived_key = scrypt_hash(password,
                              salt=decode_hex(kdf_params['salt']),
                              buffer_length=kdf_params['dklen'],
                              p=kdf_params['p'],
                              r=kdf_params['r'],
                              n=kdf_params['n'])
    if len(derived_key) < 32:
        err_msg = 'Derived key must be at least 32 bytes long.'
        raise ValueError(err_msg)
    return derived_key[:16], derived_key[16:32]


def validate_mac(*,
                 cipher_text: bytes,
                 head_mac_bytes: bytes,
                 predicted_mac: bytes) -> None:
    mac_bytes = head_mac_bytes + cipher_text
    mac = keccak_256_hash(mac_bytes).digest()
    if mac != predicted_mac:
        err_msg = ('MAC mismatch. '
                   'Password seems to be incorrect.')
        raise ValueError(err_msg)


def initial_value_str_to_int(string: str) -> int:
    return big_endian_to_int(decode_hex(string))
