#### 指定项目使用python 版本
FROM python:3.9.17-alpine
#### 镜像来源 https://registry.hub.docker.com/_/python
LABEL maintainer "yxh <xianhe_yan@sina.com>"
#### 指定工作目录
WORKDIR /usr/src/app
COPY ./haikangapi.py /usr/src/app/
COPY ./requirements.txt ./
RUN apk update && \
    apk add --no-cache build-base libffi-dev openssl-dev && \
    pip install --upgrade pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

EXPOSE 8000
#### 启动uvicorn 项目

CMD ["uvicorn", "haikangapi:app", "--host", "0.0.0.0", "--port", "8000"]
