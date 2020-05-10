import dlib,numpy
import cv2
import poimgLib.poImgLib as po

# 人臉68特徵點模型路徑
predictor_path = "./facedata/data/shape_predictor_68_face_landmarks.dat"
# 人臉辨識模型路徑
face_rec_model_path = "./facedata/data/dlib_face_recognition_resnet_model_v1.dat"
# 載入人臉檢測器
detector = dlib.get_frontal_face_detector()
# 載入人臉特徵點檢測器
sp = dlib.shape_predictor(predictor_path)
# 載入人臉辨識檢測器
facerec = dlib.face_recognition_model_v1(face_rec_model_path)
#載入安全人員名單
candidate = numpy.load('facedata/data/namelist.npz')['arr_0']
descriptors = numpy.load('facedata/data/database.npz')['arr_0']

# 選擇第一隻攝影機
cap = cv2.VideoCapture(0)  
#調整預設影像大小，預設值很大，很吃效能
cap.set(cv2. CAP_PROP_FRAME_WIDTH, 650)
cap.set(cv2. CAP_PROP_FRAME_HEIGHT, 500)

d_test = []
while(cap.isOpened()):
  # 從攝影機擷取一張影像
  ret, img = cap.read()
  dets = detector(img, 1)

  dist = []
  for k, d in enumerate(dets):
    shape = sp(img, d)
    face_descriptor = facerec.compute_face_descriptor(img, shape)
    d_test = numpy.array(face_descriptor)

    x1 = d.left()
    y1 = d.top()
    x2 = d.right()
    y2 = d.bottom()
    # 以方框標示偵測的人臉
    cv2.rectangle(img, (x1, y1), (x2, y2), ( 0, 255, 0), 4, cv2. LINE_AA)
 
    # 計算歐式距離(相似度)
    for i in descriptors:
        dist_ = numpy.linalg.norm(i -d_test)
        dist.append(dist_)

  if len(dist) > 0:
  # 將比對人名和比對出來的歐式距離組成一個dict
    c_d = zip(candidate,dist)
    # 根據歐式距離由小到大排序
    cd_sorted = sorted(c_d, key = lambda d:d[1])

    # 取得最短距離就為辨識出的人名
    if cd_sorted[0][1] < 0.5:
      # 將辨識出的人名印到圖片上面
      cv2.putText(img, cd_sorted[0][0], (x1, y1), cv2. FONT_HERSHEY_SIMPLEX , 1, ( 255, 255, 255), 2, cv2. LINE_AA)
    else:
      cv2.imwrite('WohAreYou.jpg', img)
      po.postimg('WohAreYou.jpg')
      descriptors = numpy.append(descriptors,[d_test],axis=0)
      candidate = numpy.append(candidate,["WhoAreYou"],axis=0)
  
  cv2.namedWindow('Face Recognition', cv2.WINDOW_NORMAL)
  cv2.imshow( "Face Recognition", img)

  # 若按下 q 鍵則離開迴圈
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
# 釋放攝影機
cap.release()
# 關閉所有 OpenCV 視窗
cv2.destroyAllWindows()









'''


for k, d in enumerate(dets):
    shape = sp(img, d)
    face_descriptor = facerec.compute_face_descriptor(img, shape)
    d_test = numpy.array(face_descriptor)

    x1 = d.left()
    y1 = d.top()
    x2 = d.right()
    y2 = d.bottom()
    # 以方框標示偵測的人臉
    cv2.rectangle(img, (x1, y1), (x2, y2), ( 0, 255, 0), 4, cv2. LINE_AA)
 
  # 計算歐式距離(相似度)
    for i in descriptors:
        dist_ = numpy.linalg.norm(i -d_test)
        dist.append(dist_)
    
    if len(dist) > 0:
      # 將比對人名和比對出來的歐式距離組成一個dict
      c_d = zip(candidate,dist)

      # 根據歐式距離由小到大排序
      cd_sorted = sorted(c_d, key = lambda d:d[1])

      # 取得最短距離就為辨識出的人名
      if cd_sorted[0][1] < 0.4:
        # 將辨識出的人名印到圖片上面
        cv2.putText(img, rec_name, (x1, y1), cv2. FONT_HERSHEY_SIMPLEX , 1, ( 255, 255, 255), 2, cv2. LINE_AA)
      else:
        cv2.imwrite('WohAreYou.jpg', img)
        po.postimg('WohAreYou.jpg')





cv2.namedWindow('Face Recognition', cv2.WINDOW_NORMAL)
cv2.imshow( "Face Recognition", img)'''
