<script setup>
// import PlayChessBoard from '@/components/PlayChessBoard.vue';
// import { useGameStore } from '@/stores/game.js';
// import { ref, onMounted } from "vue";

// const gameStore = useGameStore();

// let puzzles = [
//   {
//     id: 1,
//     title: 'Mate in 1',
//     pgn: `[Event "Puzzle 1"]
// [FEN "6k1/5ppp/8/8/8/8/5PPP/6K1 w - - 0 1"]
// [SetUp "1"]
// [Result "1-0"]

// 1. Kf1#`
//   },
//   {
//     id: 2,
//     title: 'Mate in 2',
//     pgn: `[Event "Puzzle 2"]
// [FEN "8/8/8/8/8/2Q5/5K2/6k1 w - - 0 1"]
// [SetUp "1"]
// [Result "1-0"]

// 1. Qg3+ Kh1 2. Qg2#`
//   },
//   {
//     id: 3,
//     title: 'Fork Tactic',
//     pgn: `[Event "Puzzle 3"]
// [FEN "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"]
// [SetUp "1"]
// [Result "*"]

// 1. Nxe5 Nxe5 2. d4`
//   }
  
// ]


// function loadpgn() {
//     gameStore.boardAPI.loadPgn(pgn)
//     gameStore.move = "pgn loaded"
// }

// onMounted(() => {
//     loadpgn();
//     console.log('onMounted done');
// });


</script>

<template>

    <div class="container-fluid" style="color: white;">
        <div class="row">
      

            <div class="col-lg-6 col-md-12">
                <PlayChessBoard />

            </div>

         
        </div>
    </div>

</template>