import imageCompression from "browser-image-compression";
import { minify } from "html-minifier";

// ✅ 이미지 압축 함수
export const compressImage = async (file: File, maxSizeMB = 1, maxWidthOrHeight = 1024) => {
    console.log(`🖼️ 원본 파일 크기: ${(file.size / 1024).toFixed(2)} KB`);

    const options = {
        maxSizeMB, // 최대 파일 크기 (기본값: 1MB)
        maxWidthOrHeight, // 최대 가로/세로 크기 (기본값: 1024px)
        useWebWorker: true, // 웹 워커 사용 (성능 향상)
    };

    try {
        const compressedFile = await imageCompression(file, options);
        console.log(`✅ 압축 후 파일 크기: ${(compressedFile.size / 1024).toFixed(2)} KB`);

        // 압축률 계산
        const reductionPercent = ((1 - compressedFile.size / file.size) * 100).toFixed(2);
        console.log(`📉 압축률: ${reductionPercent}% 감소`);

        return compressedFile;
    } catch (error) {
        console.error("❌ 이미지 압축 실패:", error);
        return file; // 실패하면 원본 반환
    }
};

// ✅ HTML 압축 함수
export const compressHTML = async (html: string) => {
    console.log("📄 원본 HTML 길이:", html.length);

    try {
        const { minify } = await import("html-minifier-terser");
        const minifiedHTML = await minify(html, {
            removeComments: true, // 주석 제거
            collapseWhitespace: true, // 공백 제거
            minifyCSS: true, // 인라인 CSS 최소화
            minifyJS: true, // 인라인 JS 최소화
        });

        console.log("✅ 압축 후 HTML 길이:", minifiedHTML.length);

        // 압축률 계산
        const reductionPercent = ((1 - minifiedHTML.length / html.length) * 100).toFixed(2);
        console.log(`📉 압축률: ${reductionPercent}% 감소`);

        return minifiedHTML;
    } catch (error) {
        console.error("❌ HTML 압축 실패:", error);
        return html; // 실패하면 원본 반환
    }
};
