### 深入剖析Kubernetes
本地阅读html格式的电子书

如果需要看别的电子书，只要替换`deep_study_Kubernetes/public/resource/html`里面的html文件然后刷新页面就行了

使用vue3+go渲染到页面 ，go占用8089端口，vue占用3333端口

#### 启动方式
clone源代码
```angular2html
git clone https://github.com/setking/deep_study_Kubernetes.git
```
cd到`deep_study_Kubernetes/public/resource/html`，运行python脚本，需要预先安装python 3.12,在运行命令前先备份源文件
```angular2html
python .\scripts.py
```
回到`deep_study_Kubernetes`目录下，启动服务，需要nodejs 23以上版本
```angular2html
pnpm install
pnpm run dev
```