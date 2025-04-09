// stores/board/BoardDeleteState.ts
import { ref } from "vue";

export const state = {
  isDeleting: ref(false),
  deleteSuccess: ref(false),
  deleteError: ref<string | null>(null),
};
