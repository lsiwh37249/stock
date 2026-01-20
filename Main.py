from pykis import PyKis, KisAuth, KisQuote, KisBalance

class Main():
    def __init__(self):
        # 실전투자용 PyKis 객체를 생성합니다.
        #kis = PyKis("secret.json", keep_token=True)
        #kis = PyKis(KisAuth.load("secret.json"), keep_token=True)

        # 모의투자용 PyKis 객체를 생성합니다.
        self.kis = PyKis("secret.json", "virtual_secret.json", keep_token=True)
        self.kis = PyKis(KisAuth.load("secret.json"), KisAuth.load("virtual_secret.json"), keep_token=True)

    # 시세 조회 
    def quote(self):
        stock = self.kis.stock("MVDA")
        quote: KisQuote = stock.quote()
        print(quote)

    def account(self):
        account = self.kis.account()
        balance: KisBalance = account.balance()
        print(repr(balance))

    def order(self):
        

    def main(self):
        
        pass

# main
if __name__ == "__main__":
    m = Main()
    m.main()