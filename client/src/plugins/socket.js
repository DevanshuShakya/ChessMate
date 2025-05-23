import { io } from "socket.io-client";

const socket = io("http://localhost:5000", {
    autoConnect: true,
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionDelayMax: 5000,
    reconnectionAttempts: 5,
    transports: ['websocket', 'polling']
});

// Add event listeners for connection status
// socket.on('connect', () => {
//     console.log('Socket connected with ID:', socket.id);
// });

socket.on('connect_error', (error) => {
    console.error('Socket connection error:', error);
});

socket.on('disconnect', (reason) => {
    console.log('Socket disconnected:', reason);
});

export default socket;
