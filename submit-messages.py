#!/usr/bin/env python
import pika
import sys
import socket
import ConfigParser
import gnupg

## Read configuration files
config = ConfigParser.RawConfigParser(allow_no_value=True)
config.read('mq.cfg')

config_pgp = ConfigParser.RawConfigParser(allow_no_value=True)
config_pgp.read('gpg.cfg')

gpg = gnupg.GPG(gnupghome=config_pgp.get("gpg","home_dir"))
gpg.enconding = 'utf-8'

gpg_passphrase=config_pgp.get("gpg","passphrase")
gpg_sign_key_id=config_pgp.get("gpg","sign_key_id")

# Read MQ config items
mq_user = config.get("mq","user")
mq_pass = config.get("mq","password")
mq_hostname = config.get("mq","host")
mq_general_key = config.get("mq","routingkeys")
mq_exchange = config.get("mq","exchange")
mq_port = config.getint("mq","port")
mq_queue = config.get("mq","queue")


# Set pika credentials
credentials = pika.PlainCredentials(mq_user,mq_pass)

# Set up connection
connection = pika.BlockingConnection(pika.ConnectionParameters(
                        mq_hostname,mq_port,'/',credentials))

channel = connection.channel()

#channel.exchange_declare(exchange=mq_exchange,
#                         type='direct')

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

receiver = {'receiver': severity}

signed_message = gpg.sign(message, passphrase=gpg_passphrase, keyid=gpg_sign_key_id)

channel.basic_publish(exchange=mq_exchange,
                      routing_key='',
                      body=signed_message.data,
                      properties = \
                              pika.BasicProperties(headers = receiver))

print " [x] Sent Signed Message (%r) %r:%r" % (gpg_sign_key_id,severity, message)
connection.close()
