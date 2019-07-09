import numpy as np
import cv2
# print(cv2.__version__)

# x = int(input("Number of ryws:"))

class Minerator:
    def __init__(self, x = 5):
        self.x = x
        self.step = int(512/(x+1))
        self.img = np.full((512,512,3), 255, dtype=np.uint8)
        self.font = cv2.FONT_HERSHEY_SIMPLEX


    def draw_cells(self):
        color = (0,0,255)
        #cv2.putText(img,'0',(int(512 / x + 10), int(512 / x - 10)), font, 3,(0,0,0),2,cv2.LINE_AA)
        for i in range(1, self.x+1):
            coord = self.step*i
            cv2.line(self.img,(0,coord),(511,coord),color,1)
            cv2.line(self.img,(self.step * i,0),(self.step * i, 511),color,1)
            cv2.putText(self.img,str(i),(int(50 / self.x) + coord, int(512 / (self.x+1) - int(50 / self.x))), self.font, 10 / self.x,(0,0,0),2,cv2.LINE_AA)
            cv2.putText(self.img,str(i),(int(50 / self.x), int(512 / (self.x+1) - int(50 / self.x)) + coord), self.font, 10 / self.x,(0,0,0),2,cv2.LINE_AA)


    def draw_mask(self,mask):
        color = (200,200,200)
        for i in range (len(mask)):
            for j in range(len(mask[0])):
                if mask[i][j] == 0:
                    cv2.rectangle(self.img, (self.step * (j+1), self.step * (i+1)), (self.step * (j+2), self.step * (i+2)), color, thickness=-1)
                if type(mask[i][j]) is int and 0 < mask[i][j] < 9:
                    cv2.rectangle(self.img, (self.step * (j+1), self.step * (i+1)), (self.step * (j+2), self.step * (i+2)), color, thickness=-1)
                    cv2.putText(self.img,str(mask[i][j]),(int(50 / self.x) + self.step * (j+1), int(512 / (self.x+1) - int(50 / self.x)) + self.step * (i+1)), self.font, 10 / self.x,(0,0,0),2,cv2.LINE_AA)
                if type(mask[i][j]) is int and mask[i][j] == 9:
                    cv2.rectangle(self.img, (self.step * (j+1), self.step * (i+1)), (self.step * (j+2), self.step * (i+2)), color, thickness=-1)
                    cv2.putText(self.img,'*',(int(50 / self.x) + self.step * (j+1), int(512 / (self.x+1) - int(50 / self.x)) + self.step * (i+1)), self.font, 10 / self.x,(0,0,0),2,cv2.LINE_AA)

    def get_image(self, mask):
        self.img = np.full((512,512,3), 255, dtype=np.uint8) 
        self.x = len(mask)
        self.step = int(512/(self.x+1))
        self.draw_mask(mask)
        self.draw_cells()
        return self.img

                    

# mask = [[0,0,0,0,0],
#         [0,0,0,'#',0],
#         [0,0,2,0,0],
#         [0,0,0,0,0],
#         [0,0,0,4,0]]
# imager = Minerator()

# cv2.imshow('Dimas', imager.get_image(mask))
# cv2.waitKey(0)
# cv2.destroyAllWindows()