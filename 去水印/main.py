import cv2
import numpy as np
import os


def extract_images_from_folder(folder_path):
    """
    从文件夹中读取所有PNG图像
    """
    images = []
    filenames = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".png"):
            image_path = os.path.join(folder_path, filename)
            image = cv2.imread(image_path)
            # 设置大小800*600
            image = cv2.resize(image, (800, 600))
            enhanced_image = enhance_colors(image)
            # 保存
            # cv2.imwrite(f"out/{filename}", enhanced_image)
            images.append(enhanced_image)
            filenames.append(filename)
    return images, filenames


def detect_watermark(image, watermark_template):
    """
    使用特征匹配检测图像中是否存在水印
    """
    # 转换为灰度图像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_template = cv2.cvtColor(watermark_template, cv2.COLOR_BGR2GRAY)

    # 使用ORB特征检测器
    orb = cv2.ORB_create()

    # 检测关键点和描述符
    keypoints1, descriptors1 = orb.detectAndCompute(gray_image, None)
    keypoints2, descriptors2 = orb.detectAndCompute(gray_template, None)

    # 创建BFMatcher对象
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # 匹配描述符
    matches = bf.match(descriptors1, descriptors2)

    # 根据匹配距离排序
    matches = sorted(matches, key=lambda x: x.distance)

    # 设定一个距离阈值，过滤较好的匹配
    threshold = 70  # 可能需要调整此阈值
    good_matches = [m for m in matches if m.distance < threshold]

    # 检查匹配的数量是否足够
    if len(good_matches) > 80:  # 你可以调整这个阈值
        return True, good_matches
    else:
        return False, None


def enhance_colors(image):
    """
    增强图像中的其他颜色，降低黑、白、灰的影响
    """
    # 将图像从BGR转换到HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 创建一个掩码，选择非黑白灰色区域
    # 定义黑色、白色和灰色的范围
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 30])

    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 30, 255])

    lower_gray = np.array([0, 0, 31])
    upper_gray = np.array([180, 30, 199])

    # 创建掩码
    mask_black = cv2.inRange(hsv_image, lower_black, upper_black)
    mask_white = cv2.inRange(hsv_image, lower_white, upper_white)
    mask_gray = cv2.inRange(hsv_image, lower_gray, upper_gray)

    # 合并掩码
    mask = mask_black | mask_white | mask_gray

    # 反转掩码
    mask = cv2.bitwise_not(mask)

    # 增强非黑白灰区域的饱和度和亮度
    hsv_image[:, :, 1] = np.where(mask > 0, hsv_image[:, :, 1] * 2, hsv_image[:, :, 1])  # 增强饱和度
    hsv_image[:, :, 2] = np.where(mask > 0, hsv_image[:, :, 2] * 1.5, hsv_image[:, :, 2])  # 增强亮度

    # 将图像从HSV转换回BGR
    enhanced_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
    return enhanced_image


def main(folder_path, watermark_image_path):
    """
    主函数，执行从文件夹读取图像并检测水印的流程
    """
    images, filenames = extract_images_from_folder(folder_path)
    watermark_template = cv2.imread(watermark_image_path)

    for i, image in enumerate(images):
        has_watermark, good_matches = detect_watermark(image, watermark_template)
        if has_watermark:
            print(f"Watermark detected in image {filenames[i]} with {len(good_matches)} good matches")
        else:
            print(f"No watermark detected in image {filenames[i]}")


if __name__ == "__main__":
    folder_path = "img"  # 替换为包含PNG文件的文件夹路径
    watermark_image_path = "test.jpg"  # 替换为你的水印图像路径
    main(folder_path, watermark_image_path)
