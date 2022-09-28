# FastAPI-User-Auth-Demo

- [`FastAPI-Amis-Admin-Demo`](https://github.com/amisadmin/fastapi_amis_admin_demo): An example `FastAPI-Amis-Admin` application.
- [`FastAPI-User-Auth-Demo`](https://github.com/amisadmin/fastapi_user_auth_demo): An example `FastAPI-User-Auth` application.

## Development

### Install command line extension

`pip install fastapi_amis_admin[cli]`

### How to start

1. create your app using `faa new app_name` .
2. writing your apps under `fastapi_user_auth_demo/backend/apps` folder.
3. run your server using `faa run` .

### Documentation

See [Docs](https://docs.amis.work/)

## Deployment

### Install and run:

```shell
# install pdm
pip install --user pdm

# install dependencies
pdm install

# run server
pdm run run
```

## Demo

You can check a online demo [here](http://user-auth.demo.amis.work/).

- admin user: admin----admin
- vip user: vip----vip

### Preview

- Open `http://127.0.0.1:8000/admin/` in your browser:

![Login](https://s2.loli.net/2022/03/20/SZy6sjaVlBT8gin.png)

- Open `http://127.0.0.1:8000/admin/` in your browser:

![ModelAdmin](https://s2.loli.net/2022/03/20/ItgFYGUONm1jCz5.png)

- Open `http://127.0.0.1:6699/admin/docs` in your browser:

![Docs](https://s2.loli.net/2022/03/20/1GcCiPdmXayxrbH.png)