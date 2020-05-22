import Vue from 'vue'
import Router from 'vue-router'

import AccountSignin from '@/views/account/signin.vue'
import AccountSignup from '@/views/account/signup.vue'
import AccountSignupByEmailDone from '@/views/account/signup_by_email_done.vue'
import AccountUserPage from '@/views/account/userpage.vue'
import AccountNotif from '@/views/account/notif.vue'
// import AccountOAuth from '@/views/account/oauth.vue'
// import AccountOAuthCheck from '@/views/account/oauth_check.vue'
import AccountPasswordReset from '@/views/account/password_reset.vue'
import AccountPasswordResetRequest from '@/views/account/password_reset_req.vue'

import Setting from '@/views/settings/setting.vue'
import SettingUserinfoMe from '@/views/settings/userinfo/me.vue'
import SettingUserinfoUpload from '@/views/settings/userinfo/upload.vue'
import SettingUserinfoPrivacy from '@/views/settings/userinfo/privacy.vue'
import SettingSecurityPassword from '@/views/settings/security/password.vue'
import SettingSecurityOAuth from '@/views/settings/security/oauth.vue'

import Admin from '@/views/admin/admin.vue'
import AdminForumBoard from '@/views/admin/forum/board.vue'
import AdminForumTopic from '@/views/admin/forum/topic.vue'
import AdminCommonUser from '@/views/admin/common/user.vue'
import AdminCommonComment from '@/views/admin/common/comment.vue'
import AdminCommonManageLog from '@/views/admin/common/manage-log.vue'

// import ForumBoards from '@/views/forum/boards.vue'
import ForumMain from '@/views/forum/main.vue'
import ForumTopic from '@/views/forum/topic.vue'
import ForumTopicEdit from '@/views/forum/topic-edit.vue'

import WikiMain from '@/views/wiki/main.vue'
import WikiEdit from '@/views/wiki/wiki-edit.vue'
import WikiArticle from '@/views/wiki/article.vue'
import WikiList from '@/views/wiki/list.vue'
import WikiRandom from '@/views/wiki/random.vue'
import WikiHistory from '@/views/wiki/history.vue'

import Search from '@/views/search.vue'
import About from '@/views/about.vue'

// 404 页面较为特殊，通常是以组件的形式被使用
import NotFoundComponent from '@/components/404.vue'

Vue.use(Router)

export function createRouter () {
  return new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
      // 主页面
      {
        path: '/',
        name: 'index',
        component: ForumMain
      },

      // 用户 - 登录
      {
        path: '/account/signin',
        name: 'account_signin',
        component: AccountSignin
      },
      // 用户 - 注册
      {
        path: '/account/signup',
        name: 'account_signup',
        component: AccountSignup
      },
      // 用户 - 邮件激活
      {
        path: '/account/signup_by_email_done',
        name: 'account_signup_by_email_done',
        component: AccountSignupByEmailDone
      },
      // 用户 - 申请重置密码
      {
        path: '/account/lost_password',
        name: 'account_password_reset_request',
        component: AccountPasswordResetRequest
      },
      // 用户 - 重置密码
      {
        path: '/account/password_reset',
        name: 'account_password_reset',
        component: AccountPasswordReset
      },

      // 用户 - 个人主页
      {
        path: '/user/:id(\\S+)',
        name: 'account_userpage',
        component: AccountUserPage
      },

      // 用户 - 个人提醒
      {
        path: '/notifications',
        name: 'account_notif',
        component: AccountNotif
      },

      // 论坛 - 主页面
      {
        path: '/forum',
        name: 'forum',
        redirect: { name: 'forum_main', params: { page: 1 } }
      },
      // 论坛 - 板块列表
      // {
      //     path: '/forum/boards',
      //     name: 'forum_boards',
      //     component: ForumBoards
      // },
      // 论坛 - 主面板
      {
        path: '/r/:page(\\d+)',
        name: 'forum_main',
        component: ForumMain
      },
      // 论坛 - 主面板 - 板块页面
      {
        path: '/b/:id([a-fA-F0-9]+)/:page(\\d+)?/:name(.+)?',
        name: 'forum_board',
        component: ForumMain
      },
      // 论坛 - 主题新建
      {
        path: '/topic/new',
        name: 'forum_topic_new',
        component: ForumTopicEdit
        // component: () => import(/* webpackChunkName: "topic-edit" */ '@/views/forum/topic-edit.vue')
      },
      // 论坛 - 主题编辑
      {
        path: '/topic/edit/:id(\\S+)',
        name: 'forum_topic_edit',
        component: ForumTopicEdit
        // component: () => import(/* webpackChunkName: "topic-edit" */ '@/views/forum/topic-edit.vue')
      },
      // 论坛 - 文章页面
      {
        path: '/topic/:id([a-fA-F0-9]+)',
        name: 'forum_topic',
        component: ForumTopic
      },

      // Wiki - 主页
      {
        path: '/wiki',
        name: 'wiki',
        component: WikiMain
        // component: () => import(/* webpackChunkName: "wiki" */ '@/views/wiki/main.vue')
      },
      // Wiki - 随机页面
      {
        path: '/wiki/random',
        name: 'wiki_random',
        component: WikiRandom
        // component: () => import(/* webpackChunkName: "wiki" */ '@/views/wiki/random.vue')
      },
      // Wiki - 历史
      {
        path: '/wiki/history/:id([a-fA-F0-9]+)',
        name: 'wiki_history',
        component: WikiHistory
        // component: () => import(/* webpackChunkName: "wiki" */ '@/views/wiki/history.vue')
      },
      // Wiki - 列表页
      {
        path: '/wiki/list/:page(\\d+)?',
        name: 'wiki_list',
        component: WikiList
        // component: () => import(/* webpackChunkName: "wiki" */ '@/views/wiki/list.vue')
      },
      // Wiki - 文章页面 - id
      {
        path: '/wiki/id/:id([a-fA-F0-9]+)',
        name: 'wiki_article_by_id',
        component: WikiArticle
        // component: () => import(/* webpackChunkName: "wiki" */ '@/views/wiki/article.vue')
      },
      // Wiki - 文章页面 - ref
      {
        path: '/wiki/r/:ref',
        name: 'wiki_article_by_ref',
        component: WikiArticle
        // component: () => import(/* webpackChunkName: "wiki" */ '@/views/wiki/article.vue')
      },
      // Wiki - 新建
      {
        path: '/wiki/new',
        name: 'wiki_article_new',
        component: WikiEdit
        // component: () => import(/* webpackChunkName: "wiki-edit" */ '@/views/wiki/wiki-edit.vue')
      },
      // Wiki - 编辑
      {
        path: '/wiki/edit/:id(\\S+)',
        name: 'wiki_article_edit',
        component: WikiEdit
        // component: () => import(/* webpackChunkName: "wiki-edit" */ '@/views/wiki/wiki-edit.vue')
      },
      // Wiki - 派生
      // {
      //     path: '/wiki/fork/:id(\\S+)',
      //     name: 'wiki_article_fork',
      //     component: () => import(/* webpackChunkName: "wiki-edit" */ '@/views/wiki/wiki-edit.vue')
      // },

      // 设置
      {
        path: '/setting',
        name: 'setting',
        redirect: { name: 'setting_user_me' },
        component: Setting
      },
      // 设置 - 用户 - 个人信息
      {
        path: '/setting/user/me',
        name: 'setting_user_me',
        component: SettingUserinfoMe
      },
      // 设置 - 用户 - 我的上传
      {
        path: '/setting/user/upload',
        name: 'setting_user_upload',
        component: SettingUserinfoUpload
      },
      // 设置 - 用户 - 隐私设置
      {
        path: '/setting/user/privacy',
        name: 'setting_user_privacy',
        component: SettingUserinfoPrivacy
      },
      // 设置 - 安全 - 修改密码
      {
        path: '/setting/security/password',
        name: 'setting_security_password',
        component: SettingSecurityPassword
      },
      // 设置 - 安全 - 绑定账号（第三方登录）
      {
        path: '/setting/security/oauth',
        name: 'setting_security_oauth',
        component: SettingSecurityOAuth
      },

      // 管理
      {
        path: '/admin',
        name: 'admin',
        component: Admin
        // component: () => import(/* webpackChunkName: "admin" */ '@/views/admin/admin.vue')
      },
      // 管理 - 社区 - 板块
      {
        path: '/admin/forum/board',
        name: 'admin_forum_board',
        component: AdminForumBoard
        // component: () => import(/* webpackChunkName: "admin" */ '@/views/admin/forum/board.vue')
      },
      // 管理 - 社区 - 文章
      {
        path: '/admin/forum/topic/:page(\\d+)?/:name(.+)?',
        name: 'admin_forum_topic',
        component: AdminForumTopic
        // component: () => import(/* webpackChunkName: "admin" */ '@/views/admin/forum/topic.vue')
      },

      // 管理 - 综合 - 用户
      {
        path: '/admin/common/user/:page(\\d+)?/:name(.+)?',
        name: 'admin_common_user',
        component: AdminCommonUser
        // component: () => import(/* webpackChunkName: "admin" */ '@/views/admin/common/user.vue')
      },
      // 管理 - 综合 - 评论
      {
        path: '/admin/common/comment/:page(\\d+)?/:name(.+)?',
        name: 'admin_common_comment',
        component: AdminCommonComment
        // component: () => import(/* webpackChunkName: "admin" */ '@/views/admin/common/comment.vue')
      },
      // 管理 - 综合 - 管理日志
      {
        path: '/admin/common/log/manage/:page(\\d+)?/:name(.+)?',
        name: 'admin_common_manage_log',
        component: AdminCommonManageLog
        // component: () => import(/* webpackChunkName: "admin" */ '@/views/admin/common/manage-log.vue')
      },

      {
        path: '*',
        component: NotFoundComponent
      },

      // 搜索
      {
        path: '/search',
        name: 'search',
        component: Search
        // component: () => import(/* webpackChunkName: "search" */ '@/views/search.vue')
      },

      // 关于
      {
        path: '/about',
        name: 'about',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        // component: () => import(/* webpackChunkName: "about" */ '@/views/about.vue')
        component: About
      }

      // // OAuth
      // {
      //     path: '/account/oauth',
      //     name: 'account_oauth',
      //     component: AccountOAuth
      // },

      // // OAuth Registe Check
      // {
      //     path: '/account/oauth_check',
      //     name: 'account_oauth_check',
      //     component: AccountOAuthCheck
      // }
    ]
  })
}
