# Recommend to try in python 3.10.3
import tenseal as ts
import base64

'''
    공개키, 비밀키 생성 및 저장
    서버로는 공개키만 전달
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

def encrypt_data():
    # Initialization
    context = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=16384,
        coeff_mod_bit_sizes=[40, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 40]
    )

    context.generate_galois_keys()
    context.global_scale = 2 ** 30

    secret_context = context.serialize(save_secret_key=True)
    write_data("client/key/secret.txt", secret_context)  # Client로 secret key 전달
    context.make_context_public()
    public_context = context.serialize()
    write_data("client/key/public.txt", public_context)  # Client로 public key 전달
    write_data("server/key/public.txt", public_context)  # Server로 public key 전달
    del context, secret_context, public_context