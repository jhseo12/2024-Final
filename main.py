from client.set_enc import *
from client.reg_face import *
from client.ver_face import *
from server.server_face import *
import cv2


encrypt_data()

cap = cv2.VideoCapture(1)  # 아이폰==0

if not cap.isOpened():
    print('camera open failed')
    sys.exit()

while True:
    ret, frame = cap.read()   # bool, img

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('얼굴 등록', frame)

    if cv2.waitKey(1) == 27:   # ESC to break
        cv2.imwrite('reg/1.jpg', frame)
        break

cap.release()   # quit camera
cv2.destroyAllWindows()

cap = cv2.VideoCapture(1)  # 아이폰==0

if not cap.isOpened():
    print('camera open failed')
    sys.exit()

while True:
    ret, frame = cap.read()   # bool, img

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('얼굴 검증', frame)

    if cv2.waitKey(1) == 27:   # ESC to break
        cv2.imwrite('reg/2.jpg', frame)
        break

cap.release()   # quit camera
cv2.destroyAllWindows()

register_face('reg/1.jpg')
verification('reg/2.jpg')

calculate_dist(read_data("server/db/enc_v1.txt"), read_data("server/db/enc_reg.txt"))

context = ts.context_from(read_data("client/key/secret.txt"))
dist_proto = read_data("client/dist.txt")
dist = ts.lazy_ckks_vector_from(dist_proto)
dist.link_context(context)
dist_plain = dist.decrypt()

print(dist_plain)

idx = -1

for i in range(len(dist_plain)):
    if dist_plain[i] > 0.55:
        idx = i
        print(f"얼굴 인증이 완료 되었습니다.")

print(idx) #해당 index를 서버 측으로 보내 valid 여부 판단