import * as axiosUtility from "../../../utility/axiosInstance";
import {useAccountStore} from "../../../account/stores/accountStore";
import { boardDetailState } from "./BoardDetailState";


export const boardDetailAction = {
    async requestDetailBoard(boardId: number) {
        console.log("🧪 payload 내용 확인:", boardId);

        const { djangoAxiosInstance } = axiosUtility.createAxiosInstances();
        
        const accountStore = useAccountStore();
        console.log("account_id=", accountStore.accountId);

        try {
            const response = await djangoAxiosInstance.get(`/board/detail/${boardId}`, {
              headers: {}
            });

            console.log("✅ 게시글 상세 조회 성공:", response.data);
            return response.data;
        } catch (error) {
            console.error("❌ requestDetailBoard() 중 에러:", error.response ? error.response.data : error.message);
            throw error;
        }
    },
};
