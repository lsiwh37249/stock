from pykis import PyKis, KisAuth

class KisAuth:
    def KisAuth():
        auth = KisAuth(
            # HTS 로그인 ID  예) soju06
            id="YOUR_HTS_ID",
            # 앱 키  예) Pa0knAM6JLAjIa93Miajz7ykJIXXXXXXXXXX
            appkey="YOUR_APP_KEY",
            # 앱 시크릿 키  예) V9J3YGPE5q2ZRG5EgqnLHn7XqbJjzwXcNpvY . . .
            secretkey="YOUR_APP_SECRET",
            # 앱 키와 연결된 계좌번호  예) 00000000-01
            account="00000000-01",
            # 모의투자 여부
            virtual=False,
        )
        # 안전한 경로에 시크릿 키를 파일로 저장합니다.
        auth.save("secret.json")
        
        return auth


if __name__=="__main__":
    
    # 실전투자용 PyKis 객체를 생성합니다.
    kis = PyKis("secret.json", keep_token=True)
    kis = PyKis(KisAuth.load("secret.json"), keep_token=True)

    # 모의투자용 PyKis 객체를 생성합니다.
    kis = PyKis("secret.json", "virtual_secret.json", keep_token=True)
    kis = PyKis(KisAuth.load("secret.json"), KisAuth.load("virtual_secret.json"), keep_token=True)