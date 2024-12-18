import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st
import datetime

# 주식 코드와 이름 매핑 (예시로 KOSPI 주요 종목 20개)
STOCK_LIST = {
    "Samsung Electronics": "005930.KS",
    "Naver": "035420.KQ",
    "SK hynix": "000660.KS",
    "Hyundai Motor": "051910.KS",
    "POSCO": "005380.KS",
    "Kakao": "035720.KQ",
    "LG Electronics": "066570.KQ",
    "Celltrion": "068270.KQ",
    "Hyundai Mobis": "012330.KS",
    "Korean Air": "003490.KS",
    "Amorepacific": "090430.KS",
    "KT": "030200.KS",
    "LG Chem": "051910.KS",
    "SK Telecom": "017670.KS",
    "SK Innovation": "096770.KQ",
    "Lotte Chemical": "011170.KS",
    "KakaoBank": "323410.KQ",
    "Hana Financial": "086790.KS",
    "Samsung Biologics": "207940.KQ",
    "KB Financial": "105560.KQ"
}

# 데이터 수집
def fetch_stock_data(ticker, start_date, end_date):
    return yf.download(ticker, start=start_date, end=end_date)

# 조건식: n일 연속 상승 여부 확인
def is_rising(df, days=5, threshold=0.05):
    """n일 연속 종가 상승 여부를 확인합니다."""
    df['Change'] = df['Close'].pct_change()  # 종가 상승률 계산
    rolling_rise = df['Change'].rolling(days).apply(lambda x: (x >= threshold).all(), raw=True)
    return rolling_rise

# 그래프 시각화 함수
def plot_stock_graph(stock_data):
    """주식 데이터를 이용해 그래프를 시각화합니다."""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(stock_data.index, stock_data['Close'], label="Close Price", color="blue")
    ax.scatter(
        stock_data.index, 
        stock_data['Close'], 
        c=stock_data['Rising'].apply(lambda x: 'red' if x else 'blue'),
        label="Rising Condition Met",
        alpha=0.5
    )
    ax.set_title(f"Stock Price with Rising Condition")
    ax.set_xlabel("Date")
    ax.set_ylabel("Close Price")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

# Streamlit 인터페이스
def main():
    # 제목
    st.title("Stock Price Analysis")

    # 사용자 선택을 위한 주식 이름 (STOCK_LIST에서 키를 선택)
    selected_stock_name = st.selectbox("Select Stock", list(STOCK_LIST.keys()))
    selected_stock_code = STOCK_LIST[selected_stock_name]  # 선택된 이름에 해당하는 종목 코드

    # 날짜 입력: datetime.date 객체로 변환
    start_date = st.date_input("Start Date", value=datetime.date(2023, 1, 1))
    end_date = st.date_input("End Date", value=datetime.date(2023, 12, 1))

    # 조건 설정
    days = st.slider("Number of Consecutive Rising Days", min_value=1, max_value=10, value=5)
    threshold = st.slider("Threshold for Rising Percentage", min_value=0.01, max_value=0.1, value=0.05)

    # 데이터 가져오기
    stock_data = fetch_stock_data(selected_stock_code, start_date, end_date)
    
    if stock_data is not None and not stock_data.empty:
        # 조건식 확인
        stock_data['Rising'] = is_rising(stock_data, days, threshold)
        
        # 그래프 시각화
        plot_stock_graph(stock_data)
    else:
        st.write(f"{selected_stock_name} 데이터가 비어 있습니다.")

if __name__ == "__main__":
    main()

