#!/usr/bin/env python

import paramiko

hostname = "127.0.0.1"
port = "22"
#username = "root"
pkey_file = "/home/mkarytka/.ssh/id_rsa"
password_ssh_key = "92791140301k_"

if __name__ == "__main__":
#    paramiko.util.log_to_file('paramiko.log')
    key = paramiko.RSAKey.from_private_key_file(pkey_file, password_ssh_key)
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.connect(hostname, port)
    stdin, stdout, stderr = s.exec_command("ifconfig")
    print stdout.read()
    s.close()
