import { defineStore } from "pinia";
import { boardAction } from "./BoardCreateActions"; // ✅ import 확인
import { boardState } from "./BoardCreateState"; // ✅ 상태 파일 추가

console.log("🟢 boardAction 객체:", boardAction);
console.log("🟢 requestCreateBoard 함수 확인:", boardAction?.requestCreateBoard);

export const useBoardStore = defineStore("boardCreateStore", { // ✅ store 명칭 수정
    state: () => ({ ...boardState }), 
    actions: {
        async requestCreateBoard(payload) {
            console.log("📤 Store 내부에서 requestCreateBoard 실행됨", payload);
            return await boardAction.requestCreateBoard(payload);
        },
    },
});
