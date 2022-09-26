# ins-dm-bot

使用步骤：
1、安装python3
2、在工程目录中pip install -r requirements.txt。程序运行报错时执行下这个初始化代码
3、在要进行群发消息的账号内，复制cookie信息，放到代码中
4、在/infos/usernames.txt中设置好要发送的账户名
5、在run.py中设置好message消息内容。message是一个数组，消息过长的话需要分成多段消息进行发送。
   目前消息内容调整过格式，由于ins的dm无法连续使用多个空格，所以使用了特殊的透明符号来替代空格。
4、设置好上述步骤后，运行软件 python run.py