from pykis import PyKis, KisAuth
import os

def create_auth():
    """인증 정보를 생성하고 secret.json 파일로 저장합니다."""
    appkey = os.environ["REAL_APPKEY"]
    appsecretkey = os.environ["REAL_APPSECRETKEY"]
    auth = KisAuth(
        # HTS 로그인 ID  예) soju06
        id="lsiwh327",
        # 앱 키  예) Pa0knAM6JLAjIa93Miajz7ykJIXXXXXXXXXX
        appkey=appkey,
        # 앱 시크릿 키  예) V9J3YGPE5q2ZRG5EgqnLHn7XqbJjzwXcNpvY . . .
        secretkey=appsecretkey,
        # 앱 키와 연결된 계좌번호  예) 00000000-01
        account="74018844-01",
        # 모의투자 여부
        virtual=False,
    )
    print(auth)
    # 안전한 경로에 시크릿 키를 파일로 저장합니다.
    auth.save("secret.json")
    
    return auth


if __name__=="__main__":
    import sys
    
    # secret.json 파일이 없으면 생성합니다.
    if not os.path.exists("secret.json"):
        print("secret.json 파일이 없습니다. 인증 정보를 생성합니다...")
        create_auth()
    
    # 실전투자용 PyKis 객체를 생성합니다.
    try:
        kis = PyKis(KisAuth.load("secret.json"), keep_token=True)
        print("PyKis 객체가 성공적으로 생성되었습니다.")
    except Exception as e:
        print(f"PyKis 객체 생성 중 오류 발생: {e}")
        sys.exit(1)