# Recommend to try in python 3.10.3
import tenseal as ts
import numpy as np
import base64
import random


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


def f(x):
    x2 = x*x
    x3 = -0.5*x
    x3 *= x2
    x3 += 1.5*x
    return x3


def calculate_dist(enc_v1_proto, enc_reg_proto):
    context = ts.context_from(read_data("server/key/public.txt"))
    enc_v1 = ts.lazy_ckks_vector_from(enc_v1_proto)
    enc_v1.link_context(context)

    enc_reg = ts.lazy_ckks_vector_from(enc_reg_proto)
    enc_reg.link_context(context)

    threshold = 100
    reverse_max_possible = 1 / 300

    dist = enc_v1 - enc_reg

    dist *= dist
    dist = dist.matmul(np.ones((128,128), dtype=np.float64)) # 모든 요소를 더한 값이 모든 요소에 동일하게 저장됨

    dist -= threshold
    dist *= reverse_max_possible
    dist = f(f(f(dist)))
    dist = -dist + 1
    dist *= 1 / 2

    idx = random.randint(0, 127)
    # idx = 3
    print(idx) # 랜덤하게 설정된 인덱스 값 (0~127)을 DB에 저장
    # mask = np.ones(128, dtype=np.float64)
    mask = np.zeros(128, dtype=np.float64)
    mask[idx] = 1

    dist *= mask

    alpha = 0.52
    beta = 0.7

    # 지정된 index를 제외한 나머지 index에 대한 값은 감마 분포를 따르도록 설정
    err = np.random.gamma(alpha, 1/beta, size=128)

    while (err > 0.55).any():  # 값이 0.55를 넘어가면 다시 뽑습니다.
        err = np.random.gamma(alpha, 1/beta, size=128)

    err[idx] = 0
    dist += err

    write_data("client/dist.txt", dist.serialize())

    return dist
