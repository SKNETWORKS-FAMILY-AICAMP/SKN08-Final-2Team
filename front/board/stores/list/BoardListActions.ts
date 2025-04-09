import * as axiosUtility from "../../../utility/axiosInstance";

export const boardAction = {
    async requestBoardList(payload) {
        const { djangoAxiosInstance } = axiosUtility.createAxiosInstances();
        const { page, perPage, title, author, start_date, end_date } = payload;


        try {
            const res = await djangoAxiosInstance.get(`board/all/`, {
                params: {
                    page,
                    per_page: perPage,
                    title,
                    author,
                    start_date,
                    end_date, 
                },
            });

            console.log("✅ Response Data:", res.data);

            // 응답 데이터 구조 반영 (List.vue에 맞게 수정)
            const { boards, total_pages, current_page } = res.data;

            console.log(`✅ boardList: ${boards}, totalPages: ${total_pages}, currentPage: ${current_page}`);

            return {
                boardList: boards || [],
                totalPages: total_pages || 0,
                currentPage: current_page || 1,
            };
        } catch (error) {
            console.error("❌ requestBoardList() 중 에러:", error);

            return {
                boardList: [],
                totalPages: 0,
                currentPage: 1,
            };
        }
    },

    async requestReadBoard(boardId) {
        try {
            const { djangoAxiosInstance } = axiosUtility.createAxiosInstances();
            const res = await djangoAxiosInstance.get(`/${boardId}/`); 

            console.log(`✅ Read Board Response: ${JSON.stringify(res.data)}`);

            return res.data;
        } catch (error) {
            console.error("❌ 게시글 정보를 가져오는 데 실패했습니다:", error);
            return null;
        }
    },

};
