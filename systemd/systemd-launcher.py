import os
import socket
import subprocess
import systemd.daemon

def systemd_socket_response():
    """
    Accepts every connection of the listen socket provided by systemd, send the
    HTTP Response 'OK' back.
    """
    try:
        fds = systemd.daemon.listen_fds()
    except ImportError:
        fds = [3]

    for fd in fds:
        sock = socket.fromfd(fd, socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0)

        try:
            while True:
              conn, addr = sock.accept()
              conn.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nOK\n")
              p1 = subprocess.Popen(
                  ['/usr/bin/ansible-playbook', 'refresh.yml'],
                  stdout=subprocess.PIPE,
                  stderr=subprocess.STDOUT,
                  cwd='/home/centos/feeders')
              for stdout_line in iter(p1.stdout.readline, ""):
                  conn.send(stdout_line)
              p1.stdout.close()
              conn.send(b"\r\n\r\n")
              conn.close()
        except socket.timeout:
            pass
        except OSError as e:
            # Connection closed again? Don't care, we just do our job.
            print(e)

if __name__ == "__main__":
   if os.environ.get("LISTEN_FDS", None) != None:
        systemd_socket_response()
