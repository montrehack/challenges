# Breaking AES

This repo contains cryptographic challenges that aims to teach various practical attacks on symmetric cryptography. All challenges uses AES, but the same attacks can be used with pretty much any block or stream cipher.

## How to run

### Docker

The easiest way to run the challenges is to install docker and docker-compose. Then, all you need to do is run: 

```bash
docker-compose up
```
All the challenges will be available on http://127.0.0.1:5000 up to http://127.0.0.1-5002.

### Python

The challenges requires python3 to work. The cleanest way too do this is using a virtual envrionment:

```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```
