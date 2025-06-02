<script setup>
import { useGameStore } from '@/stores/game.js';
import { useOptionStore } from '@/stores/option.js';
import { watch, onMounted, ref, onUpdated, reactive } from 'vue'
import axios from 'axios'
import { useUserStore } from '@/stores/user.js';
import socket from '@/plugins/socket';

const gameStore = useGameStore();
const optionStore = useOptionStore();
const userStore = useUserStore();
const preContainer = ref(null); // Ref for the pre element
let playerStatus = ref('')

function toggleColor(color) {
    if (color === 'b') {
        return 'w'
    }
    else {
        return 'b'
    }

}

let history = ref(null)


watch(() => gameStore.move, (newValue, oldValue) => {
    preContainer.value.scrollTop = preContainer.value.scrollHeight;
    history.value = gameStore.boardAPI.getHistory(true)
    console.log(history.value)
},
    { deep: true }
);


onMounted(() => {
    getMessage();
    console.log('onMounted done');
});


// let pgn;

let pgn = ref("")
// let pgn = "1. e4 d5 2. exd5 e6 3. dxe6 fxe6 4. Qe2 Qd5 5. Qxe6+ Qxe6+ 6. Kd1 Qe1+"

function getMessage() {
      const path = 'http://localhost:5000/load';
      console.log('yeah, I am in getmessage');
      axios.get(path)
        .then((res) => {
          pgn.value = res.data;
        //   console.log(pgn);
        })
        .catch((error) => {

          console.error(error);
        });
    }

function loadpgn() {
    gameStore.boardAPI.loadPgn(pgn.value)
    gameStore.move = "pgn loaded"
}

function getPgn() {
    pgn.value = gameStore.boardAPI.getPgn()
    console.log(typeof pgn.value)
    console.log(gameStore.boardAPI.getPgn())
}


function handleReset() {
    gameStore.move = null;
    gameStore.boardAPI.resetBoard();
}

function handleResign() {
    if (optionStore.option === 'casual' && optionStore.gameStarted) {
        console.log('resigning')
        socket.emit('resign', {
            room_id: optionStore.currentRoomId,
            username: userStore.user.username
        });
    }

}

</script>
<template>
    <!-- Modal -->
    <!-- <div class="modal fade" id="staticBackdrop" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
        aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content" style="color: black; background-color: antiquewhite;">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="staticBackdropLabel">The current game will be lost.</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    Do you still want to proceed?
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-danger" data-bs-dismiss="modal">No</button>
                    <button type="button" v-on:click="handleReset()" data-bs-dismiss="modal" class="btn btn-success">Yes</button>
                </div>
            </div>
        </div>
    </div> -->

    <div class="modal fade" id="staticBackdrop" tabindex="-1" aria-labelledby="warningModalLabel"
        aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content warning-modal">
                <div class="modal-header border-0">
                    <h5 class="modal-title" id="warningModalLabel">
                        <i>
                            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="red"
                                class="bi bi-exclamation-triangle-fill" viewBox="0 0 16 16">
                                <path
                                    d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5m.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2" />
                            </svg>
                        </i>
                        Warning
                    </h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close">
                    </button>
                </div>
                <div class="modal-body">
                    Your progress will be lost. Do you still want to proceed?
                </div>
                <div class="modal-footer justify-content-center border-0">
                    <button type="button" class="btn btn-outline-light" data-bs-dismiss="modal">
                        Cancel
                    </button>


                  
                    <button v-on:click="handleReset()" type="button" class="btn btn-warning"
                        data-bs-dismiss="modal">
                        Proceed
                    </button>

                </div>
            </div>
        </div>
    </div>
    <div class="modal fade" id="resignWarning" tabindex="-1" aria-labelledby="warningModalLabel"
        aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content warning-modal">
                <div class="modal-header border-0">
                    <h5 class="modal-title" id="warningModalLabel">
                        <i>
                            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="red"
                                class="bi bi-exclamation-triangle-fill" viewBox="0 0 16 16">
                                <path
                                    d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5m.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2" />
                            </svg>
                        </i>
                        Warning
                    </h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close">
                    </button>
                </div>
                <div class="modal-body">
                    You will lose the match. Do you still want to proceed?
                </div>
                <div class="modal-footer justify-content-center border-0">
                    <button type="button" class="btn btn-outline-light" data-bs-dismiss="modal">
                        Cancel
                    </button>


                    <button v-on:click="handleResign()" type="button" class="btn btn-warning"
                        data-bs-dismiss="modal">
                        Resign
                    </button>
                

                </div>
            </div>
        </div>
    </div>

    


    <!-- <div class="card text-center" style="width: 100%;background-color: #4d4d4d;border: none;">
        <div class="card-body"> -->


    <table class="table table-dark table-striped">
        <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">piece</th>
                <th scope="col">from</th>
                <th scope="col">to</th>
                <th scope="col">captured</th>
            </tr>
        </thead>

    </table>
    <pre ref="preContainer" style="background-color: #454545; height: 200px;">
                            <table class="table table-dark table-striped table-hover">        
                                <tbody>
                                    <tr v-for="(move, index) in history" :key="index">
                                        <th scope="row">{{ index + 1 }}</th>
                                        <!-- <td>{{ move.color }}</td> -->
                                        <td><img :src="gameStore.getPieceImage(move.piece, move.color)" :alt="move.piece" style="height: 30px;"></td>
                                        <td>{{ move.from }}</td>
                                        <td>{{ move.to }}</td>
                                        <!-- <td>{{ move.captured }}</td> -->
                                        <td v-if="move.captured"><img  :src="gameStore.getPieceImage(move.captured, toggleColor(move.color))" style="height: 30px;"></td>
                                        <td v-else> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
                                    </tr>
                                </tbody>
                            </table>
                        </pre>



    <!-- Options -->
    <div class="container" style="background-color: #454545; padding: 10px;">
        <div class="row">
            <div v-if="optionStore.mode == 'online'" class="col-sm-3" style="height: 54px;">
                <button class="btn btn-dark" data-bs-toggle="modal" data-bs-target="#resignWarning"
                    style="height: 50px;width: 100%;border-radius: 0px;">Resign{{ status }}</button>
            </div>
            <div v-else class="col-sm-3" style="height: 54px;">
                <button v-if="history==null" class="btn btn-dark" data-bs-toggle="modal" data-bs-target="#staticBackdrop"
                    style="height: 50px;width: 100%;border-radius: 0px;" disabled>New
                    Game</button>
                <button v-else class="btn btn-dark" data-bs-toggle="modal" data-bs-target="#staticBackdrop"
                    style="height: 50px;width: 100%;border-radius: 0px;">New
                    Game</button>
            </div>
            <div class="col-sm-3" style="height: 54px;">
                <button v-if="history==null" @click="gameStore.boardAPI.undoLastMove()" class="btn btn-dark"
                    style="height: 50px;width: 100%;border-radius: 0px;" disabled>Undo</button>
                <button v-else @click="gameStore.boardAPI.undoLastMove()" class="btn btn-dark"
                    style="height: 50px;width: 100%;border-radius: 0px;">Undo</button>
            </div>
            <div class="col-sm-3" style="height: 54px;">
                <button @click="getPgn()" class="btn btn-dark" style="height: 50px;width: 100%;border-radius: 0px;">Get
                    PGN</button>
            </div>
            <div class="col-sm-3" style="height: 54px;">
                <button @click="loadpgn()" class="btn btn-dark"
                    style="height: 50px;width: 100%;border-radius: 0px;">Load PGN</button>
            </div>

        </div>
    </div>



</template>

<style scoped>
pre {
    max-height: 200px;
    /* Limit height to make scrollable */
    overflow-y: auto;
    /* Add vertical scrolling */
    white-space: pre-wrap;
    /* Preserve whitespace and allow wrapping */
}

/* For Webkit-based browsers (Chrome, Safari) */
::-webkit-scrollbar {
    width: 12px;
    /* Width of the scrollbar */
}

::-webkit-scrollbar-track {
    background-color: #2c2f33;
    /* Background of the track */
}

::-webkit-scrollbar-thumb {
    background-color: #555;
    /* Color of the scrollbar handle */
    border-radius: 6px;
    /* Rounded corners for the scrollbar handle */
    border: 3px solid #2c2f33;
    /* Space around the handle */
}

::-webkit-scrollbar-thumb:hover {
    background-color: #888;
    /* Darker color on hover */
}

/* For Firefox */
* {
    scrollbar-width: thin;
    /* Makes the scrollbar thinner */
    scrollbar-color: #555 #2c2f33;
    /* scrollbar handle color #555, track color #2c2f33 */
}

/* Semi-transparent backdrop */
.modal-backdrop.show {
  opacity: 0.6;
}

/* .warning-modal replaces inline styles */
.warning-modal {
  background-color: #2d3138;    /* match your dark sidebar */
  border-radius: 0.5rem;        /* softer corners */
  box-shadow: 0 0.5rem 1rem rgba(0,0,0,0.3);
  color: #f8f9fa;               /* light text for readability */
}

/* White-close button for dark header */
.btn-close-white {
  filter: invert(1);
}

</style>