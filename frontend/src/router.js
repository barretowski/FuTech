import { createRouter, createWebHistory } from 'vue-router'
import ConsultaJogador from './components/ConsultaJogador.vue'

const routes = [
  {
    path: '/',
    name: 'ConsultaJogador',
    component: ConsultaJogador
  }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
