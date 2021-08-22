# PyTorch Deployment
> A template for rapid deployment of PyTorch models.

<details>
<summary><strong>点击以展开中文 README</strong></summary>
<div>

## 功能
+ [x] API.
+ [x] Web 前端.
+ [x] 支持图像转换模型.
+ [ ] 支持图像分类模型.
+ [ ] 支持图像生成模型.

## 演示
![StarGANv2_AFHQ](https://cdn.jsdelivr.net/gh/justsong-lab/images/misc/starganv2_afhq.gif)

## 部署步骤
1. 安装依赖：`pip install -r requirements.txt`
2. 启动服务，你有以下选择：
    1. `flask run -p 3000`，注意该方式性能较差。
    2. 使用 Gunicorn：
        1. 安装 Gunicorn：`pip install gunicorn`
        2. 启动应用：`gunicorn -b 127.0.0.1:3009 app:app`

请注意，模型的权重是从 Github 上下载的，如果你的服务器无法正常访问 Github，请手动下载权重并放到 data 文件夹下。

目前内置的模型：
+ starganv2_afhq.ckpt：https://github.com/justsong-lab/releases/releases/download/v0.1/starganv2_afhq.ckpt

</div>
</details>

## Features
+ [x] API.
+ [x] Web frontend.
+ [x] Support image translation models.
+ [ ] Support image classification models.
+ [ ] Support image generation models.

## Demo
![StarGANv2_AFHQ](https://cdn.jsdelivr.net/gh/justsong-lab/images/misc/starganv2_afhq.gif)

