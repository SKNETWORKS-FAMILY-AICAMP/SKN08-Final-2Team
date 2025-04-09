export interface BoardModify {    
    board_id: number;
    user_id: number; 
    title: string;      
    content: string;    
    image?: File | string | null; // 기존 이미지 URL | 새로 업로드한 파일 | 이미지 삭제(null)     
    end_time: string;  
    restaurant_id?: number;
  }
  