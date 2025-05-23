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
    <div class="row">
      <div class="col-lg-6 col-md-12">

        {{ userStore.user.username }}
      </div>
      <div class="col-lg-6 col-md-12">

      </div>
    </div>

  </div>

  <!-- <TheChessboard
          @board-created="handleBoardCreated"
          @move="handleMove"
          :player-color="'white'"
        /> -->

</template>