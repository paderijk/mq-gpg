#!/usr/bin/env python
#
# Creating keys for the GPG Signing

import ConfigParser
import gnupg

## Read configuration files
config = ConfigParser.RawConfigParser(allow_no_value=True)
config.read('gpg.cfg')

gpg = gnupg.GPG(gnupghome=config.get("gpg","home_dir"))
gpg.enconding = 'utf-8'

gpg_key_type = config.get("gpg","key_type")
gpg_key_length = config.getint("gpg","key_length")
gpg_name_real = config.get("gpg","name_real")
gpg_name_email = config.get("gpg","name_email")
gpg_key_expire = config.get("gpg","key_expire")
gpg_passphrase = config.get("gpg","passphrase")

input_data = gpg.gen_key_input(key_type=gpg_key_type, key_length=gpg_key_length, subkey_length=gpg_key_length, name_real=gpg_name_real,name_email=gpg_name_email, passphrase=gpg_passphrase)

key = gpg.gen_key(input_data)

