from pykis import PyKis, KisAuth as PyKisAuth
import os

class KisAuth:  
    def __init__(self):
        self.appkey = os.environ["REAL_APPKEY"]
        self.appsecretkey = os.environ["REAL_APPSECRETKEY"]
        self.hts_id = os.environ["HTS_ID"]
        self.account = os.environ["ACCOUNT"]
        self.auth = None

    def create_auth(self):
        """인증 정보를 생성하고 secret.json 파일로 저장합니다."""
        self.auth = PyKisAuth(
            # HTS 로그인 ID  예) soju06
            id=self.hts_id,
            # 앱 키  예) Pa0knAM6JLAjIa93Miajz7ykJIXXXXXXXXXX
            appkey=self.appkey,
            # 앱 시크릿 키  예) V9J3YGPE5q2ZRG5EgqnLHn7XqbJjzwXcNpvY . . .
            secretkey=self.appsecretkey,
            # 앱 키와 연결된 계좌번호  예) 00000000-01
            account=self.account,
            # 모의투자 여부
            virtual=False,
        )
        print(self.auth)
        # 안전한 경로에 시크릿 키를 파일로 저장합니다.
        self.auth.save("secret.json")

        return self.auth

    def main(self): 
        import sys
        # secret.json 파일이 없으면 생성합니다.
        if not os.path.exists("secret.json"):
            print("secret.json 파일이 없습니다. 인증 정보를 생성합니다...")
            self.create_auth()

        # 실전투자용 PyKis 객체를 생성합니다.
        try:
            kis = PyKis(PyKisAuth.load("secret.json"), keep_token=True)
            print("PyKis 객체가 성공적으로 생성되었습니다.")
        except Exception as e:
            print(f"PyKis 객체 생성 중 오류 발생: {e}")
            sys.exit(1)
        return kis

if __name__=="__main__":
    kis = KisAuth()
    kis.main()