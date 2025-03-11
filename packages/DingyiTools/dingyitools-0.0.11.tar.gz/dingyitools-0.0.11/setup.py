import setuptools #导入setuptools打包工具
 
 
setuptools.setup(
    name="DingyiTools", # 用自己的名替换其中的YOUR_USERNAME_
    version="0.0.11",    #包版本号，便于维护版本
    author="Dingyi",    #作者，可以写自己的姓名
    author_email="dingyi0427@126.com",    #作者联系方式，可写自己的邮箱地址
    description="Dingyi tools", #包的简述
    url="https://github.com/littleDy0427/DingyiTools",    #自己项目地址，比如github的项目地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3.6',    #对python的最低版本要求
)