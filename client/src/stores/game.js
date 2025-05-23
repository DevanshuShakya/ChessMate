import { ref, computed, reactive } from 'vue'
import { defineStore } from 'pinia'

// const moves = reactive([]); // Reactive array to store moves
// const lost_black = reactive([]); // Reactive array to store
// const lost_white = reactive([]); // Reactive array to store
// const preContainer = ref(null); // Ref for the pre element
// const winner = ref("black")
export const move = ref(null)

export const useGameStore = defineStore('game', () => {
    let boardAPI
    // const moves = reactive([]);
    const move = ref(null)
    const winner = ref("black")

    function getPieceImage(piece, color) {
        // Map each piece name to an image path
        const pieceImages = {
            'bk': "/src/data/Chess_kdt45.svg",
            'bq': "/src/data/Chess_qdt45.svg",
            'br': "/src/data/Chess_rdt45.svg",
            'bb': "/src/data/Chess_bdt45.svg",
            'bn': "/src/data/Chess_ndt45.svg",
            'bp': "/src/data/Chess_pdt45.svg",

            'wp': "/src/data/Chess_plt45.svg",
            'wr': "/src/data/Chess_rlt45.svg",
            'wn': "/src/data/Chess_nlt45.svg",
            'wb': "/src/data/Chess_blt45.svg",
            'wq': "/src/data/Chess_qlt45.svg",
            'wk': "/src/data/Chess_klt45.svg",
        }

        return pieceImages[color + piece];
    }


  const doubleCount = computed(() => count.value * 2)
  function increment() {
    count.value++
  }

  return { boardAPI, move, winner, getPieceImage  }
})
