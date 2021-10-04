from PIL import Image
from HashUtils import Hash

import cv2 as cv

import os

import time

class RootFile:
    def __init__(self,path="./"):
        self.path=path

    def FindSubRoot(self):
        def GetSubRootList(path):
            originDirList = os.listdir(path)

            originDirList.sort()
            filetedDirList = []
            for dir in originDirList:
                if os.path.isdir(os.path.join(path, dir)) == True and dir!="__pycache__":
                    '''筛选出文件夹'''
                    filetedDirList.append(dir)
            return filetedDirList

        subRootList=GetSubRootList(self.path)

        for subRoot in subRootList:
            print("=========================================")
            print(subRoot + " Start")
            print("=========================================")

            imgs = Images(subRoot)
            imgs.FindRepeat()

class Images:
    def __init__(self,path="./"):

        self.imagePath = path + "/images"
        self.sub = CompareImage(self.imagePath)
    def FindRepeat(self):

        count=0#控制targetImage

        '''过滤/label中的classes.txt文件'''
        originImageList = os.listdir(self.imagePath)
        originImageList.sort(key=lambda x: (x[:-4]))  # 对文件名按照数字从小到大排序屏蔽最后四位

        print("=========================================")
        print(" Start ")
        print("=========================================")

        originImageList = os.listdir(self.imagePath)
        originImageList.sort(key=lambda x: (x[:-4]))  # 对文件名按照数字从小到大排序屏蔽最后四位

        while count != len(originImageList):
            print("!!count:",count)

            targetName = originImageList[count]

            targetImagePath = "./" + self.imagePath + "/" + targetName
            if not os.path.exists(targetImagePath):
                print("targetImage had been deleted: ",targetName)
                count+=1
                continue
            print(targetImagePath)
            temp=cv.imread(targetImagePath)
            targetImage = Image.fromarray(cv.cvtColor(temp,cv.COLOR_BGR2RGB))

            self.sub.Del(originImageList, targetImage,count)  # 单进程模式测试功能函数是否报错（因为多进程报错不会有提示）

            count+=1


class CompareImage:
    def __init__(self,imagePath):
        self.imagePath=imagePath

    def Del(self,batchList,targetImage,count):
        def _Compare(img1, img2):
            first_image_hasher = Hash(img1)
            second_image_hasher = Hash(img2)
            first_image_score = first_image_hasher.ahash()
            second_image_score = second_image_hasher.ahash()
            diff = 0
            for i in range(len(second_image_score)):
                if first_image_score[i] != second_image_score[i]:
                    diff += 1
            return diff

        subCount = 0
        for imageName in batchList:
            imagePath="./"+self.imagePath+"/"+imageName
            if not os.path.exists(imagePath):
                print("imagePath had been deleted: ",imagePath)
                continue

            temp=cv.imread(imagePath)

            '''解决Image.open打开文件过多的问题，使用cv打开再转成Image格式'''
            image = Image.fromarray(cv.cvtColor(temp,cv.COLOR_BGR2RGB))
            subCount+=1

            score = _Compare(targetImage,image)
            print("\nscore: "+str(score)+" count: "+str(count)+" size" + str(len(batchList))+" sunCount: "+str(subCount))

            if(score<=58 and score>0):
                print("Deleted ",imagePath)
                os.remove(imagePath)



if __name__ =="__main__":
    t1=time.time()
    print("start-------------------------------------")
    # splitRatio = sys.argv[1]
    #mode = sys.argv[1]  # 第二个参数输入修改的文件目录

    root = RootFile()
    root.FindSubRoot()

    print("end--------------------------------------")
    t2=time.time()
    print("Used time: ",t2-t1)



