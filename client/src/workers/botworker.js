// botWorker.js

// Import the bot engine library if needed
// importScripts('@/Engine/botengine.js');
import { BotEngine } from '@/Engine/botengine.js'


// Handle messages from the main thread
onmessage = function(e) {
    const { type, data } = e.data;
    
    if (type === 'MAKE_MOVE') {
        // Run the bot's makeBestMove function
        // const boardAPI  = JSON.parse(data)
        
        const { fen, history, globalSUM, depth } = JSON.parse(data)
        const bot = new BotEngine(fen, history, globalSUM, depth);
        const [ bestMove, globalSum ] = bot.makeBestMove('b');
        
        // Post the result back to the main thread
        postMessage({ type: 'BEST_MOVE', data:  JSON.stringify({ bestMove, globalSum })});
    }
};