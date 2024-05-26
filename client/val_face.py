# Recommend to try in python 3.10.3
import tenseal as ts
import base64

'''
    VALIDATION
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


def check_valid():
    context = ts.context_from(read_data("client/key/secret.txt"))
    dist_proto = read_data("client/dist.txt")
    dist = ts.lazy_ckks_vector_from(dist_proto)
    dist.link_context(context)
    dist_plain = dist.decrypt()

    print(dist_plain)

    idx = -1

    for i in range(len(dist_plain)):
        if dist_plain[i] < -0.1:
            idx = i


    if idx == -1:
        return False
    else:
        print(idx)
        return True

print(check_valid())

# 서버로 dist_plain을 보냄

# 암호화된 연산 값이랑 원본 상태에서의 연산 값의 오차가 0.00001 미만인지 확인 필요
