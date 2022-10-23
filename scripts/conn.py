import paramiko
import time

command=["sudo -S -p '' chmod u+x docker-install.sh && ./docker-install.sh"]

class Installation:

    def __init__(self, host, username, password) -> None:
        self.host = host
        self.username = username
        self.password = password

    def execute(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.host, username=self.username, password=self.password)

        
        stdin, stdout, stderr = client.exec_command("sudo -S -p '' chmod u+x docker-install.sh && ./docker-install.sh", get_pty=True)
        stdin.write(self.password + "\n")
        stdin.flush()

        time.sleep(1)
        for line in stdout:
            print(line)
            #print(line.strip('\n'), end="")

        client.close()

    def copy_file(self):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        print (f"Connecting to {self.host} with username={self.username}...")
        t = paramiko.Transport(self.host, 22)
        t.connect(username=self.username,password=self.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        print (f"Copying file: 'docker-install.sh' to path: /home/{self.username}/")
        sftp.put('docker-install.sh', 'docker-install.sh')
        sftp.close()
        t.close()


if __name__ == "__main__":
    install = Installation(host="172.16.131.141", username = "block", password = "localhost")
    install.copy_file()
    install.execute()