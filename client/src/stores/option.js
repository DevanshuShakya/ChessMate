import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import socket from "@/plugins/socket"
import { useUserStore } from '@/stores/user.js'
import { useGameStore } from '@/stores/game.js'

export const useOptionStore = defineStore('option', () => {
  const option = ref(null)
  const mode = ref(null)
  const playerColor = ref('white');
  const isWaiting = ref(false);
  const gameStarted = ref(false);
  const currentOpponent = ref(null);
  const currentRoomId = ref(null);
  const isSuccess = ref(false);
  const userStore = useUserStore()
  const gameStore = useGameStore()



  const CasualGamePlay = () => {
    console.log('Initializing casual mode');
    isWaiting.value = true;

    // Setup socket event listeners
    socket.on('connect', () => {
      console.log('Socket connected with ID:', socket.id);
    });

    socket.on('disconnect', () => {
      console.log('Socket disconnected');
      isWaiting.value = true;
      gameStarted.value = false;
      currentOpponent.value = null;
    });

    socket.on('error', (error) => {
      console.error('Socket error:', error);
      alert(error.message);
    });

    socket.on('game_found', (data) => {
      console.log('Game found:', data);
      isWaiting.value = false;
      gameStarted.value = true;
      playerColor.value = data.color;
      currentOpponent.value = data.opponent;
      currentRoomId.value = data.room_id;

      // Join the game room
      console.log('Joining game room:', data.room_id);
      socket.emit('join_game', {
        room_id: data.room_id,
        username: userStore.user.username
      });

      print(data)

      // If player is black, flip the board
      if (data.color === 'black') {
        gameStore.boardAPI.toggleOrientation();
      }

      
    });

    socket.on('game_state', (gameState) => {
      // console.log('Received game state:', gameState);
      // Handle any initial game state setup if needed
    });

    socket.on('waiting_for_opponent', () => {
      console.log('Waiting for opponent');
      isWaiting.value = true;
      gameStarted.value = false;
    });

    socket.on('opponent_move', (data) => {
      console.log('Opponent move received:', data);
      gameStore.boardAPI.move({ from: data.from, to: data.to });
    });

    socket.on('game_over', (data) => {
      console.log('Game over:', data);
      const mymodal = new bootstrap.Modal(document.getElementById('myModal'));
      gameStore.winner = data.winner;
      isSuccess.value = data.winner === userStore.user.username;
      mymodal.show();

      // Reset game state
      gameStarted.value = false;
      currentOpponent.value = null;
    });

    // Start finding a game
    console.log('Emitting find_game event');
    socket.emit('find_game', {
      username: userStore.user.username
    });
  }
  return { mode, option, CasualGamePlay,isSuccess, playerColor, isWaiting, gameStarted, currentOpponent, currentRoomId }
})


