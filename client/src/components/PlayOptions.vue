<script setup>
import { ref } from 'vue'
import { useOptionStore } from '@/stores/option.js'
import { useGameStore } from '@/stores/game.js'
import { useUserStore } from '@/stores/user.js'

const optionStore = useOptionStore()
const gameStore = useGameStore()
const userStore = useUserStore()
const selectedOption = ref(null)
const selectedSubOption = ref(null)
const chattingbox = ref(false)

function selectOption(option) {
    if (!userStore.user.username && (option === 'online' || option === 'friend')) {
        return; // Prevent selection if not logged in
    }
    console.log('Selected Option: ', option)
    selectedOption.value = option;
}

function selectSubOption(subOption) {
    console.log("Selected Sub Option:", subOption);
    console.log(optionStore.option, '  ', subOption)

    if (optionStore.option !== subOption) {
        const myModal = new bootstrap.Modal(document.getElementById('historylosingwarningmodal'), {})
        myModal.show()
        selectedSubOption.value = subOption
    } else {
        selectedSubOption.value = subOption
    }
    chattingbox.value = true
}

function goBack() {
    console.log("Go Back")
    selectedOption.value = null;
    selectedSubOption.value = null
    chattingbox.value = false
}

function handleReset() {
    gameStore.move = null;
    gameStore.boardAPI.resetBoard();
    optionStore.option = selectedSubOption.value;
    optionStore.mode = selectedOption.value;
    if (optionStore.option == 'casual') {
        optionStore.CasualGamePlay();
    }
}

</script>
<template>

    <div class="modal fade" id="historylosingwarningmodal" tabindex="-1" aria-labelledby="warningModalLabel"
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
                    <button @click="goBack()" type="button" class="btn btn-outline-light" data-bs-dismiss="modal">
                        Cancel
                    </button>
                    <button @click="handleReset()" type="button" class="btn btn-warning" data-bs-dismiss="modal">
                        Proceed
                    </button>
                </div>
            </div>
        </div>
    </div>


    <!-- <div class="card" style="width: 100%; ;background-color: #4d4d4d;border: none; color: white;min-height: 240px;">
        <div class="card-body"> -->



    <div class="col-lg-12">
        <button v-on:click="goBack()" class="btn"
            style="border: none;border-radius: 900px; width: 30px;height: 30px;padding: 0px;">
            <img src="@/data/back.png" style="height: 15px;" alt="">
        </button>

    </div>
    <div class="container">
        <div class="row">
            <div class="col-lg-12" style="height: 200px; overflow-y:scroll;">
                <div class="play-options">
                    <!-- Main Options -->
                    <div v-if="!selectedOption && !selectedSubOption">
                        <button 
                            @click="selectOption('online')" 
                            :class="{ 'disabled-button': !userStore.user.username }"
                            :disabled="!userStore.user.username">
                            <div class="row">
                                <div class="col-3" style="display: flex; justify-content: center; max-height: 80px">
                                    <img style="height: 70%;" src="@/data/play_online.png"
                                        class="img-fluid rounded-start" alt="...">
                                </div>
                                <div class="col-9" style="font-weight: 600;">
                                    Play Online
                                    <br>
                                    <p style="font-size: smaller;">Find Opponent and play now</p>
                                    <p v-if="!userStore.user.username" class="login-required">Login required</p>
                                </div>
                            </div>
                        </button>

                        <button @click="selectOption('bot')">
                            <div class="row">
                                <div class="col-3" style="display: flex; justify-content: center;max-height: 80px">
                                    <img style="height: 70%;" src="@/data/play_bots.png" class="img-fluid rounded-start"
                                        alt="...">
                                </div>
                                <div class="col-9" style="font-weight: 600;">
                                    Play Bot
                                    <br>
                                    <p style="font-size: smaller;">Challenge yourself with bots from Easy to Master</p>
                                </div>
                            </div>
                        </button>

                        <button 
                            @click="selectOption('friend')" 
                            :class="{ 'disabled-button': !userStore.user.username }"
                            :disabled="!userStore.user.username">
                            <div class="row">
                                <div class="col-3" style="display: flex; justify-content: center;max-height: 80px">
                                    <img style="height: 70%" src="@/data/play_a_friend.png"
                                        class="img-fluid rounded-start" alt="...">
                                </div>
                                <div class="col-9" style="font-weight: 600;">
                                    Play a friend
                                    <br>
                                    <p style="font-size: smaller;">Invite and play</p>
                                    <p v-if="!userStore.user.username" class="login-required">Login required</p>
                                </div>
                            </div>
                        </button>
                    </div>

                    <!-- Options for Play Bot -->
                    <div v-if="selectedOption === 'bot' && !selectedSubOption">
                        <button @click="selectSubOption('beginner')">

                            <div class="row">
                                <div class="col-3" style="display: flex; justify-content: center; max-height: 80px">
                                    <img style="height: 90%;" src="@/data/beginner.png" class="img-fluid rounded-start"
                                        alt="...">

                                </div>
                                <div class="col-9" style="font-weight: 600;">
                                    Play Beginner Bot
                                    <br>
                                    <p style="font-size: smaller;">He is Nobita, playing for few days</p>

                                </div>
                            </div>

                        </button>
                        <button @click="selectSubOption('intermediate')">

                            <div class="row">
                                <div class="col-3" style="display: flex; justify-content: center; max-height: 80px">
                                    <img style="height: 90%;" src="@/data/intermediate.png"
                                        class="img-fluid rounded-start" alt="...">

                                </div>
                                <div class="col-9" style="font-weight: 600;">
                                    Play Intermediate Bot
                                    <br>
                                    <p style="font-size: smaller;">Gian with the help Suneo, play average.</p>

                                </div>
                            </div>

                        </button>
                        <button @click="selectSubOption('advanced')">

                            <div class="row">
                                <div class="col-3" style="display: flex; justify-content: center; max-height: 80px">
                                    <img style="height: 90%;" src="@/data/advanced.png" class="img-fluid rounded-start"
                                        alt="...">

                                </div>
                                <div class="col-9" style="font-weight: 600;">
                                    Play Advanced Bot
                                    <br>
                                    <p style="font-size: smaller;">Suzuka, with hard work aquired the title of GM.</p>

                                </div>
                            </div>

                        </button>
                        <button @click="selectSubOption('expert')">

                            <div class="row">
                                <div class="col-3" style="display: flex; justify-content: center; max-height: 80px">
                                    <img style="height: 90%;" src="@/data/expert.png" class="img-fluid rounded-start"
                                        alt="...">

                                </div>
                                <div class="col-9" style="font-weight: 600;">
                                    Play Expert
                                    <br>
                                    <p style="font-size: smaller;">Degisuki, intelligent from birth.You should not
                                        challenge him.</p>

                                </div>
                            </div>

                        </button>
                        <button @click="goBack">Back</button>
                    </div>

                    <!-- Options for Play Online -->
                    <div v-if="selectedOption === 'online' && !selectedSubOption">
                        <button @click="selectSubOption('ranked')">Play Ranked</button>
                        <button @click="selectSubOption('casual')">Play Casual</button>
                        <button @click="goBack">Back</button>
                    </div>

                    <!-- Options for Play a Friend -->
                    <div v-if="selectedOption === 'friend' && !selectedSubOption">
                        <button @click="selectSubOption('invite')">Invite a Friend</button>
                        <button @click="selectSubOption('accept')">Accept an Invitation</button>
                        <button @click="goBack">Back</button>
                    </div>

                    <div v-if="chattingbox === true">

                        <div class="container" v-if="selectedOption === 'bot' && optionStore.option === 'beginner'"
                            style="background-color: #454545;">
                            <h1>Chat box</h1>
                            <p>Nobita is saying hi</p>
                        </div>
                        <div class="container" v-if="selectedOption === 'bot' && optionStore.option === 'intermediate'"
                            style="background-color: #454545;">
                            <h1>Chat box</h1>
                            <p>Gian is saying hi</p>
                        </div>
                        <div class="container" v-if="selectedOption === 'bot' && optionStore.option === 'advanced'"
                            style="background-color: #454545;">
                            <h1>Chat box</h1>
                            <p>Suzuka is saying hi</p>
                        </div>
                        <div class="container" v-if="selectedOption === 'bot' && optionStore.option === 'expert'"
                            style="background-color: #454545;">
                            <h1>Chat box</h1>
                            <p>Degisuki is saying hi</p>
                        </div>
                        <div class="container" v-if="selectedOption === 'online' && optionStore.option === 'casual'"
                            style="background-color: #454545;">
                            <h1>Chat box</h1>
                            <p>Online Chat Room</p>
                        </div>

                    </div>
                </div>
            </div>
        </div>
    </div>




</template>

<style>
.play-options button {
    display: block;
    margin: 5px;
    height: 95px;
    width: 100%;
    background-color: #272829;
    border: none;
    border-radius: 5px;
    color: white;
    text-align: start;
    padding: 15px;
}

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
    background-color: #2d3138;
    /* match your dark sidebar */
    border-radius: 0.5rem;
    /* softer corners */
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.3);
    color: #f8f9fa;
    /* light text for readability */
}

/* White-close button for dark header */
.btn-close-white {
    filter: invert(1);
}

.disabled-button {
    opacity: 0.6;
    cursor: not-allowed;
    position: relative;
    pointer-events: none; /* This prevents any mouse interaction */
}

.login-required {
    color: #ff6b6b;
    font-size: 0.8em;
    margin-top: 5px;
}

/* Increase backdrop opacity for postGameStatusModal */
:deep(.modal-backdrop.show[data-bs-target="#postGameStatusModal"]) {
    opacity: 0.8 !important;
}
</style>