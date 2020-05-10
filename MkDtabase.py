import os,dlib,glob,numpy
from skimage import io
import cv2

# 人臉68特徵點模型路徑
predictor_path = "./facedata/data/shape_predictor_68_face_landmarks.dat"

# 人臉辨識模型路徑
face_rec_model_path = "./facedata/data/dlib_face_recognition_resnet_model_v1.dat"

# 比對人臉圖片資料夾名稱
faces_folder_path = "./facedata/image"

# 載入人臉檢測器
detector = dlib.get_frontal_face_detector()

# 載入人臉特徵點檢測器
sp = dlib.shape_predictor(predictor_path)

# 載入人臉辨識檢測器
facerec = dlib.face_recognition_model_v1(face_rec_model_path)

# 比對人臉描述子列表
descriptors = []

# 比對人臉名稱列表
candidate = []

# 針對比對資料夾裡每張圖片做比對:
# 1.人臉偵測
# 2.特徵點偵測
# 3.取得描述子
for f in glob.glob(os.path.join(faces_folder_path, "*.jpg")):
    base = os.path.basename(f)
    # 依序取得圖片檔案人名
    candidate.append(os.path.splitext(base)[ 0])
    img = io.imread(f)

    # 1.人臉偵測
    dets = detector(img, 1)

    for k, d in enumerate(dets):
        # 2.特徵點偵測
        shape = sp(img, d)
 
        # 3.取得描述子，128維特徵向量
        face_descriptor = facerec.compute_face_descriptor(img, shape)
        # 轉換numpy array格式
        v = numpy.array(face_descriptor)
        descriptors.append(v)
numpy.savez('facedata/data/database.npz',descriptors)
numpy.savez('facedata/data/namelist.npz',candidate)