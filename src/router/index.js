import Vue from 'vue'
import Router from 'vue-router'

import AccountSignin from '@/components/account/signin.vue'
import AccountSignup from '@/components/account/signup.vue'
import AccountUserPage from '@/components/account/userpage.vue'
import AccountNotif from '@/components/account/notif.vue'

import Forum from '@/components/forum/forum.vue'
import ForumRecent from '@/components/forum/recent.vue'
import ForumBoard from '@/components/forum/board.vue'
import ForumTopcEdit from '@/components/forum/topic_edit.vue'
import ForumTopic from '@/components/forum/topic.vue'

import Admin from '@/components/admin/admin.vue'
import AdminForumBoard from '@/components/admin/forum/board.vue'
import AdminForumTopic from '@/components/admin/forum/topic.vue'
import AdminCommonUser from '@/components/admin/common/user.vue'
import AdminCommonComment from '@/components/admin/common/comment.vue'

import About from '@/components/about.vue'

Vue.use(Router)

export default new Router({
    mode: 'history',
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
            name: 'account_userpage',
            component: AccountUserPage
        },

        // 个人提醒
        {
            path: '/notifications',
            name: 'account_notif',
            component: AccountNotif
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
            path: '/board/:id([a-fA-F0-9]+)/:page(\\d+)?/:name(.+)?',
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
            path: '/topic/:id([a-fA-F0-9]+)',
            name: 'forum_topic',
            component: ForumTopic
        },

        // 管理
        {
            path: '/admin',
            name: 'admin',
            component: Admin
        },
        // 管理 - 社区 - 板块
        {
            path: '/admin/forum/board',
            name: 'admin_forum_board',
            component: AdminForumBoard
        },
        // 管理 - 社区 - 文章
        {
            path: '/admin/forum/topic/:page(\\d+)?/:name(.+)?',
            name: 'admin_forum_topic',
            component: AdminForumTopic
        },

        // 管理 - 综合 - 用户
        {
            path: '/admin/common/user/:page(\\d+)?/:name(.+)?',
            name: 'admin_common_user',
            component: AdminCommonUser
        },
        // 管理 - 综合 - 评论
        {
            path: '/admin/common/comment/:page(\\d+)?/:name(.+)?',
            name: 'admin_common_comment',
            component: AdminCommonComment
        },

        // 关于
        {
            path: '/about',
            name: 'about',
            component: About
        }
    ]
})
