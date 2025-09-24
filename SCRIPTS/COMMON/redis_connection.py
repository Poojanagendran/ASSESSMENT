import paramiko

def create_ssh_client():
    """Initializes and returns a new SSHClient object."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    return ssh

def connect_to_server(ssh, ssh_host, ssh_port, ssh_user, private_key_path):
    """
    Connects to a remote server using SSH.

    Args:
        ssh (paramiko.SSHClient): An instance of SSHClient
        ssh_host (str): Hostname or IP address
        ssh_port (int): SSH port (default is 22)
        ssh_user (str): Username for the SSH connection
        private_key_path (str): Path to the private key file
    """
    try:
        print(f"Connecting to {ssh_host}:{ssh_port} as {ssh_user}...")
        ssh.connect(
            hostname=ssh_host,
            port=ssh_port,
            username=ssh_user,
            key_filename=private_key_path
        )
        print("✅ SSH connection established.")
    except Exception as e:
        print("❌ SSH connection failed:", e)

def run_redis_command(ssh, redis_host, redis_key, redis_method_type, redis_port=None):
    """
    Runs a redis-cli command on a remote server via SSH.

    Args:
        ssh (paramiko.SSHClient): Active SSH connection
        redis_host (str): Redis host (e.g., '127.0.0.1' or 'my.redis.host')
        redis_key (str): Redis key or pattern
        redis_method_type (str): Redis command (e.g., 'KEYS', 'TTL', 'DEL')
        redis_port (int, optional): Redis port (defaults to 6379 if not provided)

    Returns:
        tuple: (output, error)
    """
    # Build redis-cli command with optional port
    if redis_port:
        redis_cmd = f"redis-cli -h {redis_host} -p {redis_port} {redis_method_type} '{redis_key}'"
    else:
        redis_cmd = f"redis-cli -h {redis_host} {redis_method_type} '{redis_key}'"

    print(f"\n🚀 Running Redis command: {redis_cmd}")
    try:
        stdin, stdout, stderr = ssh.exec_command(redis_cmd)
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        return output, error
    except Exception as e:
        print("❌ Failed to execute Redis command:", e)
        return None, str(e)

def close_ssh_connection(ssh):
    """Closes the SSH connection."""
    if ssh:
        ssh.close()
        print("\n🔒 SSH connection closed.")
