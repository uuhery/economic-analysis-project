import Vue from 'vue'
import Router from 'vue-router'
import HomePage from '../views/HomePage.vue'
import Estimation from '../views/Estimation.vue'
import Finance from '../views/Finance.vue'
import Risk from '../views/Risk.vue'
import Scheduling from '../views/Scheduling'

Vue.use(Router)

export default new Router({
    mode: 'hash',
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomePage
        },
        { path: '/estimation', name: 'estimation', component: Estimation },
        { path: '/finance', name: 'finance', component: Finance },
        { path: '/risk', name: 'risk', component: Risk },
        { path: '/scheduling', name: 'scheduling', component: Scheduling}

    ]
})
