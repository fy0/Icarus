import Vue from 'vue'
import Router from 'vue-router'

import AccountSignin from '@/components/account/signin.vue'
import AccountSignup from '@/components/account/signup.vue'

import Forum from '@/components/forum/forum.vue'
import ForumRecent from '@/components/forum/recent.vue'
import ForumBoard from '@/components/forum/board.vue'
import ForumTopcEdit from '@/components/forum/topic_edit.vue'
import ForumTopic from '@/components/forum/topic.vue'

import Admin from '@/components/admin/admin.vue'
import AdminForumBoard from '@/components/admin/forum/board.vue'

import About from '@/components/about.vue'

Vue.use(Router)

export default new Router({
    routes: [
        // 登录
        {
            path: '/account/signin',
            name: 'account_signin',
            component: AccountSignin
        },
        // 注册
        {
            path: '/account/signup',
            name: 'account_signup',
            component: AccountSignup
        },

        // 用户页面
        {
            path: '/user/:id(\\S+)',
            name: 'user_page',
            component: About
        },

        // 主页面
        {
            path: '/',
            name: 'forum',
            component: Forum
        },
        // 论坛 - 最近发布
        {
            path: '/recent',
            name: 'forum_recent',
            component: ForumRecent
        },
        // 论坛 - 板块页面
        {
            path: '/board/:id(\\S+)/:page(\\d+)?/:name(.+)?',
            name: 'forum_board',
            component: ForumBoard
        },
        // 论坛 - 主题新建
        {
            path: '/topic/new',
            name: 'forum_topic_new',
            component: ForumTopcEdit
        },
        // 论坛 - 主题编辑
        {
            path: '/topic/edit/:id(\\S+)',
            name: 'forum_topic_edit',
            component: ForumTopcEdit
        },
        // 论坛 - 文章页面
        {
            path: '/topic/:id(\\S+)',
            name: 'forum_topic',
            component: ForumTopic
        },

        // 管理
        {
            path: '/admin',
            name: 'admin',
            component: Admin
        },
        // 管理 - 板块
        {
            path: '/admin/forum/board',
            name: 'admin_forum_board',
            component: AdminForumBoard
        },

        // 关于
        {
            path: '/about',
            name: 'about',
            component: About
        }
    ]
})
