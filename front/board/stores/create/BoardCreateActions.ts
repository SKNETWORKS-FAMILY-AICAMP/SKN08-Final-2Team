import * as axiosUtility from "../../../utility/axiosInstance";
import {useAccountStore} from "../../../account/stores/accountStore";
import { format } from 'date-fns'


export const boardAction = { // ✅ `export const` 확인
    async requestCreateBoard(payload) {
        console.log("🧪 payload 내용 확인:", payload);
        
        const { djangoAxiosInstance } = axiosUtility.createAxiosInstances();
        const accountStore = useAccountStore();

        const { title, content, image, end_time, restaurant_id } = payload;
        const author_id = payload.author_id || localStorage.getItem("account_id");
        console.log("🟢 author_id 값:", author_id);

        console.log("account_id=", accountStore.accountId);

        payload.selectedDate = new Date(payload.end_time);

        // formData.append('end_time', payload.selectedDate.value);
        // console.log("🟢 formData 확인:", Object.fromEntries(formData.entries()));

        try {
            const formData = new FormData();
            formData.append("title", title);
            formData.append("content", content);
            formData.append("author_id", author_id);
            formData.append("end_time", new Date(payload.end_time).toISOString());

          
            if (image instanceof File || image instanceof Blob) {
              formData.append("image", image); // ✅ 이게 정상 작동하려면 image는 File이어야 함
            } else {
              console.warn("⚠️ image가 File이 아닙니다", image);
            }
          
            if (restaurant_id) {
              formData.append("restaurant_id", restaurant_id);
            }

            if (!payload.title || !payload.author_id) {
                     console.error("❌ 필수 필드 누락: 제목과 author_id는 필수입니다.");
                     throw new Error("제목과 로그인은 필수 입력값입니다.");
                 }

            console.log("📤 게시글 생성 요청 데이터:", Object.fromEntries(formData.entries()));

            const res = await djangoAxiosInstance.post(`/board/create/`, formData, {
              headers: {}
            });

            console.log("✅ 게시글 생성 성공:", res.data);
            return res.data;
        } catch (error) {
            console.error("❌ requestCreateBoard() 중 에러:", error.response ? error.response.data : error.message);
            throw error;
        }
    },
};
