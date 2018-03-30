# Icarus

> A opensource forum project write with python3 and vue.js

## 如何部署

首先 clone 项目。

```bash
git clone https://github.com/fy0/Icarus.git
```

下面逐项照做即可。

迫于前端安装node_modules等待时间长，在环境安装完成后，前端篇和后端篇可以一起做，以节省时间。


### 环境依赖篇

1. Python 3.6+

Windows上直接使用Anaconda3或者官方版本。

Linux上部分发行版（例如ArchLinux）天然满足要求。

这里只说我的个人环境，Debian/Ubuntu 解决方案：

```bash
# 这个 deadsnakes 的 python 源并非最流行的那一款 Python3.6 第三方源
# 但是细节要比流行的源强得多，举例来说 ubuntu lts 现在内置 Python 3.5
# 安装了那个源之后会发生 3.5 和 3.6 的 pip 互相打架无法并存的情况
# 这个源这点就做的比较好，而且长期维护，很稳定
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install -y python3.6 python3.6-dev python3.6-venv
sudo su -c "curl https://bootstrap.pypa.io/get-pip.py | python3.6"
```


2. NodeJS

建议使用LTS版本的 nodejs，通过包管理器安装：

https://nodejs.org/en/download/package-manager/

```bash
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y nodejs
```


3. PostgreSQL

官方提供了一系列操作系统的安装解决方案：https://www.postgresql.org/download/

Windows下你可以下载安装包，主流Linux可以使用包管理器添加软件源。

还是以ubuntu举例：https://www.postgresql.org/download/linux/ubuntu/

```bash
# 为 ubuntu 16.04 添加 PG 源
sudo su -c "echo 'deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main' > /etc/apt/sources.list.d/pgdg.list"
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | \
  sudo apt-key add -
sudo apt-get update

# 安装PostgreSQL，需要9.6以上版本
sudo apt-get install -y postgresql-10
```


### 后端篇

建议使用 pipenv 进行部署。

```bash
sudo pip3.6 install pipenv
cd Icarus/backend
pipenv install
```

环境装完之后，这样启动服务：
```bash
pipenv shell
python main.py
```

不过有个问题就是 pipenv 太慢，总是在 Locking，给个venv的方案：

```bash
cd Icarus/backend
python3.6 -m venv .
source bin/activate
pip3.6 install requirements.txt
python3.6 main.py
```

这样也能启动服务。


### 前端篇

```bash
# 安装项目依赖
cd Icarus
npm install
```

迫于安装时间过长，国内可以使用cnpm：
```bash
npm install -g cnpm --registry=https://registry.npm.taobao.org
cnpm install
```

如果只是开发环境下看看效果，那么：
```bash
npm run dev
```
然后在浏览器中查看即可。


如果配置域名外部访问，那么：
```bash
npm run build
```
生成dist目录备用。


## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report

# run unit tests
npm run unit

# run e2e tests
npm run e2e

# run all tests
npm test
```

For detailed explanation on how things work, checkout the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).
