import cv2
import numpy as np

def remove_watermark(image_path, mask_path, output_path):
    # 加载图像
    image = cv2.imread(image_path)
    # 更换尺寸800*600
    image = cv2.resize(image, (800, 600))
    # 加载水印掩码图像
    mask = cv2.imread(mask_path, 0)

    # 图像修复（inpainting）去除水印
    result = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)

    # 保存去除水印后的图像
    cv2.imwrite(output_path, result)

# 示例使用
image_path = 'img/img_3.png'
mask_path = 'test.jpg'
output_path = 'out.jpg'

remove_watermark(image_path, mask_path, output_path)
