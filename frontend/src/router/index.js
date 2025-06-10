import Vue from 'vue'
import Router from 'vue-router'
import HomePage from '../views/HomePage.vue'
import NPVView from '../views/NPVView.vue'

Vue.use(Router)

export default new Router({
    mode: 'hash',
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomePage
        },
        {
            path: '/npv',
            name: 'npv',
            component: NPVView
        }
    ]
})
