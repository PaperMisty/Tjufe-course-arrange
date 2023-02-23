# encoding:utf-8
import cv2
import numpy as np
import ocr
# 读入图像并转为灰度图像
src = cv2.imread('src.png')
img = cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)

# 获取图像大小
height, width = img.shape[:2]

# 复制一张图像作为输出图像
output = img.copy()

# 循环遍历图像每一个像素
for i in range(1, height - 1):
  for j in range(1, width - 1):
    # 获取3x3卷积核的像素值
    roi = img[i - 1:i + 7, j - 1:j + 7]
    # 判断是否有不少于2个像素近于0，判定为黑色成行或成列，进行保留；否则为孤点，取值255为白
    if np.sum(roi < 130) >= 4:
      output[i, j] = img[i, j]
    else:
      output[i, j] = 255

# 显示输出图像
cv2.imshow('output', output)

# 图像挂起
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# 去噪图片储存
tmp_png_name = 'tmp.png'
cv2.imwrite(tmp_png_name,output)
# 获取识别结果文本
response = ocr.ocr_course(tmp_png_name)
# 文本整理输入到info.txt
ocr.info_format(response)