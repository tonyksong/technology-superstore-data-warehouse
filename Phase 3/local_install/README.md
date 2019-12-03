# Local Install Instructions
#### CSE6400 Database Project:  S&E Tech Store

## Pre-requisites
0. (no op) you already have pulled the entire flask code and SQL schema via the earlier git clone which is why you're reading this file in the first place

1. Install docker for your laptop from [here](https://www.docker.com/products/docker-desktop)
2. run the following commands:
```
docker pull store/oracle/mysql-enterprise-server:5.7
```
_Example:_
```bash
knail1s-MacBook-Pro.local [knail1]$ docker pull store/oracle/mysql-enterprise-server:5.7
5.7: Pulling from store/oracle/mysql-enterprise-server
Digest: sha256:fcf8ce705beef7919dba0b1522175264813185a1f469eb93a8fc5778a25f9cdd
Status: Image is up to date for store/oracle/mysql-enterprise-server:5.7
```

```bash
docker pull python:3.7.0-alpine
```
*alpine is a much lighter container than the 1GB python official

_Example:_
```bash
knail1s-MBP.home [knail1]$ docker pull python:3.7.0-alpine
3.7.0-alpine: Pulling from library/python
4fe2ade4980c: Pull complete
7cf6a1d62200: Pull complete
b66090d9998c: Pull complete
e0dc374a57ff: Pull complete
eb580e903ff2: Pull complete
Digest: sha256:e12594db7297ebf9d9478ba60373e0181974f373016e7495926a7da81bda323b
Status: Downloaded newer image for python:3.7.0-alpine
knail1s-MBP.home [knail1]$
```

