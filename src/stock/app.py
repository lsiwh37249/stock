import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st
import datetime

# 삼성전자 주식 코드
TICKER = "005930.KS"

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
    ax.set_title("Samsung Electronics Stock Price with Rising Condition")
    ax.set_xlabel("Date")
    ax.set_ylabel("Close Price")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

# Streamlit 인터페이스
def main():
    # 제목
    st.title("Samsung Electronics Stock Price Analysis")

    # 날짜 입력: datetime.date 객체로 변환
    start_date = st.date_input("Start Date", value=datetime.date(2023, 1, 1))
    end_date = st.date_input("End Date", value=datetime.date(2023, 12, 1))
    
    # 조건 설정
    days = st.slider("Number of Consecutive Rising Days", min_value=1, max_value=10, value=5)
    threshold = st.slider("Threshold for Rising Percentage", min_value=0.01, max_value=0.1, value=0.05)

    # 데이터 가져오기
    stock_data = fetch_stock_data(TICKER, start_date, end_date)
    
    if stock_data is not None and not stock_data.empty:
        # 조건식 확인
        stock_data['Rising'] = is_rising(stock_data, days, threshold)
        
        # 그래프 시각화
        plot_stock_graph(stock_data)
    else:
        st.write(f"{TICKER} 데이터가 비어 있습니다.")

if __name__ == "__main__":
    main()
