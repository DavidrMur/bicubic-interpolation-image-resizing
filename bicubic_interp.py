import cv2
import numpy as np
import math

def cubic(A, B, C, D, t):
	a = -A/2.0 + (3.0*B)/2.0 - (3.0*C)/2.0 + D/2.0
	b = A - (5.0*B)/2.0 + 2.0*C - D/2.0
	c = -A/2.0 + C/2.0
	d = B

	return a*t*t*t + b*t*t + c*t + d

def bicubic(img, new_x, new_y, imgWidth, imgHeight):

	x = (new_x * imgWidth) - 0.5
	y = (new_y * imgHeight) - 0.5

	xint = int(x)
	yint = int(y)

	derv_x = x - math.floor(x)
	derv_y = y - math.floor(y)
	value = []

	if (xint >= imgWidth): 
		xint = imgWidth - 1

	if (yint >= imgHeight):
		yint = imgHeight - 1		



	for i in range(3):
		col0 = cubic(img[max(xint-1,0),max(yint-1,0)][i], img[min(xint,imgWidth-1),max(yint-1,0)][i], img[min(xint+1,imgWidth-1),max(yint-1,0)][i], img[min(xint+2,imgWidth-1),max(yint-1,0)][i], derv_x)
		col1 = cubic(img[max(xint-1,0),yint][i], img[min(xint,imgWidth-1),yint][i], img[min(xint+1,imgWidth-1),yint][i], img[min(xint+2,imgWidth-1),yint][i], derv_x)
		col2 = cubic(img[max(xint-1,0),min(yint+1,imgHeight-1)][i], img[min(xint,imgWidth-1),min(yint+1,imgHeight-1)][i], img[min(xint+1,imgWidth-1),min(yint+1,imgHeight-1)][i], img[min(xint+2,imgWidth-1),min(yint+1,imgHeight-1)][i], derv_x)
		col3 = cubic(img[max(xint-1,0),min(yint+2,imgHeight-1)][i], img[min(xint,imgWidth-1),min(yint+2,imgHeight-1)][i], img[min(xint+1,imgWidth-1),min(yint+2,imgHeight-1)][i], img[min(xint+2,imgWidth-1),min(yint+2,imgHeight-1)][i], derv_x)
		value.append(cubic(col0,col1,col2,col3, derv_y))

	return value	


def resize(img, ratio):
	imgWidth,imgHeight,C = img.shape


	dstHeight = imgHeight*ratio
	dstWidth = imgWidth*ratio

	dstImg = np.zeros((dstWidth, dstHeight, 3))

	for i in range(dstHeight):

		new_y = float(i) / float(dstHeight-1)

		for j in range(dstWidth):
			new_x = float(j) / float(dstWidth-1)

			sample = bicubic(img, new_x, new_y, imgWidth, imgHeight)

			dstP = [0,0,0]
			dstP[0] = max(sample[0],0)
			dstP[1] = max(sample[1],0)
			dstP[2] = max(sample[2],0)
			dstImg[j, i] += dstP

	
	
	return dstImg
if __name__ == '__main__':
    ratio = 2
    img = cv2.imread('img_example_lr.png')

    new_img = resize(img, ratio)

    print('done')
    cv2.imwrite('bicubic_img_example_lr.png', new_img)			

