import paramiko
import json
import os


def create_dump(filename):
    hostname = os.getenv("SSH_HOSTNAME")
    username = os.getenv("SSH_USERNAME")
    password = os.getenv("SSH_PASSWORD")
    save_path = os.getenv("SAVE_PATH")

    container_name = 'mysqlparser'
    local_backup_dir = '/sql_dump'

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname, username=username, password=password)
        
        dump_command = f"mysqldump -u aitomaton -ptrdYTvtrC756c parser > {save_path}/{filename}"
        stdin, stdout, stderr = ssh.exec_command(dump_command)
        exit_status = stdout.channel.recv_exit_status()

        if exit_status == 0:
            print("Backup created")
        else:
            print(f"Error during backup: {stderr.read().decode()}")
        
    finally:
        ssh.close()