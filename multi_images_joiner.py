from PIL import Image
import os
import argparse

def JoinFunc(imagesFolder, orientation):
	# step 1.
	# 获取 imagesFolder 下所有图片的名字
	# os.walk() 通过在目录树中游走，输出在目录中的文件名，next(os.walk(imagesFolder))返回值依次为 root, dirs, files
	# next() 返回迭代器的下一个项目
	imagesName = next(os.walk(imagesFolder))[2]
	print(imagesName)

	# step 2.
	# 读入所有图片
	# os.getcwd() 用于返回当前工作目录
	# images 为 list 类型
	images = []
	for imageName in imagesName:
	    imagePath = os.path.join(os.getcwd(), imagesFolder, imageName)
	    if isinstance(imagePath, str):
	        images.append(Image.open(imagePath))
	    else:
	        raise Exception('Invalid! Use image path!')


	# step 3.
	# 根据拼接方向（水平、垂直）进行拼接
	# box 的类型为 tuple，中文名为元组，与list的不同之处在于元素不可修改
	offset = 0
	output_width = 0
	output_height = 0
	offsets = [0]
	resize_factors = []
	if orientation == 'vertical':
		I = 1
		output_width = max( [image.size[0] for image in images] )
		for image in images:
			resize_factor = output_width / image.size[0]
			resize_factors.append(resize_factor)
			offsets.append(int(image.size[1]*resize_factor))

			output_height = sum([int(image.size[1]*resize_factor), output_height])
	else:
		I = 0
		output_height = max( [image.size[1] for image in images] ) 
		for image in images:
			resize_factor = output_height / image.size[1]
			resize_factors.append(resize_factor)
			offsets.append(int(image.size[0]*resize_factor))

			output_width = sum( [int(image.size[0]*resize_factor), output_width] )
		
	joinImage = Image.new('RGBA', (output_width, output_height))

	count = 0
	for image in images:
		offset = sum(offsets[0:count+1])
		resize_factor = resize_factors[count]
		if orientation == 'vertical':
			box = (0, offset)
		else:
			box = (offset, 0)
		reImage = image.resize((int(image.size[0]*resize_factor), int(image.size[1]*resize_factor)))
		joinImage.paste(reImage, box)
		count += 1

	return joinImage

if __name__ == '__main__':
	parser = argparse.ArgumentParser( description = 'Join multiple images along vertical or horizontal direction.' )
	
	# 将待拼接的所有图片保存于文件夹 JoinImages 下
	parser.add_argument('--imagesFolder', default = 'JoinImages')

	# 指定拼接方向
	parser.add_argument('--orientation', default = 'vertical')

	args = parser.parse_args()
	joinImage = JoinFunc(args.imagesFolder, args.orientation)
	joinImage.save(os.path.join(os.getcwd(), 'joinImage'+args.imagesFolder+args.orientation+'.png'))
	print('Successfully join these images!')



