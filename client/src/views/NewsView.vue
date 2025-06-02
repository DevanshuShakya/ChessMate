<script setup>
import axios from 'axios';
import { reactive, onMounted, ref } from 'vue'

// let news = { "choices": [{ "delta": { "content": "", "role": "assistant" }, "finish_reason": "stop", "index": 0, "logprobs": null, "message": { "annotations": null, "audio": null, "content": "```json\n[\n  {\n    \"title\": \"Magnus Carlsen Leads Norway Chess After Win Over Fabiano Caruana\",\n    \"summary\": \"Magnus Carlsen extended his lead in the prestigious Norway Chess tournament by defeating Fabiano Caruana, holding a 1.5-point advantage at the top of the standings. Earlier in the tournament, Carlsen also secured a key victory over world champion D Gukesh in the opening round.\"\n  },\n  {\n    \"title\": \"IM Reza Mahdavi Wins Maiden Bullet Brawl Title\",\n    \"summary\": \"Iranian International Master Reza Mahdavi claimed his first Bullet Brawl victory, finishing ahead of 175 titled players. Mahdavi became only the second IM ever to win the event, posting an impressive 62.5/73 score and a final tally of 221.\"\n  },\n  {\n    \"title\": \"Gukesh Defeats Hikaru Nakamura in Norway Chess\",\n    \"summary\": \"World champion D Gukesh marked his 19th birthday by defeating world No. 2 Hikaru Nakamura in the Norway Chess tournament, ending a losing streak and earning three valuable points.\"\n  },\n  {\n    \"title\": \"Praggnanandhaa Wins Tata Steel Chess Masters in Dramatic Tie-Break\",\n    \"summary\": \"Indian Grandmaster R Praggnanandhaa triumphed over world champion D Gukesh in a sudden-death tie-breaker to win the 2025 Tata Steel Chess Masters, following a tense final round where both players had finished tied.\"\n  },\n  {\n    \"title\": \"Controversy and Feud Mark Freestyle Chess Grand Tour\",\n    \"summary\": \"The ongoing Freestyle Chess Grand Tour has been notable not only for its strong field\u2014including Gukesh, Carlsen, and Caruana\u2014but also for a public dispute between Carlsen and the tour's promoters with FIDE, the world chess federation.\"\n  },\n  {\n    \"title\": \"Praggnanandhaa Claims First Grand Chess Tour Title at Superbet Classic\",\n    \"summary\": \"Indian GM R Praggnanandhaa won his first Grand Chess Tour title by defeating Maxime Vachier-Lagrave at the Superbet Classic, reinforcing his rising status on the global stage.\"\n  },\n  {\n    \"title\": \"Former World Champion Boris Spassky Dies at 88\",\n    \"summary\": \"Legendary former world chess champion Boris Spassky, most famous for his 1972 World Championship match against Bobby Fischer, has passed away at the age of 88.\"\n  },\n  {\n    \"title\": \"Chess Grandmaster Arrested After Physical Altercation\",\n    \"summary\": \"A Russian chess grandmaster was arrested after allegedly punching a videographer in frustration following a tournament loss, in another incident highlighting tensions in elite chess.\"\n  }\n]\n```", "function_call": null, "refusal": null, "role": "assistant", "tool_calls": null } }], "citations": ["https://www.chess.com/news", "https://en.chessbase.com", "https://www.espn.com/chess/", "https://www.the-independent.com/topic/chess", "https://sports.ndtv.com/chess/news"], "created": 1748786532, "id": "3cada06f-af89-46ea-b7fe-62463ad8eac9", "model": "sonar-pro", "object": "chat.completion", "search_results": [{ "date": null, "title": "Chess News and Event Coverage", "url": "https://www.chess.com/news" }, { "date": null, "title": "ChessBase: Chess News", "url": "https://en.chessbase.com" }, { "date": null, "title": "Chess - Latest News, Updates - ESPN", "url": "https://www.espn.com/chess/" }, { "date": null, "title": "Chess - latest news, breaking stories and comment - The Independent", "url": "https://www.the-independent.com/topic/chess" }, { "date": null, "title": "Chess News - Latest Chess Updates & Information, Live Chess Score", "url": "https://sports.ndtv.com/chess/news" }], "service_tier": null, "system_fingerprint": null, "usage": { "completion_tokens": 597, "completion_tokens_details": null, "prompt_tokens": 41, "prompt_tokens_details": null, "search_context_size": "low", "total_tokens": 638 } }

const news = ref([])

const getNews = async () => {
    try {
        let res = await axios.get(
            'http://localhost:5000/api/chess-news',
            {
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        )
        news.value = res.data["articles"]

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
            <div class="col-10">
                <h1 style="margin-top: 20px; margin-bottom: 20px;">
                    <svg style="margin-right: 5px;" xmlns="http://www.w3.org/2000/svg" width="55" height="55"
                        fill="green" class="bi bi-newspaper" viewBox="0 0 16 16">
                        <path
                            d="M0 2.5A1.5 1.5 0 0 1 1.5 1h11A1.5 1.5 0 0 1 14 2.5v10.528c0 .3-.05.654-.238.972h.738a.5.5 0 0 0 .5-.5v-9a.5.5 0 0 1 1 0v9a1.5 1.5 0 0 1-1.5 1.5H1.497A1.497 1.497 0 0 1 0 13.5zM12 14c.37 0 .654-.211.853-.441.092-.106.147-.279.147-.531V2.5a.5.5 0 0 0-.5-.5h-11a.5.5 0 0 0-.5.5v11c0 .278.223.5.497.5z" />
                        <path
                            d="M2 3h10v2H2zm0 3h4v3H2zm0 4h4v1H2zm0 2h4v1H2zm5-6h2v1H7zm3 0h2v1h-2zM7 8h2v1H7zm3 0h2v1h-2zm-3 2h2v1H7zm3 0h2v1h-2zm-3 2h2v1H7zm3 0h2v1h-2z" />
                    </svg>
                    Chess News
                </h1>

                <div v-for="n in news">


                    <a style="padding: 10px;" :href="n['url']" class="list-group-item list-group-item-action"
                        aria-current="true">
                        <hr style="margin: 5px;">
                        <!-- <div style="margin-bottom: 10px;" class="d-flex w-100 justify-content-between"> -->
                        <div class="row d-flex w-100 justify-content-between">
                            <div class="col-10">
                                <h5 class="mb-1">{{ n['title'] }}</h5>
                                <small> - {{ n['author'] }}</small>
                            </div>
                            <div class="col-2">
                                <small>{{ n["publishedAt"] }}</small>
                            </div>
                        </div>
                        <!-- </div> -->

                        <p class="mb-1">{{ n['description'] }}</p>
                        <small>Source: {{ n['source']['name'] }}</small>
                    </a>


                </div>


            </div>

        </div>
    </div>
</template>

<style scoped>
.newstyle {
    background-color: #a6a6a6;
}
</style>
