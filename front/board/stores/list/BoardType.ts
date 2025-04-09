export interface BoardState {
    boardList: Board[]
    board: Board | null
  
    currentPage: Number
    totalPages: Number
  }
  
  export interface Board {
    id: number;
    title: string;
    price: string;
    description: string;
    image?: File | string; // 이미지 파일 또는 URL (선택적)
    author_id: number;
    end_time?: string; // 종료 시간 (ISO 날짜 문자열, 선택적)
    restaurant_id: number;
}

    