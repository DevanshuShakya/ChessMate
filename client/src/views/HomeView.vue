<script setup>
import { TheChessboard } from 'vue3-chessboard';
import { Engine } from '@/Engine/Engine.ts';
import { reactive } from 'vue';
import axios from 'axios';
import { useUserStore } from '@/stores/user.js'
import { format } from 'date-fns'

let boardAPI;
let engine;

const userStore = useUserStore()

function handleBoardCreated(boardApi) {
  boardAPI = boardApi;

  engine = new Engine(boardApi);
}

function handleMove() {
  const history = boardAPI?.getHistory(true);

  const moves_ = history?.map((move) => {
    if (typeof move === 'object') {
      return move.lan;
    } else {
      return move;
    }
  });

  if (moves_) {
    console.log(moves_)
    engine?.sendPosition(moves_.join(' '));
  }
}

const formatDate = (dateString) => {
  return format(new Date(dateString), 'MMMM d, yyyy')
}




</script>

<template>

  <div class="container">
    <div class="row" style="margin-top: 50px;">
      <div class="col-lg-6 col-md-12" style="margin-top: 50px; font-weight: 900; font-size: large;">
        <svg height="170" width="170" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg"
                        xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512" xml:space="preserve">
                        <path style="fill:#D6E5F6;" d="M253.659,0H86.661C73.809,0,63.389,10.422,63.389,23.273c0,12.853,10.42,23.273,23.273,23.273h13.521
	v187.988c0,12.854,10.42,23.273,23.273,23.273h39.201c6.173,0,12.092-2.451,16.455-6.816l32.084-32.084v56.076L107,379.181
	c-6.656,6.654-8.647,16.665-5.046,25.363c3.603,8.695,12.089,14.365,21.501,14.365H388.54c12.853,0,23.273-10.418,23.273-23.273
	V158.161C411.814,70.951,340.865,0,253.659,0z" />
                        <path style="fill:#A4C6EC;" d="M295.989,5.762v413.147h92.551c12.853,0,23.273-10.418,23.273-23.273V158.161
	C411.814,85.61,362.705,24.318,295.989,5.762z" />
                        <path style="fill:#385C8E;" d="M438.483,372.364H73.517c-12.853,0-23.273,10.422-23.273,23.273v93.091
	c0,12.854,10.42,23.273,23.273,23.273h364.966c12.853,0,23.273-10.418,23.273-23.273v-93.091
	C461.756,382.785,451.336,372.364,438.483,372.364z" />
                        <path style="fill:#1D3366;" d="M438.483,372.364H256V512h182.483c12.853,0,23.273-10.418,23.273-23.273v-93.091
	C461.756,382.785,451.336,372.364,438.483,372.364z" />
                    </svg>
        <h1 v-if="userStore.user.username" style="color: white; margin: 10px;">
          Welcome back, 
        </h1>
        <h1 v-else style="color: white; margin: 10px;">
          Welcome to the 
          <span style="color: #283b69; margin: 0%; font-size: 70px;" class="dancing-script-brand">
            ChessMate.com 
          </span>
        </h1>

        <div style="margin: 10px;">

          <h1 class="dancing-script-brand" style="color: #283b69;margin: 0%; font-size: 70px;">
            {{ userStore.user.username }}
            <span style="font-size: large;color: #283b69; font-weight: 600;">
              {{ userStore.user.rating }}
            </span>
          </h1>
          
            {{ userStore.user.email }}
        
        </div>
        <!-- <div>
          {{ userStore.user }}
        </div> -->
        <hr>

        <div style="color: green; margin: 10px;font-weight: 700;">
          Play against the Stockfish Engine
        </div>

        


      </div>
      <div class="col-lg-6 col-md-12">

        <TheChessboard
                @board-created="handleBoardCreated"
                @move="handleMove"
                :player-color="'white'"
              />
      </div>
    </div>

  </div>


</template>

<style scoped>
.rating-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  color: #fff;
  font-weight: bold;
  font-family: sans-serif;
}

.rating-bronze    { background: #cd7f32; }
.rating-silver    { background: #C0C0C0; color: #000; }
.rating-gold      { background: #FFD700; color: #000; }
.rating-platinum  { background: #B0E0E6; color: #000; }
.rating-diamond   { background: #B9F2FF; color: #000; }
.rating-champion  { background: #E066FF; }
.rating-legendary { background: #AA00FF; }


.dancing-script-brand {
    font-family: "Tiny5", serif;
    font-optical-sizing: auto;
    font-weight: 400;
    font-style: normal;
}

</style>