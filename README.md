# Python fastapi fly.io deploy damvflaskapitest


#### files structure :

    ❯ tree -L 2 -I 'gambar-petunjuk|README.md'

        ├── Dockerfile
        ├── app.py
        ├── arial.ttf
        ├── fly.toml
        └── requirements.txt

        0 directories, 5 files

### &#x1FAB6; code :

- python 


- Dockerfile


### &#x1F31F; Test application with Docker container



&#x1F535; list :




#### application :

- CURL :


- Postman :


#### Reset containers :

    ❯ docker rm -f $(docker ps -aq) && docker rmi -f $(docker images -q)






---

<p align="center">
    <img src="./gambar-petunjuk/fly-io-logo.svg" alt="fly-io-logo" style="display: block; margin: 0 auto;">
</p>


---

## Stages in deploying the application to fly.io


#### code :

- toml [Tom's Obvious Minimal Language]

        ❯ vim fly.toml


### check version :

    ❯ flyctl version


### &#x1F530; create Apps :

    ❯ flyctl apps create --name damvflaskapitest

check and watch for updates on the fly.io console dashboard



### &#x1F530; deploy Apps :

    ❯ flyctl deploy


check and watch for updates on the fly.io console dashboard


### &#x1F530; check

    ❯ flyctl status

    ❯ flyctl ips list

    ❯ flyctl services list


### &#x1F530; open :

    ❯ flyctl open


#### &#x1F535; postman : 


---

<p align="center">
    <img src="./gambar-petunjuk/well_done.png" alt="well_done" style="display: block; margin: 0 auto;">
</p>


---


### Remove Apps :



---