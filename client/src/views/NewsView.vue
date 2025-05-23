<script setup>
import axios from 'axios';
import { reactive, onMounted } from 'vue'

let news = reactive()

const getNews = async () => {
    try {
        news = await axios.get(
            'http://localhost:5000/api/chess-news',
            {
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        )
        console.log(news)

    } catch (err) {
        console.log(err)
    }
}

onMounted(() => {
    getNews()
});



</script>
<template>
    <div class="container">
        <div class="row">
            <div class="col">
                <!-- {{ news.data }} -->
            </div>
        </div>
    </div>
</template>
