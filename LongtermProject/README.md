- Content-Based Movie Recommender System
    
    “주어진 데이터셋을 기반으로 사용자에게 새로운 영화를 추천하라”
    
    데이터셋 : MovieLens (28만명 사용자, 5.8만 영화, 평점 포함)
    
- 문제 및 해결 방식
    
    1️⃣ 추천 시스템의 쟁점 : Matrix Sparsity
    
    → Matrix Factorization / Deep learning 사용하여 해결하고자 함
    
    2️⃣ Loss function 미분, Back Propagation 진행하여 학습
    
    → 원리 이해 위해 프레임워크 사용 ❌
    
    3️⃣ Hyper-Parameter Tuning 진행
    
    4️⃣ RMSE = 0.95 근사한 결과 도출 성공
