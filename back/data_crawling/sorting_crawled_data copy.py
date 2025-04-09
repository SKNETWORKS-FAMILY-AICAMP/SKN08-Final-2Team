import os
import glob
import pandas as pd

# 필터링 조건
MIN_DEGREE = 3.0  # 최소 평점
MIN_REVIEWS = 10  # 최소 리뷰 수

# 제거할 프랜차이즈 키워드 리스트 (대소문자 구분 없이 일치시키기 위함)
FRANCHISE_KEYWORDS = [
    '스타벅스', '이디야', '이디야커피', '할리스', '할리스커피',
    '베스킨라빈스', '베스킨라벤스', '던킨', '파리바게뜨', '뚜레쥬르',
    '투썸플레이스', '엔제리너스', '커피빈', '버거킹', '맥도날드',
    '맘스터치', '롯데리아', '서브웨이', '도미노', '피자헛', '미스터피자',
    'KFC', '노브랜드버거', '공차', '탐앤탐스', '빽다방', '배스킨라빈스'
]

# 원본 파일이 있는 디렉토리
input_dir = "crawling_20250316"
input_files = glob.glob(os.path.join(input_dir, "*.csv"))

# 저장할 디렉토리
output_dir = "sorted_crawled_data_20250316"
os.makedirs(output_dir, exist_ok=True)

# 모든 CSV 파일 필터링 및 저장
for file_path in input_files:
    df = pd.read_csv(file_path, encoding='utf-8-sig')

    # 컬럼명 정리
    df.rename(columns=lambda x: x.strip(), inplace=True)

    # 컬럼명 확인 후 '이름', '평점', '리뷰수'가 없으면 스킵
    if not {'이름', '평점', '리뷰수'}.issubset(df.columns):
        print(f"⚠️ 필수 컬럼 누락: {file_path}")
        continue

    # 평점과 리뷰수를 숫자로 변환
    df['평점'] = pd.to_numeric(df['평점'], errors='coerce')
    df['리뷰수'] = pd.to_numeric(df['리뷰수'], errors='coerce').astype('Int64')

    # NaN 제거 및 평점/리뷰 기준 필터링
    filtered_df = df.dropna(subset=['평점', '리뷰수'])
    filtered_df = filtered_df[
        (filtered_df['평점'] >= MIN_DEGREE) &
        (filtered_df['리뷰수'] >= MIN_REVIEWS)
    ]

    # 프랜차이즈 제거
    pattern = '|'.join(FRANCHISE_KEYWORDS)
    filtered_df = filtered_df[~filtered_df['이름'].str.contains(pattern, case=False, na=False)]

    # 저장
    filename = os.path.basename(file_path).replace('.csv', '_filtered.csv')
    output_path = os.path.join(output_dir, filename)
    filtered_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"✅ 필터링 완료: {output_path}")

print("🚀 모든 파일 필터링 완료!")
