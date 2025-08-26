import cv2
from pathlib import Path

image_paths = sorted(Path("images").glob("*.jpg"))

for image_path in image_paths:
    img = cv2.imread(str(image_path))
    img = cv2.resize(img, (800, 600))

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # # extract the sky
    # hsv_mask = cv2.inRange(hsv, lowerb=(80, 100, 0), upperb=(120, 255, 255)) # type: ignore

    # brightness = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # brightness_mask = cv2.inRange(brightness, 150, 255) # type: ignore

    # threshold, _ = cv2.threshold(brightness, 150, 255, cv2.THRESH_BINARY) # type: ignore

    # mask = cv2.bitwise_and(hsv_mask, brightness_mask)

    blue = img[:, :, 0]
    top_rows_blue = blue[0:100, :]
    mean_top_blue = int(top_rows_blue.mean())
    _, thresh_blue = cv2.threshold(blue, mean_top_blue - 20, 255, cv2.THRESH_BINARY) # type: ignore

    saturation = hsv[:, :, 1]
    _, thresh_saturation = cv2.threshold(saturation, 50, 255, cv2.THRESH_BINARY) # type: ignore

    _, low_sat = cv2.threshold(saturation, 10, 255, cv2.THRESH_BINARY_INV) # type: ignore

    thresh_saturation = cv2.bitwise_or(thresh_saturation, low_sat)

    hue = hsv[:, :, 0]
    mask_green = cv2.inRange(hue, 35, 85) # type: ignore

    mask = cv2.bitwise_and(thresh_blue, thresh_saturation)
    mask = cv2.bitwise_and(mask, cv2.bitwise_not(mask_green))

    cv2.imshow("blue", blue)
    cv2.imshow("mask", mask)


    # green = img[:, :, 1]

    # diff = cv2.subtract(blue, green)

    # # aply sobel y operator
    # sobel_y = cv2.Sobel(blue, cv2.CV_64F, 0, 1, ksize=5)
    # sobel_y = cv2.convertScaleAbs(sobel_y)
    # _, blue = cv2.threshold(sobel_y, 150, 255, cv2.THRESH_BINARY) # type: ignore

    # # equalize the blue channel
    # # blue_eq = cv2.equalizeHist(blue)
    
    # cv2.imshow("Image", img)
    # cv2.imshow("hsv", hsv[:, :, 2])
    # cv2.imshow("Diff", diff)
    # cv2.imshow("Mask", blue)
    # cv2.imshow("Sobel", sobel_y)
    
    key = cv2.waitKey(0) & 0xFF

    if key == ord('q'):
        break

cv2.destroyAllWindows()
