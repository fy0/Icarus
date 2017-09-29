import Vue from 'vue'
import Router from 'vue-router'

import AccountSignin from '@/components/account/signin.vue'
import AccountSignup from '@/components/account/signup.vue'

import Forum from '@/components/forum/forum.vue'
import ForumRecent from '@/components/forum/recent.vue'
import ForumBoard from '@/components/forum/board.vue'

import Admin from '@/components/admin/admin.vue'
import AdminForumBoard from '@/components/admin/forum/board.vue'

import About from '@/components/about.vue'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/account/signin',
            name: 'account_signin',
            component: AccountSignin
        },
        {
            path: '/account/signup',
            name: 'account_signup',
            component: AccountSignup
        },
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
            path: '/board/:id(\\S+)/:name(.+)?',
            name: 'forum_board',
            component: ForumBoard
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
