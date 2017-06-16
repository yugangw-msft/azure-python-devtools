# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import hashlib
import inspect
import math
import os
import base64
import zlib


def get_qualified_test_name(test_object, method_name):
    """
    Get the fully qualified (module + method) name of a test.

    Example of a fully qualified test name:
    test_mgmt_network.test_public_ip_addresses
    """
    _, filename = os.path.split(inspect.getsourcefile(type(test_object)))
    module_name, _ = os.path.splitext(filename)
    return '{0}.{1}'.format(module_name, method_name)


def get_resource_name(name_prefix, identifier):
    """
    Append a suffix to the name, based on a prefix and an identifier.

    A good identifier is the fully qualified test name.
    We use a checksum of the identifier so that each test gets different
    resource names, but each test will get the same name on repeat runs,
    which is needed for playback.
    Most resource names have a length limit, so we use a crc32.
    """
    checksum = zlib.adler32(identifier) & 0xffffffff
    name = '{}{}'.format(name_prefix, hex(checksum)[2:]).rstrip('L')
    return name


def create_random_name(prefix='aztest', length=24):
    if len(prefix) > length:
        raise 'The length of the prefix must not be longer than random name length'

    padding_size = length - len(prefix)
    if padding_size < 4:
        raise 'The randomized part of the name is shorter than 4, which may not be able to offer ' \
              'enough randomness'

    random_bytes = os.urandom(int(math.ceil(float(padding_size) / 8) * 5))
    random_padding = base64.b32encode(random_bytes)[:padding_size]

    return str(prefix + random_padding.decode().lower())


def get_sha1_hash(file_path):
    sha1 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            sha1.update(data)

    return sha1.hexdigest()
