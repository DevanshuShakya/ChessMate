<script setup>
import { ref, watch } from "vue";
import { TheChessboard } from 'vue3-chessboard';
import 'vue3-chessboard/style.css';
import { useOptionStore } from "@/stores/option.js"
import { useGameStore } from "@/stores/game.js";
import { onMounted, onUnmounted } from 'vue';
import socket from '@/plugins/socket';
import { useUserStore } from '@/stores/user.js'

// accept these as props or derive from route

const optionStore = useOptionStore()
const gameStore = useGameStore()
const userStore = useUserStore()

// if(optionStore.option=='casual'){
//     props = defineProps({
//     roomId: { type: String, required: true },
//     username: { type: String, required: true }
// });
// }

// const roomId = 'roomhaina'


// Initialize the worker
let worker;
let globalSUM = 0;

const playerColor = ref('white');

onMounted(() => {
    // Load the Web Worker

    console.log("onmounted in playchessboard")
    worker = new Worker(new URL('@/workers/botWorker.js', import.meta.url), { type: 'module' });

    worker.onmessage = (e) => {
        const { type, data } = e.data;
        if (type === 'BEST_MOVE') {
            const { bestMove, globalSum } = JSON.parse(data);
            globalSUM = globalSum
            gameStore.boardAPI.move(bestMove)
        }
    };

    
});

// Send a message to the worker to make a move
function triggerBotMove(fen, history, globalSUM, depth) {
    worker.postMessage({
        type: 'MAKE_MOVE',
        data: JSON.stringify({ fen, history, globalSUM, depth }),
    });
}

onUnmounted(() => {
    worker.terminate();

    if (optionStore.option == 'casual') {
        if (currentRoomId.value) {
            socket.emit('leave_game', { 
                room_id: currentRoomId.value, 
                username: userStore.user.username 
            });
        }
        socket.off('game_found');
        socket.off('game_state');
        socket.off('waiting_for_opponent');
        socket.off('opponent_move');
        socket.off('game_over');
    }
});




let lost_black = ref(null); // Reactive array to store
let lost_white = ref(null); // Reactive array to store

function toggleColor(color) {
    if (color === 'b') {
        return 'w'
    }
    else if (color === 'w') {
        return 'b'
    }
    else if (color === 'white') {
        return 'black'
    }
    else {
        return 'white'
    }
}

function getPieceStyle(index) {
    return {
        zIndex: index, // Higher index pieces appear on top
        left: `${index * 20}px`, // Adjust the offset as needed
    }
}

const boardConfig = {
    coordinates: true,
    animation: { // modify piece animations
        enabled: true,
        duration: 400,
    },
    style: {
        colors: {
            dark: '#4d4d4d',  // Dark squares color
            light: '#eeeed2', // Light squares color
        },
    },
};

const isSuccess = ref(true);



function handleBoardCreated(boardApi) {
    console.log('board created')
    gameStore.boardAPI = boardApi;
    lost_white.value = null
    lost_black.value = null
    gameStore.move = null
}


watch(() => gameStore.move, (newValue, oldValue) => {
    if (gameStore.move != null) {
        lost_white.value = gameStore.boardAPI.getCapturedPieces()['black']
        lost_black.value = gameStore.boardAPI.getCapturedPieces()['white']
    }
    else {
        lost_white.value = null
        lost_black.value = null
    }

},
    { deep: true }
);

function handleMove(move_) {
    gameStore.move = move_;

    if (optionStore.option === 'beginner') {
        if (move_.color === 'w') {
            triggerBotMove(gameStore.boardAPI.getFen(), gameStore.boardAPI.getHistory(true), globalSUM, 1)
        }
    }
    if (optionStore.option === 'intermediate') {
        if (move_.color === 'w') {
            triggerBotMove(gameStore.boardAPI.getFen(), gameStore.boardAPI.getHistory(true), globalSUM, 2)
        }
    }
    if (optionStore.option === 'advanced') {
        if (move_.color === 'w') {
            triggerBotMove(gameStore.boardAPI.getFen(), gameStore.boardAPI.getHistory(true), globalSUM, 3)
        }
    }
    if (optionStore.option === 'expert') {
        if (move_.color === 'w') {
            triggerBotMove(gameStore.boardAPI.getFen(), gameStore.boardAPI.getHistory(true), globalSUM, 4)
        }
    }



    console.log(optionStore.option)

    if (optionStore.option === 'casual' && optionStore.gameStarted) {
        // Only emit move if it's player's turn
        console.log(optionStore.playerColor)
        if ((optionStore.playerColor === 'white' && move_.color === 'w') ||
            (optionStore.playerColor === 'black' && move_.color === 'b')) {
            socket.emit('make_move', {
                room_id: optionStore.currentRoomId,
                from: move_.from,
                to: move_.to,
                fen: gameStore.boardAPI.getFen(),
                username: userStore.user.username,
                checkmate: gameStore.boardAPI.getIsCheckmate()
            });
        }
    }
}

function handleResign() {
    if (optionStore.option === 'casual' && optionStore.gameStarted) {
        socket.emit('resign', {
            room_id: optionStore.currentRoomId,
            username: userStore.user.username
        });
        const mymodal = new bootstrap.Modal('#myModal')
        mymodal.show()
    }
}

function handleCheckmate(isMated) {
    // Create a Bootstrap modal instance
    const mymodal = new bootstrap.Modal('#myModal');
    gameStore.winner = toggleColor(isMated)
    console.log(gameStore.winner)
    if (gameStore.winner == 'black') {
        optionStore.isSuccess = false;
    }
    // Show the modal
    mymodal.show();
}


</script>
<template>
    <div>

        <!-- Modal -->
        <div class="modal fade" id="myModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content" :class="{ 'bg-success': isSuccess, 'bg-danger': !isSuccess }">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="exampleModalLabel">Game Over</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <img style="height: 50px; width: 50px;" :src="gameStore.getPieceImage('k', gameStore.winner[0])"
                            alt=""> won the game.
                    </div>

                </div>
            </div>
        </div>

        <!-- Waiting Status -->
        <!-- <div v-if="optionStore.option === 'casual' && optionStore.isWaiting" class="alert alert-info text-center" role="alert">
            Waiting for opponent...
            <div class="spinner-border spinner-border-sm ms-2" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div> -->

        <!-- Captured Pieces -->
        <div v-if="optionStore.playerColor=='black'" class="captured-pieces">
            <div v-for="(piece, index) in lost_black" :key="index" :class="['piece']" :style="getPieceStyle(index)">
                <img :src="gameStore.getPieceImage(piece, 'b')" style="height: 30px;" :alt="piece.type" />
            </div>
        </div>
        <div v-else class="captured-pieces">
            <div v-for="(piece, index) in lost_white" :key="index" :class="['piece']" :style="getPieceStyle(index)">
                <img :src="gameStore.getPieceImage(piece, 'w')" style="height: 30px;" :alt="piece.type" />
            </div>
        </div>

        <!-- Opponent Label -->
        <div style="font-weight: 600; font-size: small;padding: 7px;text-align: end;padding-right: 30px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-person-fill"
                viewBox="0 0 16 16">
                <path d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6" />
            </svg>
            <span v-if="!optionStore.option">
                Opponent
            </span>
            <span v-if="optionStore.option === 'beginner'">
                Nobita
            </span>
            <span v-if="optionStore.option === 'intermediate'">
                Suneo
            </span>
            <span v-if="optionStore.option === 'advanced'">
                Suzuka, the Grandmaster
            </span>
            <span v-if="optionStore.option === 'expert'">
                Degisuki, the undefeatable
            </span>
            <span v-if="optionStore.option === 'casual' && optionStore.currentOpponent">
                {{ optionStore.currentOpponent }}
            </span>
            <span v-if="optionStore.option === 'casual' && !optionStore.currentOpponent">
                Waiting for opponent...
            </span>
        </div>

        <!-- Chessboard -->

        <TheChessboard v-if="!optionStore.option" :board-config="boardConfig" style="max-width: 565px;"
            @move="handleMove" @checkmate="handleCheckmate" @board-created="handleBoardCreated" />

        <TheChessboard v-if="optionStore.option === 'advanced'" :board-config="boardConfig" style="max-width: 565px;"
            @move="handleMove" :player-color="playerColor" @checkmate="handleCheckmate"
            @board-created="handleBoardCreated" />

        <TheChessboard v-if="optionStore.option === 'expert'" :board-config="boardConfig" style="max-width: 565px;"
            @move="handleMove" :player-color="playerColor" @checkmate="handleCheckmate"
            @board-created="handleBoardCreated" />

        <TheChessboard v-if="optionStore.option === 'beginner'" :board-config="boardConfig" style="max-width: 565px;"
            @move="handleMove" :player-color="playerColor" @checkmate="handleCheckmate"
            @board-created="handleBoardCreated" />

        <TheChessboard v-if="optionStore.option === 'intermediate'" :board-config="boardConfig"
            style="max-width: 565px;" @move="handleMove" :player-color="playerColor" @checkmate="handleCheckmate"
            @board-created="handleBoardCreated" />
        <TheChessboard v-if="optionStore.option === 'casual'" :board-config="boardConfig" style="max-width: 565px;"
            @move="handleMove" @checkmate="handleCheckmate" :player-color="optionStore.playerColor" @board-created="handleBoardCreated" />

        <!-- Resign Button for Casual Mode -->
        <div v-if="optionStore.option === 'casual' && optionStore.gameStarted" class="text-center mt-3">
            <button @click="handleResign" class="btn btn-danger">
                Resign Game
            </button>
        </div>

        <!-- Your Captured Pieces -->
        <div v-if="optionStore.playerColor=='black'" class="captured-pieces">
            <div v-for="(piece, index) in lost_white" :key="index" :class="['piece']" :style="getPieceStyle(index)">
                <img :src="gameStore.getPieceImage(piece, 'w')" style="height: 30px;" :alt="piece.type" />
            </div>
        </div>
        <div v-else class="captured-pieces">
            <div v-for="(piece, index) in lost_black" :key="index" :class="['piece']" :style="getPieceStyle(index)">
                <img :src="gameStore.getPieceImage(piece, 'b')" style="height: 30px;" :alt="piece.type" />
            </div>
        </div>

        <!-- Your Label -->
        <div style="font-weight: 600; font-size: small;text-align: end; padding: 7px;padding-right: 30px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-person-fill"
                viewBox="0 0 16 16">
                <path d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6" />
            </svg>
            <span v-if="userStore.user.username">{{ userStore.user.username }}
            </span>
            <span v-else>You</span>
        </div>

    </div>
</template>


<style scoped>
.captured-pieces {
    position: relative;
    width: 199px;
    /* Adjust as needed */
}

.piece {
    position: absolute;
    width: 30px;
    padding-top: 10px;
    padding-left: 20px;
    /* Adjust piece size */

}
</style>