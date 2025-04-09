import os
import glob
import pandas as pd

# 필터링 조건
MIN_DEGREE = 3.0  # 최소 평점
MIN_REVIEWS = 10  # 최소 리뷰 수

# 원본 파일이 있는 디렉토리 (crawled_data 내부의 모든 CSV 파일 처리)
input_dir = "crawled_data"
input_files = glob.glob(os.path.join(input_dir, "*.csv"))  # 모든 CSV 파일 리스트 가져오기

# 저장할 디렉토리 생성
output_dir = "sorted_crawled_data"
os.makedirs(output_dir, exist_ok=True)

# 모든 CSV 파일 필터링 및 저장
for file_path in input_files:
    df = pd.read_csv(file_path, encoding='utf-8-sig')
    
    # 'degree'와 'review num' 컬럼을 숫자로 변환 (문자열이 섞여 있을 가능성 대비)
    df['degree'] = pd.to_numeric(df['degree'], errors='coerce').astype(float)  # 변환 불가능한 값은 NaN 처리
    df['review num'] = pd.to_numeric(df['review num'], errors='coerce').astype('Int64')

    # NaN 값 제거 후 필터링 적용
    filtered_df = df.dropna(subset=['degree', 'review num'])
    filtered_df = filtered_df[
        (filtered_df['degree'] >= MIN_DEGREE) & 
        (filtered_df['review num'] >= MIN_REVIEWS)
    ]

    # 파일 이름에서 경로 및 확장자 제거 후 새로운 이름 생성
    filename = os.path.basename(file_path).replace('.csv', '_filtered.csv')
    output_path = os.path.join(output_dir, filename)

    # 필터링된 데이터를 저장
    filtered_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"✅ 필터링 완료: {output_path}")

print("🚀 모든 파일 필터링 완료!")  
