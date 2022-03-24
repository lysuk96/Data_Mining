## 프로젝트 내용

---

- 목표
    
    **“주어진 데이터셋을 기반으로 사용자에게 새로운 영화를 추천하라”**
    
    데이터셋 : MovieLens (평점 수: 2800만, 영화 수: 6.2만, 사용자 수 : 16.2만)
    
- 문제 및 해결 방식
    
    방식 선택 : **Content-Based Recommender System**
    
    1️⃣ 추천 시스템의 쟁점 : Matrix Sparsity
    
    → Matrix Factorization / Deep learning 사용하여 해결 시도
    
    2️⃣ Loss function 미분, Back Propagation 진행하여 학습
    
    → 원리 이해 위해 프레임워크 사용 ❌
    
    3️⃣ Hyper-Parameter Tuning 진행
    
    4️⃣ RMSE = 0.95 근사한 결과 도출 성공
    
## Instrunction for compiling

---

A. python 설치
B. Base 파일, Test 파일, RecSys_2016025732.py 같은 디렉토리내 위치
C. Execute the program with four arguments : training data name, test data name
![image](https://user-images.githubusercontent.com/48303178/159904814-9bc6fb29-5523-4e5f-bc0b-4e4fe409895b.png)
