import face_recognition
import cv2
import time
from tqdm import tqdm
# from PIL import Image

def get_biggest_face(face_locations):
    '''返回面积最大的face location'''
    faceareas = []
    for location in face_locations:
        top, right, bottom, left = location
        area = (bottom - top) * (right - left)
        faceareas.append(area)
        # print(location,area)
        # face_image = cover_image[top:bottom, left:right]
        # # pil_image = Image.fromarray(face_image)
        # # pil_image.show()

    max_area = max(faceareas)
    max_area_index = faceareas.index(max_area)
    return face_locations[max_area_index]



def work(cover_image,teaser_Video):
    input_movie = cv2.VideoCapture(teaser_Video)
    video_length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))
    cover_image = face_recognition.load_image_file(cover_image)

    print('封面人脸识别中，可能需要一分钟左右')
    cover_face_locations = face_recognition.face_locations(cover_image,number_of_times_to_upsample=2,model='cnn')
    print('识别到人脸数: ',len(cover_face_locations))
    # print(cover_face_locations)
    cover_face_location = get_biggest_face(cover_face_locations)
    cover_face_encoding = face_recognition.face_encodings(cover_image,[cover_face_location])[0]
    # print(cover_face_encoding)

    print('开始比对视频和封面')
    pbar = tqdm(total = video_length)
    frame_number = 0
    video_face_count = 0
    face_distances = 0

    
    while frame_number < video_length:
        input_movie.set(1,frame_number)
        ret, frame = input_movie.read()
        rgb_frame = frame[:, :, ::-1]
        videoface_encoding = face_recognition.face_encodings(rgb_frame)
        if len(videoface_encoding) > 0:
            distance = face_recognition.face_distance(videoface_encoding,cover_face_encoding)[0]
            if distance < 0.85:
                video_face_count += 1
                face_distances += distance
            frame_number += 20
            pbar.update(20)            
            # print(distance)
        frame_number += 5
        pbar.update(5)
    
    print('总对比次数: ',video_face_count,'平均差值(越小代表越接近): ',face_distances/video_face_count)



# work('OAE-099-coverImage.jpg','OAE-099-teaservideo.mp4')


