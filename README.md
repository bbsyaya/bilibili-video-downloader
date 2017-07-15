# bilibili-video-downloader
download video from bilibili for batch.[http://www.bilibili.com](http://www.bilibili.com)

## 1. 项目结构说明
- lib/

	爬虫核心代码
- out/

	结果文件
- main.py

	主程序入口
- requirements.txt

	python依赖库

- download.sh

	下载脚本

## 2. 项目运行说明
## Linux系统
### 1. 搭建python开发环境
- 推荐安装pyenv和pyenv-virtualenv, 完全隔离不同项目的开发环境.
- pyenv的安装, 请参考[https://github.com/yyuu/pyenv](https://github.com/yyuu/pyenv)
- pyenv-virtualenv的安装, 请参考[https://github.com/yyuu/pyenv-virtualenv](https://github.com/yyuu/pyenv-virtualenv)
- 当然, 你也可以直接使用系统默认安装的python进行操作, 不过平时要养成良好的习惯, 推荐使用前面的方式操作.
- 安装python虚拟环境

  		pyenv virtualenv 2.7.9 env_bilibili_video_downloader_2.7.9        // 2.7.9: 虚拟环境的python版本, env_bilibili_video_downloader_2.7.9: 虚拟环境

  其中, 安装不同版本的python:

	  pyenv install 2.7.9         // 指定版本号

### 2. 运行项目

      pyenv activate env_bilibili_video_downloader_2.7.9       // 切换到项目对应的虚拟环境
      pip install -r requirements.txt                 		  // 安装依赖库
      python main.py                                         // 运行项目

  下载视频:

	  ./download.sh

## 3. 如何贡献
- fork
- modify
- pull request

## 4. TODO
可以适当对结果文件进行分片, 多进程下载, 可以加快速度.
