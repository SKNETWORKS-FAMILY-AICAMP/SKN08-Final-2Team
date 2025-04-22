export interface BoardModify {    
  board_id: number;
  title: string;
  content: string;
  image?: File | File[] | string | null;
  end_time: string;
  restaurant_id?: number;
}
