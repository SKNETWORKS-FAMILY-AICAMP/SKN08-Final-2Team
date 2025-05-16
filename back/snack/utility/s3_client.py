import os
import boto3
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()  # .env 파일 로드

class S3Client:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance._initialize()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def _initialize(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        self.bucket_name = os.getenv('AWS_BUCKET_NAME')

    def upload_file(self, file_obj, file_name: str) -> str:
        try:
            print("✅ S3 업로드 시작", file_name)
            self.s3_client.upload_fileobj(
                Fileobj=file_obj,
                Bucket=self.bucket_name,
                Key=file_name,
                ExtraArgs={
                    'ContentType': file_obj.content_type,
                    'ACL': 'public-read'
                }
            )
            file_url = f"https://{self.bucket_name}.s3.amazonaws.com/{file_name}"
            print("✅ 업로드 성공:", file_url)
            return file_url
        except Exception as e:
            print("❌ S3 업로드 실패:", e)
            raise Exception(f"파일 업로드 실패: {str(e)}")

    def delete_file(self, key: str):
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
            print(f"✅ S3 삭제 성공: {key}")
        except Exception as e:
            print(f"❌ S3 삭제 실패: {e}")
            raise Exception(f"S3 삭제 실패: {str(e)}")

# ✅ 유틸 함수로도 제공
def delete_s3_file(image_url: str):
    parsed_url = urlparse(image_url)
    key = parsed_url.path.lstrip('/')

    s3 = S3Client.getInstance()
    s3.delete_file(key)
