<script setup>
import 'vue3-chessboard/style.css';
import PlayOptions from '@/components/PlayOptions.vue'
import PlayChessBoard from '@/components/PlayChessBoard.vue';
import PlayHistory from '@/components/PlayHistory.vue';
import { useUserStore } from '@/stores/user.js';
import { useOptionStore } from '@/stores/option.js'

const userStore = useUserStore()
const optionStore = useOptionStore()

// console.log()

</script>

<template>

    <div class="container-fluid" style="color: white;">
        <div class="row">
            <!-- Column 1 -->

            <div class="col-lg-6 col-md-12">
                <PlayChessBoard />

                <!-- {{ userStore.user.username }} -->


            </div>


            <!-- Column 2 -->

            <div class="col-lg-6 col-md-12" style="border-radius: 5px;margin-top: 20px;padding-top: 2px;">

                <div class="col2Card">
                    <!-- <div class="corner-item">I'm in the lower-left corner</div> -->
                    <!-- Corresponding Components -->
                    <div class="row" style="min-height: 220px;">
                        <div class="col">
                            <PlayOptions />
                        </div>
                    </div>




                    <br>

                    <!-- History Table -->
                    <div class="row">
                        <div class="col">

                            <PlayHistory />
                        </div>
                    </div>


                </div>





            </div>

        </div>
    </div>




</template>

<style scoped>
.col2Card {
    position: relative;
    /* Make the container a positioned element */
    width: 100%;
    height: 90%;
    background-color: #4d4d4d;
}

.corner-item {
    position: absolute;
    bottom: 0;
    /* Align to the bottom of the container */
    left: 0;
    /* Align to the left of the container */
    background-color: #ffcc00;
    padding: 10px;
}

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
