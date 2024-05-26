# Recommend to try in python 3.10.3
import tenseal as ts
from deepface import DeepFace
import base64

'''
    VERIFICATION
'''

def write_data(file_name, data):

    if type(data) == bytes:
        #bytes to base64
        data = base64.b64encode(data)

    with open(file_name, 'wb') as f:
        f.write(data)


def read_data(file_name):
    with open(file_name, "rb") as f:
        data = f.read()

    #base64 to bytes
    return base64.b64decode(data)


def verification(img_path):
    img_embedding = DeepFace.represent(img_path, model_name = 'Facenet') # Facenet 모델로 이미지 임베딩
    img_embedding = img_embedding[0]['embedding']

    context = ts.context_from(read_data("client/key/secret.txt"))
    # TenSEAL 라이브러리의 ckks_vector() 함수에 변환된 데이터 전달
    enc_v1 = ts.ckks_vector(context, img_embedding)

    enc_v1_proto = enc_v1.serialize()

    write_data("server/db/enc_v1.txt", enc_v1_proto)

    del context, enc_v1, enc_v1_proto