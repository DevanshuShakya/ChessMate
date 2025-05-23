import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import PlayView from '@/views/PlayView.vue'
import PuzzlesView from '@/views/PuzzlesView.vue'
import NewsView from '@/views/NewsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/play',
      name:'play',
      component: PlayView,
    },
    {
      path: '/puzzles',
      name:'puzzles',
      component: PuzzlesView,
    },
    {
      path: '/news',
      name:'news',
      component: NewsView,
    },
  ],
})

export default router
