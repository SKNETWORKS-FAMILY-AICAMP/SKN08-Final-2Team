import os
import pandas as pd
from django.core.management.base import BaseCommand
from restaurants.entity.restaurants import Restaurant

class Command(BaseCommand):
    help = "모든 CSV 파일을 DB에 저장"

    def handle(self, *args, **kwargs):
        directory_path = "data"  # 모든 CSV 파일이 들어 있는 디렉토리 경로
        csv_files = [f for f in os.listdir(directory_path) if f.endswith(".csv")]

        if not csv_files:
            self.stdout.write(self.style.WARNING("⚠️ CSV 파일이 없습니다."))
            return

        for file_name in csv_files:
            file_path = os.path.join(directory_path, file_name)
            self.stdout.write(self.style.NOTICE(f"📂 처리 중: {file_name}"))

            df = pd.read_csv(file_path)
            for _, row in df.iterrows():
                name = row['이름']
                latitude = row.get('위도')
                longitude = row.get('경도')
                address = row.get('주소', '')
                rating = row.get('평점', None)
                review_count = row.get('리뷰수', None)
                category = row.get('서브카테고리', '')
                closed = row.get('영업시간', '')  # 폐업 여부 없음
                keyword = row.get('키워드', '')  # 키워드 필드 추가

                obj, created = Restaurant.objects.get_or_create(
                    name=name,
                    defaults={
                        'latitude': latitude,
                        'longitude': longitude,
                        'address': address,
                        'rating': rating,
                        'reviewCount': review_count,
                        'category': category,
                        'closed': closed,
                        'keyword': keyword,
                    }
                )
                msg = "✅ 저장 완료" if created else "⚠️ 이미 존재"
                self.stdout.write(self.style.SUCCESS(f"{msg}: {name}"))

            self.stdout.write(self.style.SUCCESS(f"🎉 {file_name} 처리 완료!\n"))

        self.stdout.write(self.style.SUCCESS("✅ 모든 CSV 데이터 입력 완료!"))
