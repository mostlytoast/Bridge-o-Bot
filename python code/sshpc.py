import paramiko
hostname = "10.0.0.147"
username = "pi"
password = "cheese01"
commands = [
    ""
]
# initialize the SSH client
client = paramiko.SSHClient()
# add to known hosts
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(hostname=hostname, username=username, password=password)

except:
    print("[!] Cannot connect to the SSH Server")
    exit()
# execute the commands
for command in commands:
    print("="*50, command, "="*50)
    stdin, stdout, stderr = client.exec_command(command)
    print(stdout.read().decode())
    err = stderr.read().decode()
    if err:
        print(err)
print('a')