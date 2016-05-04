# MQ GPG

## About

This is a proof-of-concept to send/receive messages over RabbitMQ combined with GPG Signing.

## Prerequisites

* Need to have a full functioning [RabbitMQ](https://www.rabbitmq.com/) Environment
* Installed the following Python modules
  * `pika`
  * `sys`
  * `socket`
  * `ConfigParser`
  * `gnupg`

## Configuration

The scripts have two configuration files.

* `mq.cfg`
* `gpg.cfg`

### mq.cfg

This file contains the credentials and details on how to connect to the MQ broker.

```
[mq]
user=broker-1
password=S3cr3tPassWord-ChangeMe
host=mq.local.example.com
routingkeys=GENERAL,Broadcast
exchange=testing
port = 5672
queue=hello
```

Please ensure it meet your settings.

### gpg.cfg

This configuration file contains the gpg specific configuration

```
[gpg]
home_dir=gpg-dir
key_type=RSA
key_length=2048
name_real=Command issuer
name_email=signing_sender@example.com
key_expire=30d
passphrase=ThisIsAnExamplePleaseChange
sign_key_id=A171959F
```

You can identify the `sign_key_id` using the following command:

```bash
gpg --no-default-keyring --keyring ./pubring.gpg --list-keys | grep ^pub | awk '{ print $2 }' | awk -F\/ '{ print $2 }'
```

To create a key pair you can run the script `create-gpg-keys.py`, which also read the `gpg.cfg` file.

## Receive messages

Starting the script `receive-messages.py` will bind to the MQ Channels and collect the messages, verify signature and if it's a valid signature display it.

## Submit messages

Starting the script `submit-messages.py` will submit what is given as option after the command, for example:

```
submit-messages.py This is a test
```

The script will sign the message and put it in the message queue.

## Todo

There are still some small things that needs to be done:
* Split the `mq.cfg` and the `gpg.cfg`, so the credentials for GPG are only know by the `submit-messages.py` script

## Acknowledgement

The start of the script(s) for RabbitMQ come original from the tutorials on the RabbitMQ Website - https://www.rabbitmq.com/getstarted.html
