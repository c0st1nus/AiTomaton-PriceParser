import paramiko
import json
import os


def create_dump(backup_file_path):
    hostname = os.getenv("SSH_HOSTNAME")
    username = os.getenv("SSH_USERNAME")
    password = os.getenv("SSH_PASSWORD")
    container_name = 'mysqlparser'
    local_backup_dir = '/sql_dump'

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname, username=username, password=password)
        
        dump_command = f"docker exec {container_name} sh -c 'mysqldump -u root -proot parser > {backup_file_path}'"
        stdin, stdout, stderr = ssh.exec_command(dump_command)
        exit_status = stdout.channel.recv_exit_status()

        if exit_status == 0:
            print("Backup created inside the container.")
        else:
            print(f"Error during backup: {stderr.read().decode()}")

        copy_command = f"echo \"{password}\" | sudo -S docker cp {container_name}:{backup_file_path} {local_backup_dir}"
        
        stdin, stdout, stderr = ssh.exec_command(copy_command)
        exit_status = stdout.channel.recv_exit_status()

        if exit_status == 0:
            print(f"Backup copied to {local_backup_dir}.")
        else:
            print(f"Error during file copy: {stderr.read().decode()}")
        
    finally:
        ssh.close()