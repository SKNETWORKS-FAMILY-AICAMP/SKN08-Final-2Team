export interface BoardState {
  boardList: Board[]
  board: Board | null

  currentPage: Number
  totalPages: Number
}

export interface Board {
  board_id: number;
  title: string;
  image?: File | string;
  author_id: number;
  end_time: string; 
  restaurant_id?: number;
}
