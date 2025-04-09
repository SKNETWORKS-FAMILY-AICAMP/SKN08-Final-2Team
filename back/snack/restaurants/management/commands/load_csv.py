import pandas as pd
from django.core.management.base import BaseCommand
from restaurants.entity.restaurants import Restaurant  # ✅ 모델 임포트

class Command(BaseCommand):
    help = "CSV 파일을 데이터베이스에 저장"

    def handle(self, *args, **kwargs):
        file_path = "data/gang_nam_rest.csv"  # ✅ CSV 파일 경로 (프로젝트 내에 위치)
        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            # ✅ 데이터 저장 (이미 존재하는 경우 중복 방지)
            name = row["name"]
            latitude = None if pd.isna(row["latitude"]) else row["latitude"]
            longitude = None if pd.isna(row["longitude"]) else row["longitude"]
            address = row["address"]

            # ✅ 데이터 저장 (이미 존재하는 경우 중복 방지)
            obj, created = Restaurant.objects.get_or_create(
                name=name,
                latitude=latitude,
                longitude=longitude,
                address=address
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ 저장 완료: {row['name']}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ 이미 존재: {row['name']}"))

        self.stdout.write(self.style.SUCCESS("🎉 CSV 데이터 입력 완료!"))
