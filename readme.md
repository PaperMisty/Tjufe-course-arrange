# 这是针对天津财经大学课程编排的程序
## Author：PhoebeZhennan；


# Part 1  
%如果你愿意手动将课程信息（信息较少时建议手动），以要求格式（参见Tips 1）输入到info.txt文件中，则可跳过此部分程序%

运行denoise.py，该程序将你的课程表(src.png)进行图像降噪，输出到tmp.png  
并将自动利用百度文本识别API从tmp.png提取文本，得到的课程信息输入到info.txt中	

但是！  
课程表画面太糙，识别技术还不是非常成熟，需要打开info.txt验证课程信息是否正确（参见Tips 2）！

# Part 2  
1.如果课程信息正确，则运行info2ics.py文件，自动将课程编排到GMT.ics文件（格林威治时间）和Beijing.ics文件（北京时间）中  
2.将你需要的.ics文件添加到你的日历软件中即可（目前我用的是Google Calendar，似乎没什么问题）  


# Tips
0.安装必要的package，比如opencv-python（我现在版本是python3.10，numpy等）  

1.课表截取范围需要和src.png一致!!!  
并且将你的课表命名为src.png作为替换

2.课程信息要求格式(除了XXX其余都需要仔细校对)：  
XXXXXXXXX]课程名字 老师名字 1-17 二[5XXX]双 N3218  
比如：  
[B0320020]智慧物流 刘畅 1-17 四[3-4节] N3229  
并且程序认为第一行一般是注释，是不计入的   

3.仅用于学术交流，不支持任何盈利活动  
