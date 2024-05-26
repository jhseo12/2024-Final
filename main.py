from client.set_enc import *
from client.reg_face import *
from client.ver_face import *
from server.server_face import *
import cv2


''' 암호키 생성 '''
encrypt_data()

''' 최초 얼굴 등록(ESC키로 캡쳐) '''
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

''' 검증용 얼굴 등록(ESC로 캡쳐) '''
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


''' 얼굴 검증 단계 '''
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


'''
    서버 측에서 랜덤하게 지정된 인덱스를 출력하고 128차원의 배열을 출력한다.
    valid한 index라면 해당 인덱스를 출력, 아니라면 -1을 출력
    valid하면 얼굴 인증 완료문 출력
'''
