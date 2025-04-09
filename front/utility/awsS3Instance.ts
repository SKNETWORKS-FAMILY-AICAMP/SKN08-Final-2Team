import { S3Client, GetObjectCommand, DeleteObjectCommand } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import { useRuntimeConfig } from 'nuxt/app';

let awsS3Instance: S3Client | null = null;

export function createAwsS3Instance() {
  if (!awsS3Instance) {
    const config = useRuntimeConfig();

    // config 값들을 string으로 명시적으로 캐스팅
    const region = config.public.AWS_REGION as string;
    const accessKeyId = config.public.AWS_ACCESS_KEY_ID as string;
    const secretAccessKey = config.public.AWS_SECRET_ACCESS_KEY as string;

    awsS3Instance = new S3Client({
      region,
      credentials: {
        accessKeyId,
        secretAccessKey,
      },
    });
  }

  return awsS3Instance;
}

export async function getSignedUrlFromS3(key) {
  const s3 = createAwsS3Instance();
  const config = useRuntimeConfig();
  const bucketName = config.public.AWS_BUCKET_NAME;

  const command = new GetObjectCommand({
    Bucket: bucketName,
    Key: key,
  });

  return await getSignedUrl(s3, command, { expiresIn: 3600 }); // 1시간 유효한 서명 URL
}

export async function deleteFileFromS3(key: string) {
  const s3 = createAwsS3Instance();
  const config = useRuntimeConfig();
  const bucketName = config.public.AWS_BUCKET_NAME;

  try {
    await s3.send(
      new DeleteObjectCommand({
        Bucket: bucketName,
        Key: key,
      })
    );
    console.log(`파일 삭제 완료: ${key}`);
  } catch (error) {
    console.error(`파일 삭제 실패: ${key}`, error);
    throw error;
  }
}
