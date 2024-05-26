import { createRouter, createWebHistory } from 'vue-router'
import HomeView from "@/views/HomeView.vue";
import SignUpView from "@/views/SignUpView.vue";
import LoginView from "@/views/LoginView.vue";
import SearchView from "@/views/SearchView.vue";
import DetailView from "@/views/DetailView.vue";
import ProfileView from "@/views/ProfileView.vue";
import ProfileUpdateView from "@/views/ProfileUpdateView.vue";
import ArticleView from "@/views/ArticleView.vue";


const routes = [

  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/signUp',
    name: 'signUp',
    component: SignUpView,
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
  },
  {
    path: '/search/:query',
    name: 'search',
    component: SearchView,
    props: true
  },
  {
    path: '/detail/:id',
    name: 'detail',
    component: DetailView,
    props: true
  },
  {
    path: '/profile/:username',
    name: 'profile',
    component: ProfileView,
    props: true
  },
  {
    path: '/profile/update/:username',
    name: 'profileUpdate',
    component: ProfileUpdateView,
    props: true
  },
  {
    path: '/article/:id',
    name: 'article',
    component: ArticleView,
    props: true
  },
  {
    path: '/passwordChange',
    name: 'passwordChange',
    component: () => import('@/views/PasswordChangeView.vue'),
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes, // short for `routes: routes`
})

export default router
