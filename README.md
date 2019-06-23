# Chinese-Handwrting-Recognition

These codes apply for Chinese Handwriting recognition. 

The whole codes include three parts
1. Handwriting.py: scrap picture of Chinese handwriting from Internet
2. tail.py: change the picture to statisfy the special problem, which will be the trainset of CNN(transferlearning)
3. cv.py: recognise with selective search and filter the frame with CNN and the position. (using OpenCV)

VGG16.h5 save the weight of CNN (transfer learning from VGG16)
