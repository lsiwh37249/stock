# 실시간 주식 자동매매 파이프라인

한국투자증권 OpenAPI(WebSocket)를 사용해 실시간 시세를 수신하고, 조건을 만족하는 종목에 대해 자동으로 주문을 생성·전달하는 파이프라인입니다.

## 주요 기능

- **실시간 시세 수신 (`Realtime.py`)**
  - 한국투자증권 WebSocket(`H0STCNT0`, 호가/체결) 구독
  - `REAL_APPKEY`, `REAL_APPSECRETKEY` 환경변수 기반 인증
  - 수신한 원시 메시지를 `asyncio.Queue`로 안전하게 전달 (`raw_queue`, `preprocess_queue`)

- **주문 조건 판단 (`Order.py`)**
  - 실시간 거래량 기준으로 급등 여부 판단
    - 최근 5틱 기준 평균 거래량과 비교해 `volume_ratio` 계산
  - `volume_ratio`가 임계값 이상인 경우 매수 주문 생성
  - 조건을 만족하는 주문만 `order_worker_queue`로 전달

- **기타 모듈 (파일 기준)**  
  실제 구현은 코드와 다를 수 있으니 참고용으로 봐 주세요.
  - `Queue.py`: `raw_queue`, `preprocess_queue`, `order_queue`, `order_worker_queue` 등 비동기 큐 정의
  - `Preprocess.py`: 원시 WebSocket 데이터를 가공/파싱하여 주문 판단에 사용할 구조로 변환
  - `Worker.py`: `order_worker_queue`를 소비해 실제 주문 API 호출 또는 로그/모니터링 처리
  - `Monitor.py`, `monitor.log`: 시스템 동작 로그 및 모니터링
  - `Stock.py`, `Control.py`, `KisAuth.py`: 종목 관리, 전략 제어, 한국투자증권 인증/토큰 관리 등

## 요구 사항

- Python 3.10+
- 의존 라이브러리 (예시)
  - `requests`
  - `websocket-client`
  - `asyncio` (표준 라이브러리)
  - 기타 실제 코드에서 사용하는 라이브러리들

> 아직 `requirements.txt`가 정리되지 않았다면, 설치된 환경 기준으로 `pip freeze > requirements.txt`로 정리한 뒤 공유하는 것을 권장합니다.

## 환경 변수 / 설정

한국투자증권 OpenAPI 연동을 위해 다음 환경 변수가 필요합니다.

- `REAL_APPKEY`: 실계좌 앱키
- `REAL_APPSECRETKEY`: 실계좌 앱 시크릿키

추가적으로, `secret.json` 파일에 계좌번호 등 민감 정보를 저장해 사용할 수 있습니다. 이 파일은 반드시 `.gitignore`에 포함되어야 합니다.

```bash
export REAL_APPKEY="YOUR_APP_KEY"
export REAL_APPSECRETKEY="YOUR_APP_SECRET"
```

## 실행 방법

### 1. 가상환경 및 패키지 설치

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt  # requirements.txt가 있는 경우
```

### 2. 실시간 수신 테스트 (`Realtime.py` 단독 실행)

```bash
export REAL_APPKEY="YOUR_APP_KEY"
export REAL_APPSECRETKEY="YOUR_APP_SECRET"

python Realtime.py
```

기본 예제에서는 `ticker="222080"` 종목을 WebSocket으로 구독하고, 수신한 raw 데이터를 콘솔에 출력합니다.

### 3. 전체 파이프라인 개요

전체 파이프라인은 대략 다음과 같은 구성으로 동작합니다.

1. `Realtime.py`  
   - WebSocket 연결 및 실시간 데이터 수신  
   - `raw_queue` / `preprocess_queue`로 데이터 전달  
2. `Preprocess.py`  
   - 원시 데이터를 파싱하여 주문 판단에 사용할 딕셔너리 구조로 변환  
3. `Order.py`  
   - 거래량 급등 여부 등 조건 판단  
   - 조건 만족 시 주문 정보 생성 후 `order_worker_queue`로 전송  
4. `Worker.py`  
   - 큐에서 주문 정보를 소비하고 실제 주문 API 호출 또는 시뮬레이션 수행  

실제 실행 스크립트(예: `Control.py` 또는 `tmp.py`)에서 위 컴포넌트들을 하나의 이벤트 루프 안에서 실행하도록 구성할 수 있습니다.

## 주문 조건 로직 개요

`Order.py` 기준 기본 로직은 다음과 같습니다.

- 최근 거래량 리스트(`prev_volumes`)를 유지
- 현재 거래량 / 최근 5틱 평균 거래량 = `volume_ratio`
- `volume_ratio >= volume_ratio_threshold`(기본값 1) 이면 매수 신호
- 매수 신호일 경우:
  - `ticker`, `current_price`, `quantity`(없으면 기본 1)로 주문 딕셔너리 생성
  - `order_worker_queue`에 푸시
- 조건 불만족 시:
  - 빈 주문 정보 반환 및 로그 출력

임계값(`price_up_ratio_threshold`, `volume_ratio_threshold`, `amount_ratio_threshold`, `time_window_threshold`, `cond_index_threshold`)은 전략에 맞게 조정 가능합니다.

## 주의사항

- **실계좌 정보 보호**: `secret.json` 및 환경 변수에 포함된 모든 정보는 절대 공개 저장소에 노출되면 안 됩니다.
- **실거래 전 모의 테스트 필수**: 실제 현금 계좌로 사용하기 전에 반드시 모의투자/테스트 환경에서 충분히 검증 후 사용하세요.
- **API 이용약관 준수**: 한국투자증권 OpenAPI 이용약관을 반드시 숙지하고 준수해야 합니다.

## TODO / 향후 개선 아이디어

- 주문 조건 로직 고도화
  - 가격 상승률, 거래대금 비율(`amount_ratio`), 동시 발생 종목 수 등 추가 지표 반영
- 다양한 전략을 플러그인 형태로 교체 가능하도록 구조화
- `Monitor.py` 기반 웹/대시보드 모니터링 추가
- 에러/예외 처리 및 재연결 로직 강화

