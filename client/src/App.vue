<script setup>
import { RouterLink, RouterView } from "vue-router"
import axios from 'axios';
import { useUserStore } from '@/stores/user.js';
import { ref, onMounted } from "vue"


const userStore = useUserStore()
const sidebar_class = ref("collapsed")
const collapse_icon = ref(true)
// const user = ref("")
// const email = ref("")
// const password = ref("")
// const message = ref("")
// const loginstatus = ref("")

// const API_URL = 'http://localhost:5000'
let token = localStorage.getItem('auth_token')

const email = ref('')
const password = ref('')
const username = ref('')
const loginStatus = ref('')
const confirm_password = ref(null)
const isLogin = ref(false)
if (token) {
    isLogin.value = true
    getUserDetails()
}

const handleLogin = async () => {
    try {
        const res = await axios.post(
            'http://localhost:5000/login?include_auth_token=true',
            {
                email: email.value,
                password: password.value
            },
            {
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        )

        token = res.data.response.user.authentication_token
        localStorage.setItem('auth_token', token)  // Store token for future use

        // Optionally, redirect or show success
        console.log('Login successful!')
        isLogin.value = true
        loginStatus.value = 'Successfully Logged in'
        getUserDetails()
        const modalEl = document.getElementById('exampleModalToggle')
        const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl)
        modal.hide()

    } catch (err) {
        loginStatus.value = err.response?.data?.response?.message || 'Login failed.'
        console.log(loginStatus.value)
        isLogin.value = false
    }
}



async function getUserDetails() {
    try {
        //   const token = localStorage.getItem('auth_token')
        const user = await axios.get(
            'http://localhost:5000/user',
            {
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': token
                }
            }
        )

        // console.log(user)
        userStore.user = user.data

        // router.push('/')  // redirect to home or dashboard
    } catch (err) {
        console.log(err)
    }

}


async function handleRegister() {
    try {
        const res = await axios.post(
            'http://localhost:5000/register?include_auth_token=true',
            {
                email: email.value,
                username: username.value,
                password: password.value
            },
            {
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        )

        token = res.data.response.user.authentication_token
        localStorage.setItem('auth_token', token)
        const modalEl = document.getElementById('exampleModalToggle2')
        const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl)
        modal.hide()

        isLogin.value = true
        loginStatus.value = ''
        getUserDetails()

        // router.push('/')  // redirect to home or dashboard
    } catch (err) {
        loginStatus.value = err.response?.data?.response?.errors[0]
        console.log(err)
        isLogin.value = false
    }
}

async function logout() {
    localStorage.removeItem('auth_token')
    token = null
    loginStatus.value = ""
    isLogin.value = false
    // router.push('/login')
}


// async function login(email, password) {
//   const response = await axios.post(`${API_URL}/login?include_auth_token=true`, {
//     email,
//     password
//   })
//   const token = response.data.response.user.authentication_token
//   localStorage.setItem('auth_token', token)
//   return token
// }

// async function getProtected() {
//   const token = localStorage.getItem('auth_token')
//   return axios.get(`${API_URL}/api/protected`, {
//     headers: {
//       'Authentication-Token': token
//     }
//   })
// }

// async function handleLogin() {
//   try {
//     await login(email.value, password.value)
//     const response = await getProtected()
//     message.value = response.data.message
//   } catch (err) {
//     message.value = 'Login failed'
//   }
// }




// function loginqueued(){
//     let form = new FormData()
//     form.append('email', email);
//     form.append('password', password)
//     console.log('loginqueued started')

//     fetch('http://localhost:5000/login', {
//         method: 'POST',
//         body: form
//     })
//     .then(response => response.json())
//     .then(data => {
//         console.log('Success', data)
//     })
//     .catch(error => {
//         console.error('Error:', error)
//     })
// }


function toggleSidebar() {
    console.log('toggleSidebar called')
    sidebar.classList.toggle('collapsed');
    collapse_icon.value = !collapse_icon.value;
    window.dispatchEvent(new Event('resize'));
}

onMounted(() => {
    // getUserDetails();
    console.log('onMounted done');
});

// function getUserDetails() {
//     const path = 'http://localhost:5000/';
//     console.log('yeah, I am in getUserDetails');
//     axios.get(path)
//         .then((res) => {
//             user.value = res.data;
//             console.log(user.value);
//         })
//         .catch((error) => {

//             console.error(error);
//         });
// }


</script>
<template>

    <div class="d-flex">
        <!-- Sidebar -->

        <div id="sidebar" v-bind:class="sidebar_class">


            <a href="#" class="sidebar-item" style="padding: 7px;">
                <i>
                    <svg height="40" width="40" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg"
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
                </i>
                <span class="dancing-script-brand" style="font-weight: 600; font-size: x-large;">Chess</span>
            </a>

            <br>






            <RouterLink to="/" active-class="active" class="sidebar-item">
                <i>
                    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor"
                        class="bi bi-house-door-fill" viewBox="0 0 16 16">
                        <path
                            d="M6.5 14.5v-3.505c0-.245.25-.495.5-.495h2c.25 0 .5.25.5.5v3.5a.5.5 0 0 0 .5.5h4a.5.5 0 0 0 .5-.5v-7a.5.5 0 0 0-.146-.354L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293L8.354 1.146a.5.5 0 0 0-.708 0l-6 6A.5.5 0 0 0 1.5 7.5v7a.5.5 0 0 0 .5.5h4a.5.5 0 0 0 .5-.5" />
                    </svg>
                </i>
                <span>Home</span>
            </RouterLink>


            <RouterLink to="/play" active-class="active" class="sidebar-item">
                <i>
                    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor"
                        class="bi bi-joystick" viewBox="0 0 16 16">
                        <path
                            d="M10 2a2 2 0 0 1-1.5 1.937v5.087c.863.083 1.5.377 1.5.726 0 .414-.895.75-2 .75s-2-.336-2-.75c0-.35.637-.643 1.5-.726V3.937A2 2 0 1 1 10 2" />
                        <path
                            d="M0 9.665v1.717a1 1 0 0 0 .553.894l6.553 3.277a2 2 0 0 0 1.788 0l6.553-3.277a1 1 0 0 0 .553-.894V9.665c0-.1-.06-.19-.152-.23L9.5 6.715v.993l5.227 2.178a.125.125 0 0 1 .001.23l-5.94 2.546a2 2 0 0 1-1.576 0l-5.94-2.546a.125.125 0 0 1 .001-.23L6.5 7.708l-.013-.988L.152 9.435a.25.25 0 0 0-.152.23" />
                    </svg>
                </i><span>Play</span>
            </RouterLink>

            <RouterLink to="/puzzles" active-class="active" class="sidebar-item">
                <i>
                    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor"
                        class="bi bi-puzzle-fill" viewBox="0 0 16 16">
                        <path
                            d="M3.112 3.645A1.5 1.5 0 0 1 4.605 2H7a.5.5 0 0 1 .5.5v.382c0 .696-.497 1.182-.872 1.469a.5.5 0 0 0-.115.118l-.012.025L6.5 4.5v.003l.003.01q.005.015.036.053a.9.9 0 0 0 .27.194C7.09 4.9 7.51 5 8 5c.492 0 .912-.1 1.19-.24a.9.9 0 0 0 .271-.194.2.2 0 0 0 .036-.054l.003-.01v-.008l-.012-.025a.5.5 0 0 0-.115-.118c-.375-.287-.872-.773-.872-1.469V2.5A.5.5 0 0 1 9 2h2.395a1.5 1.5 0 0 1 1.493 1.645L12.645 6.5h.237c.195 0 .42-.147.675-.48.21-.274.528-.52.943-.52.568 0 .947.447 1.154.862C15.877 6.807 16 7.387 16 8s-.123 1.193-.346 1.638c-.207.415-.586.862-1.154.862-.415 0-.733-.246-.943-.52-.255-.333-.48-.48-.675-.48h-.237l.243 2.855A1.5 1.5 0 0 1 11.395 14H9a.5.5 0 0 1-.5-.5v-.382c0-.696.497-1.182.872-1.469a.5.5 0 0 0 .115-.118l.012-.025.001-.006v-.003l-.003-.01a.2.2 0 0 0-.036-.053.9.9 0 0 0-.27-.194C8.91 11.1 8.49 11 8 11s-.912.1-1.19.24a.9.9 0 0 0-.271.194.2.2 0 0 0-.036.054l-.003.01v.002l.001.006.012.025c.016.027.05.068.115.118.375.287.872.773.872 1.469v.382a.5.5 0 0 1-.5.5H4.605a1.5 1.5 0 0 1-1.493-1.645L3.356 9.5h-.238c-.195 0-.42.147-.675.48-.21.274-.528.52-.943.52-.568 0-.947-.447-1.154-.862C.123 9.193 0 8.613 0 8s.123-1.193.346-1.638C.553 5.947.932 5.5 1.5 5.5c.415 0 .733.246.943.52.255.333.48.48.675.48h.238z" />
                    </svg>
                </i><span>Puzzle</span>
            </RouterLink>

            <RouterLink to="/news" active-class="active" class="sidebar-item">
                <i>
                    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor"
                        class="bi bi-newspaper" viewBox="0 0 16 16">
                        <path
                            d="M0 2.5A1.5 1.5 0 0 1 1.5 1h11A1.5 1.5 0 0 1 14 2.5v10.528c0 .3-.05.654-.238.972h.738a.5.5 0 0 0 .5-.5v-9a.5.5 0 0 1 1 0v9a1.5 1.5 0 0 1-1.5 1.5H1.497A1.497 1.497 0 0 1 0 13.5zM12 14c.37 0 .654-.211.853-.441.092-.106.147-.279.147-.531V2.5a.5.5 0 0 0-.5-.5h-11a.5.5 0 0 0-.5.5v11c0 .278.223.5.497.5z" />
                        <path
                            d="M2 3h10v2H2zm0 3h4v3H2zm0 4h4v1H2zm0 2h4v1H2zm5-6h2v1H7zm3 0h2v1h-2zM7 8h2v1H7zm3 0h2v1h-2zm-3 2h2v1H7zm3 0h2v1h-2zm-3 2h2v1H7zm3 0h2v1h-2z" />
                    </svg>
                </i><span>News</span>
            </RouterLink>

            <div class="sidebar-bottom">

                <a class="sidebar-item" v-on:click="toggleSidebar">
                    <i v-if="!collapse_icon">
                        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor"
                            class="bi bi-arrow-bar-left" viewBox="0 0 16 16">
                            <path fill-rule="evenodd"
                                d="M12.5 15a.5.5 0 0 1-.5-.5v-13a.5.5 0 0 1 1 0v13a.5.5 0 0 1-.5.5M10 8a.5.5 0 0 1-.5.5H3.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L3.707 7.5H9.5a.5.5 0 0 1 .5.5" />
                        </svg>
                    </i>
                    <i v-else>
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor"
                            class="bi bi-arrow-bar-right" viewBox="0 0 16 16">
                            <path fill-rule="evenodd"
                                d="M6 8a.5.5 0 0 0 .5.5h5.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 0 0-.708.708L12.293 7.5H6.5A.5.5 0 0 0 6 8m-2.5 7a.5.5 0 0 1-.5-.5v-13a.5.5 0 0 1 1 0v13a.5.5 0 0 1-.5.5" />
                        </svg>
                    </i>
                    <span>Collapse</span>
                </a>

                <a href="" v-if="!token" class="sidebar-item" data-bs-target="#exampleModalToggle"
                    data-bs-toggle="modal">
                    <i>
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                            class="bi bi-box-arrow-in-right" viewBox="0 0 16 16">
                            <path fill-rule="evenodd"
                                d="M6 3.5a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 .5.5v9a.5.5 0 0 1-.5.5h-8a.5.5 0 0 1-.5-.5v-2a.5.5 0 0 0-1 0v2A1.5 1.5 0 0 0 6.5 14h8a1.5 1.5 0 0 0 1.5-1.5v-9A1.5 1.5 0 0 0 14.5 2h-8A1.5 1.5 0 0 0 5 3.5v2a.5.5 0 0 0 1 0z" />
                            <path fill-rule="evenodd"
                                d="M11.854 8.354a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L10.293 7.5H1.5a.5.5 0 0 0 0 1h8.793l-2.147 2.146a.5.5 0 0 0 .708.708z" />
                        </svg>
                    </i>
                    <span>Login</span>
                </a>


                <a v-else href="" v-on:click="logout()" class="sidebar-item">
                    <i>
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                            class="bi bi-box-arrow-right" viewBox="0 0 16 16">
                            <path fill-rule="evenodd"
                                d="M10 12.5a.5.5 0 0 1-.5.5h-8a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 .5.5v2a.5.5 0 0 0 1 0v-2A1.5 1.5 0 0 0 9.5 2h-8A1.5 1.5 0 0 0 0 3.5v9A1.5 1.5 0 0 0 1.5 14h8a1.5 1.5 0 0 0 1.5-1.5v-2a.5.5 0 0 0-1 0z" />
                            <path fill-rule="evenodd"
                                d="M15.854 8.354a.5.5 0 0 0 0-.708l-3-3a.5.5 0 0 0-.708.708L14.293 7.5H5.5a.5.5 0 0 0 0 1h8.793l-2.147 2.146a.5.5 0 0 0 .708.708z" />
                        </svg>
                    </i>
                    <span>Logout</span>
                </a>

                <!-- Button trigger modal -->
                <!-- <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#staticBackdrop">
                    Launch static backdrop modal
                </button> -->



                <a class="sidebar-item">
                    <i>
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                            class="bi bi-person-fill" viewBox="0 0 16 16">
                            <path d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6" />
                        </svg>
                    </i>

                    <span>Profile</span>

                    <!-- <span v-if="user == ''">Profile</span> -->
                    <!-- <span v-else>{{ user[0]['username'] }}</span> -->
                </a>


                <a class="sidebar-item">
                    <i>
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                            class="bi bi-gear-fill" viewBox="0 0 16 16">
                            <path
                                d="M9.405 1.05c-.413-1.4-2.397-1.4-2.81 0l-.1.34a1.464 1.464 0 0 1-2.105.872l-.31-.17c-1.283-.698-2.686.705-1.987 1.987l.169.311c.446.82.023 1.841-.872 2.105l-.34.1c-1.4.413-1.4 2.397 0 2.81l.34.1a1.464 1.464 0 0 1 .872 2.105l-.17.31c-.698 1.283.705 2.686 1.987 1.987l.311-.169a1.464 1.464 0 0 1 2.105.872l.1.34c.413 1.4 2.397 1.4 2.81 0l.1-.34a1.464 1.464 0 0 1 2.105-.872l.31.17c1.283.698 2.686-.705 1.987-1.987l-.169-.311a1.464 1.464 0 0 1 .872-2.105l.34-.1c1.4-.413 1.4-2.397 0-2.81l-.34-.1a1.464 1.464 0 0 1-.872-2.105l.17-.31c.698-1.283-.705-2.686-1.987-1.987l-.311.169a1.464 1.464 0 0 1-2.105-.872zM8 10.93a2.929 2.929 0 1 1 0-5.86 2.929 2.929 0 0 1 0 5.858z" />
                        </svg>
                    </i>

                    <span>Settings</span>
                </a>

            </div>

        </div>

        <!-- Content -->
        <div id="content" class="flex-grow-1">

            <!-- Modal -->
            <div class="modal fade" id="exampleModalToggle" data-bs-backdrop="static" data-bs-keyboard="false"
                aria-hidden="true" aria-labelledby="exampleModalToggleLabel" tabindex="-1">
                <div class="modal-dialog modal-dialog-centered">

                    <form @submit.prevent="handleLogin">

                        <div class="modal-content modal-form">
                            <div class="modal-header border-0">
                                <h1 class="modal-title fs-5" id="exampleModalToggleLabel">Login</h1>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"
                                    aria-label="Close"></button>
                            </div>
                            <div class="modal-body">

                                <div class="mb-3">
                                    <label for="exampleFormControlInput1" class="form-label">Email address</label>
                                    <input v-model="email" type="email" class="form-control"
                                        id="exampleFormControlInput1" placeholder="name@example.com" required>
                                </div>
                                <div class="mb-3">
                                    <label for="inputPassword5" class="form-label">Password</label>
                                    <input v-model="password" minlength="8" type="password" id="inputPassword5"
                                        class="form-control" aria-describedby="passwordHelpBlock" required>
                                    <div id="passwordHelpBlock" style="color: grey;" class="form-text">
                                        Your password must be 8-20 characters long, contain letters and numbers, and
                                        must
                                        not contain spaces, special characters, or emoji.
                                    </div>
                                </div>

                            </div>

                            <div class="row">
                                <div class="col-9 border-0">
                                    <a style="margin-left: 12px; font-size: small; color: #385C8E;"
                                        data-bs-target="#exampleModalToggle2" data-bs-toggle="modal">
                                        New to Chessmate.com? Register Now!
                                    </a>
                                </div>

                                <div class="col-3 border-0" style="text-align: end;">
                                    <button type="submit" class="btn btn-success"
                                        style="margin-right: 8px; margin-bottom: 8px;">Login</button>
                                </div>


                            </div>
                            <div class="row" style="color: yellow; text-align: center;">
                                <div class="col">
                                    {{ loginStatus }}
                                </div>

                            </div>





                        </div>

                    </form>


                </div>
            </div>
            <div class="modal fade" id="exampleModalToggle2" data-bs-backdrop="static" data-bs-keyboard="false"
                aria-hidden="true" aria-labelledby="exampleModalToggleLabel2" tabindex="-1">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content modal-form">
                        <form @submit.prevent="handleRegister()">
                            <div class="modal-header border-0">
                                <h1 class="modal-title fs-5" id="exampleModalToggleLabel2">Register</h1>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"
                                    aria-label="Close"></button>
                            </div>
                            <div class="modal-body">

                                <div class="mb-3">
                                    <label for="exampleFormControlInput1" class="form-label">Email address</label>
                                    <input v-model="email" type="email" class="form-control"
                                        id="exampleFormControlInput1" placeholder="name@example.com" required>
                                </div>

                                <div class="mb-3">
                                    <label for="exampleFormControlInput1" class="form-label">Username</label>
                                    <input v-model="username" type="text" class="form-control"
                                        id="exampleFormControlInput1" required>
                                </div>

                                <div class="mb-3">
                                    <label for="inputPassword5" class="form-label">Password</label>
                                    <input v-model="password" minlength="8" type="password" id="inputPassword5" class="form-control"
                                        aria-describedby="passwordHelpBlock" required>
                                    <div id="passwordHelpBlock" style="color: grey;" class="form-text">
                                        Your password must be 8-20 characters long, contain letters and numbers, and
                                        must
                                        not contain spaces, special characters, or emoji.
                                    </div>
                                </div>
                                <div class="mb-3">
                                    <label for="inputPassword5" class="form-label">Confirm Password</label>
                                    <input v-model="confirm_password" type="password" id="inputPassword5"
                                        class="form-control" aria-describedby="passwordHelpBlock" required>
                                    <div v-if="password != confirm_password && confirm_password" id="passwordHelpBlock"
                                        style="color: red;" class="form-text">
                                        Password is not matching
                                    </div>
                                    <div id="passwordHelpBlock" style="color: grey;" class="form-text">
                                        Retype your password
                                    </div>
                                </div>



                            </div>
                            <div class="border-0">
                                <div class="row">
                                    <div class="col-9">
                                        <a style="margin-left: 12px; font-size: small; color: #385C8E;"
                                            data-bs-target="#exampleModalToggle" data-bs-toggle="modal">Already have an
                                            account? Login</a>
                                    </div>
                                    <div class="col-3" style="text-align: end;">
                                        <button v-if="password!=confirm_password" type="submit" class="btn btn-success"
                                            style="margin-right: 8px; margin-bottom: 8px;" disabled>Register</button>
                                        <button v-else type="submit" class="btn btn-success"
                                            style="margin-right: 8px; margin-bottom: 8px;">Register</button>
                                    </div>
                                </div>



                                <div class="row">
                                    <div class="col" style="text-align: center; color: yellow;">
                                        {{ loginStatus }}
                                    </div>
                                </div>
                            </div>
                        </form>


                    </div>
                </div>
            </div>

            <RouterView></RouterView>



        </div>
    </div>



</template>

<style scoped>
/* Styling for sidebar and content */
@import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400..700&display=swap');

.d-flex {
    display: flex;
    align-items: stretch;
}

.dancing-script-brand {
    font-family: "Tiny5", serif;
    font-optical-sizing: auto;
    font-weight: 400;
    font-style: normal;
}

/* #sidebar {
    width: 130px;
    height: 100vh;
    background-color: #343a40;
    color: white;
    transition: width 0.3s;
} */

#sidebar {
    position: fixed;
    top: 0;
    bottom: 0;
    /* stretch from top to bottom of viewport */
    left: 0;
    width: 130px;
    background-color: #343a40;
    display: flex;
    flex-direction: column;
}

/* #sidebar.collapsed {
    width: 50px;
} */

.sidebar-bottom {
    margin-top: auto;
    /* pushes this block to the bottom */
    display: flex;
    flex-direction: column;
}

#sidebar.collapsed {
    width: 50px;
}

#sidebar.collapsed~#content {
    margin-left: 50px;
}

.sidebar-item {
    display: flex;
    align-items: center;
    padding-left: 15px;
    padding-top: 5px;
    padding-bottom: 5px;
    color: white;
    text-decoration: none;
    transition: all 0.3s;
    /* margin-bottom: 5px; */
}

.sidebar-item:hover {
    background-color: #495057;
}

.sidebar-item i {
    font-size: 1.2rem;
}

.sidebar-item span {
    margin-left: 10px;
    transition: opacity 0.3s;
}

#sidebar.collapsed .sidebar-item span {
    opacity: 0;
}

/* #content {
    margin-left: 10px;
    transition: margin-left 0.3s;
} */

#content {
    margin-left: 130px;
    /* push your content over so it doesn’t sit under the fixed sidebar */
    transition: margin-left .3s;
}

.active {
    color: green;
    font-size: large;
    font-weight: 800;
    background-color: #495057;
}

input::placeholder {
    color: grey;
}

input {
    background-color: #212529;
    border-color: #495057;
    color: white;
}

.modal-form {
    background-color: #212529;
    color: white;
}

input:focus {
    background-color: #212529;
    /* keep same background on focus */
    color: white;
}
</style>