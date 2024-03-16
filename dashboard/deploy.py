import subprocess
import paramiko
import os

# Define SSH credentials and commands
SSH_HOST = "192.168.0.111"
SSH_USER = "home"
SSH_PASS = "home"

# Define Docker commands
DOCKER_IMAGE_NAME = "dieterverbruggen/dashboard"
DOCKER_COMPOSE_FILE = "/home/home/IOT/dashboard/docker-compose.yml"
LOCAL_COMPOSE_FILE = "docker-compose.yml"  # Local path to docker-compose.yml on your development machine

def build_docker_image():
    print("Building docker image")
    try:
        subprocess.run(["docker", "build", "-t", DOCKER_IMAGE_NAME, "."], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error building Docker image: {e}")
        raise

def push_docker_image():
    print(f"Pushing docker image to {DOCKER_IMAGE_NAME}")
    try:
        subprocess.run(["docker", "push", DOCKER_IMAGE_NAME], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error pushing Docker image: {e}")
        raise

def connect_ssh():
    print(f"Connecting to {SSH_HOST}")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SSH_HOST, username=SSH_USER, password=SSH_PASS)
    return ssh

def execute_ssh_commands(ssh, commands):
    print("Starting SSH commands")
    for cmd in commands:
        print(f"executing ssh cmd: {cmd}")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stdout.read().decode())
        print(stderr.read().decode())
    print("Finished SSH commands")

def upload_docker_compose_file(ssh):
    print(f"Uploading {LOCAL_COMPOSE_FILE} to {SSH_HOST}")
    if not os.path.exists(LOCAL_COMPOSE_FILE):
        print(f"Error: Local file {LOCAL_COMPOSE_FILE} does not exist.")
        return False

    sftp = ssh.open_sftp()
    try:
        sftp.put(LOCAL_COMPOSE_FILE, DOCKER_COMPOSE_FILE)
    except FileNotFoundError as e:
        print(f"Error uploading file: {e}")
        return False
    finally:
        sftp.close()
    
    print(f"Uploaded {LOCAL_COMPOSE_FILE} to {SSH_HOST}:{DOCKER_COMPOSE_FILE}")

def main():
    # Build Docker image
    build_docker_image()

    # Push Docker image
    push_docker_image()

    # Connect to Raspberry Pi over SSH
    ssh = connect_ssh()

    # Upload docker-compose.yml file
    upload_docker_compose_file(ssh)

    # SSH Commands
    commands = [
        "sudo docker compose -f {} down".format(DOCKER_COMPOSE_FILE),
        "sudo docker compose -f {} pull".format(DOCKER_COMPOSE_FILE),
        "sudo docker compose -f {} up -d".format(DOCKER_COMPOSE_FILE)
    ]

    # Execute SSH commands
    execute_ssh_commands(ssh, commands)

    # Close SSH connection
    print("Closing SSH connection")
    ssh.close()

    print("Succesfully deployed application")

if __name__ == "__main__":
    main()