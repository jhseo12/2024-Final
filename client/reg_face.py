# Recommend to try in python 3.10.3
import tenseal as ts
from deepface import DeepFace
import base64

'''
    REGISTRATION
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


def register_face(reg_path):
    reg_embedding = DeepFace.represent(reg_path, model_name = 'Facenet')
    reg_embedding = reg_embedding[0]['embedding']

    context = ts.context_from(read_data("client/key/secret.txt"))
    # ckks_vector() 함수에 임베딩 된 데이터 전달
    enc_reg= ts.ckks_vector(context, reg_embedding)
    enc_reg_proto = enc_reg.serialize()

    write_data("server/db/enc_reg.txt", enc_reg_proto) # Server로 encryption된 데이터 전달

    del context, enc_reg, enc_reg_proto

