import Vue from 'vue'
import Router from 'vue-router'
import Forum from '@/components/forum/forum.vue'
import About from '@/components/about.vue'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'forum',
            component: Forum
        },
        {
            path: '/about',
            name: 'about',
            component: About
        }
    ]
})
