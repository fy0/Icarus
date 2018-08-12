import Vue from 'vue'
import Router from 'vue-router'

import AccountSignin from '@/components/account/signin.vue'
import AccountSignup from '@/components/account/signup.vue'
import AccountUserPage from '@/components/account/userpage.vue'
import AccountNotif from '@/components/account/notif.vue'
import AccountOAuth from '@/components/account/oauth.vue'
import AccountOAuthCheck from '@/components/account/oauth_check.vue'
import AccountActivation from '@/components/account/activation.vue'
import AccountPasswordReset from '@/components/account/password_reset.vue'
import AccountPasswordResetRequest from '@/components/account/password_reset_req.vue'
import AccountFiles from '@/components/account/files.vue'

import Setting from '@/components/settings/setting.vue'
import SettingUserinfoMe from '@/components/settings/userinfo/me.vue'
import SettingUserinfoUpload from '@/components/settings/userinfo/upload.vue'
import SettingUserinfoPrivacy from '@/components/settings/userinfo/privacy.vue'
import SettingSecurityPassword from '@/components/settings/security/password.vue'
import SettingSecurityOAuth from '@/components/settings/security/oauth.vue'

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
import AdminCommonManageLog from '@/components/admin/common/manage-log.vue'

import About from '@/components/about.vue'
import NotFoundComponent from '@/components/404.vue'

Vue.use(Router)

export default new Router({
    mode: 'history',
    routes: [
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
        // 用户 - 激活
        {
            path: '/account/activation',
            name: 'account_activation',
            component: AccountActivation
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

        // 用户 - 个人文件
        {
            path: '/account/files',
            name: 'account_files',
            component: AccountFiles
        },

        // 用户 - 个人提醒
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
        // 管理 - 综合 - 评论
        {
            path: '/admin/common/log/manage/:page(\\d+)?/:name(.+)?',
            name: 'admin_common_manage_log',
            component: AdminCommonManageLog
        },

        {
            path: '*',
            component: NotFoundComponent
        },

        // 关于
        {
            path: '/about',
            name: 'about',
            component: About
        },

        // OAuth
        {
            path: '/account/oauth',
            name: 'account_oauth',
            component: AccountOAuth
        },

        // OAuth Registe Check
        {
            path: '/account/oauth_check',
            name: 'account_oauth_check',
            component: AccountOAuthCheck
        }
    ]
})
