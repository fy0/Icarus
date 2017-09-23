import Vue from 'vue'
import Router from 'vue-router'
import Forum from '@/components/forum/forum.vue'
import ForumRecent from '@/components/forum/recent.vue'
import About from '@/components/about.vue'

import Admin from '@/components/admin/admin.vue'
import AdminForumBoard from '@/components/admin/forum/board.vue'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'forum',
            component: Forum
        },
        {
            path: '/recent',
            name: 'forum_recent',
            component: ForumRecent
        },
        {
            path: '/admin',
            name: 'admin',
            component: Admin
        },
        {
            path: '/admin',
            name: 'admin',
            component: Admin
        },
        {
            path: '/admin/forum/board',
            name: 'admin_forum_board',
            component: AdminForumBoard
        },
        {
            path: '/about',
            name: 'about',
            component: About
        }
    ]
})
