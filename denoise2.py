# encoding:utf-8
import cv2
import numpy as np
import ocr
# 严苛的去噪版本

# 读入图像并转为灰度图像
src = cv2.imread('src1.png')
img = cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)


# 定义去噪函数
def img_denoise(img,kernel,noise_num):
  output = img.copy()
  # 获取图像大小
  height, width = img.shape[:2]
  # 循环遍历图像每一个像素
  for i in range(1, height - 1):
    for j in range(1, width - 1):
      # 获取kernel x kernel核的像素值
      roi = img[i - 1:i + kernel - 1, j - 1:j + kernel - 1]
      # 判断是否有不少于noise_num个像素近于0，判定为黑色成行或成列，进行保留；否则为孤点，取值255为白
      if np.sum(roi < 130) >= noise_num:
        output[i, j] = img[i, j]
      else:
        output[i, j] = 255
  return output
img = img_denoise(img,3,2)
# 二次过滤
img = img_denoise(img,5,3)

# 显示输出图像
# cv2.imshow('img', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# 去噪图片储存
tmp_png_name = 'tmp.png'
cv2.imwrite(tmp_png_name,img)
# 获取识别结果文本
response = ocr.ocr_course(tmp_png_name)
# 文本整理输入到info.txt
ocr.info_format(response)