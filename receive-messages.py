#!/usr/bin/env python
import pika
import sys
import socket
import ConfigParser
import gnupg

## Read configuration files
config = ConfigParser.RawConfigParser()
config.read('mq.cfg')

config_pgp = ConfigParser.RawConfigParser()
config_pgp.read('gpg.cfg')

gpg = gnupg.GPG(gnupghome=config_pgp.get("gpg","home_dir"))
gpg.enconding = 'utf-8'

gpg_sign_key_id=config_pgp.get("gpg","sign_key_id")


# Read config items
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

hostname_fqdn = (socket.gethostname()).lower()
hostname_short = hostname_fqdn.split(".")[0]

receive_keys = [ hostname_fqdn, hostname_short] 
receive_keys.extend(mq_general_key.split(","))

# Bind to routing keys
for receivers in receive_keys:
    channel.queue_bind(exchange=mq_exchange,
                       queue=mq_queue,
                       routing_key='',
                       arguments = {'receiver': receivers})

print "Receiving for routing key: %r" % (receive_keys)
print ' [*] Waiting for logs. To exit press CTRL+C'

def callback(ch, method, properties, body):
    verified = gpg.verify(body)
    if verified.trust_level is not None and verified.trust_level >= verified.TRUST_FULLY:
        print(' [ACK] Message received trust level: %s' % verified.trust_text)
        print('       %s ' % gpg.decrypt(body))
    else:
        print(' [ERR] Untrusted message received')

channel.basic_consume(callback,
                      queue=mq_queue,
                      no_ack=True)


try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

    connection.close()

sys.exit(0)

