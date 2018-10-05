/* eslint-disable import/first */

import Vue from 'vue'
import App from './app'
import router from './router'
import nprogress from 'nprogress/nprogress.js'

import 'normalize.css'
import 'qiniu-js'
import 'animate.css'
import 'nprogress/nprogress.css'
import 'font-awesome/css/font-awesome.css'

Vue.config.productionTip = false

import 'vue-loaders/dist/vue-loaders.css'
import * as VueLoaders from 'vue-loaders'
Vue.use(VueLoaders)

// social share
import 'social-share.js/dist/js/social-share.min.js'
import 'social-share.js/dist/css/share.min.css'

import './assets/css/base-ui.scss'
import './assets/icons/iconfont.css'
import './md.js'

import state from './state.js'
import api from './netapi.js'
import ws from './ws.js'
import config from './config.js'

import PageNotFound from './components/404.vue'
import Redirecting from './components/misc/redirecting.vue'
import UserLink from './components/misc/user-link.vue'
import PostLink from './components/misc/post-link.vue'
import ICDialog from './components/dialogs/_dialog.vue'

import Loading from './components/ui/loading.vue'
import Avatar from './components/ui/avatar.vue'
import Paginator from './components/ui/paginator.vue'
import ICTime from './components/ui/ic-time.vue'
import CheckRow from './components/ui/checkrow.vue'
import Timeline from './components/ui/timeline.vue'
import TimelineItem from './components/ui/timeline-item.vue'
import Tab from './components/ui/tab.vue'
import Tabs from './components/ui/tabs.vue'
import Progress from './components/ui/progress.vue'
import Badge from './components/ui/badge.vue'
import GoTop from './components/ui/gotop.vue'
// import MsgBox from './components/msgbox.vue'

import DialogTopicManage from './components/dialogs/topic-manage.vue'
import DialogUserManage from './components/dialogs/user-manage.vue'
import DialogCommentManage from './components/dialogs/comment-manage.vue'
import DialogUserSetAvatar from './components/dialogs/user-set-avatar.vue'

Vue.component('page-not-found', PageNotFound)
Vue.component('redirecting', Redirecting)
Vue.component('user-link', UserLink)
Vue.component('post-link', PostLink)

Vue.component('paginator', Paginator)
Vue.component('loading', Loading)
Vue.component('avatar', Avatar)
Vue.component('ic-time', ICTime)
Vue.component('check-row', CheckRow)
Vue.component('ic-timeline', Timeline)
Vue.component('ic-timeline-item', TimelineItem)
Vue.component('ic-tab', Tab)
Vue.component('ic-tabs', Tabs)
Vue.component('ic-progress', Progress)
Vue.component('ic-badge', Badge)
Vue.component('ic-gotop', GoTop)

Vue.component('ic-dialog', ICDialog)
Vue.component('dialog-topic-manage', DialogTopicManage)
Vue.component('dialog-user-manage', DialogUserManage)
Vue.component('dialog-comment-manage', DialogCommentManage)
Vue.component('dialog-user-set-avatar', DialogUserSetAvatar)

Vue.directive('title', {
    inserted: function (el, binding) {
        document.title = el.innerText
        el.remove()
    },
    update: function (el, binding) {
        document.title = el.innerText
        el.remove()
    }
})

nprogress.configure({ showSpinner: false })

if (config.ws.enable) {
    ws.conn.callback['notif.refresh'] = (data) => {
        if (data) {
            if (!state.unreadAlerted) {
                // $.message_text(`收到 ${data} 条新提醒，请点击右上角提醒按钮查看！`)
                state.unreadAlerted = true
            }
            Vue.set(state, 'unread', data)
        }
    }

    ws.conn.callback['user.online'] = (data) => {
        Vue.set(state, 'userOnline', data)
    }
}

router.beforeEach(async function (to, from, next) {
    let toUrl = null
    state.loading = 1
    nprogress.start()

    // 重置对话框
    state.dialog.topicManage = null

    if (state.misc === undefined) {
        let ret = null

        // 获取 misc 信息
        while (true) {
            try {
                ret = await api.misc()
                break
            } catch (e) {
                // 连接失败，重试
                await $.timeout(3000)
            }
        }
        if (ret.code === 0) {
            Vue.set(state, 'misc', ret.data)
            api.retcode = ret.data.retcode
            api.retinfo = ret.data.retinfo_cn
        }

        // 若用户已登录，做一些额外处理
        if (!state.user) {
            let ret = await api.user.getUserId()
            if (ret.code !== api.retcode.SUCCESS) {
                // 未登录，后续不必进行
                Vue.set(state, 'initLoadDone', true)
            } else {
                ret = await api.user.get({ id: ret.data.id }, 'inactive_user')
                if (ret.code !== api.retcode.SUCCESS) {
                    // 执行未成功
                    state.loading = 0
                    nprogress.done()
                    Vue.set(state, 'initLoadDone', true)
                    $.message_error('获取用户信息失败，可能是网络问题或者服务器无响应')
                    toUrl = '/'
                } else {
                    if (state.misc.extra.daily_reward) {
                        $.message_success(`每日登陆，获得经验 ${state.misc.extra.daily_reward['exp']} 点`, 5000)
                        ret.data.exp += state.misc.extra.daily_reward['exp']
                    }

                    Vue.set(state, 'user', ret.data)
                    Vue.set(state, 'initLoadDone', true)
                }
            }
        }

        // 开启周期数据
        $.tickStart()
    }

    if (to.name) {
        if (!state.user) {
            if (to.name.startsWith('setting_')) {
                state.loading = 0
                nprogress.done()
                toUrl = '/404'
            } else if (to.name === 'account_notif') {
                state.loading = 0
                nprogress.done()
                toUrl = '/404'
            }
        } else {
            if (to.name === 'account_signin' || to.name === 'account_signup') {
                state.loading = 0
                nprogress.done()
                toUrl = '/'
            }
        }

        if (to.name.startsWith('admin_')) {
            if (!(state.user && state.misc && state.user.group >= state.misc.USER_GROUP.SUPERUSER)) {
                state.loading = 0
                nprogress.done()
                $.message_error('当前账户没有权限访问此页面')
                toUrl = '/'
            }
        }
    }

    return (toUrl) ? next(toUrl) : next()
})

router.afterEach(async function (to, from, next) {
    state.loading--
    nprogress.done()
    // ga('set', 'page', location.pathname + location.hash)
    // ga('send', 'pageview')
})

new Vue({
    router,
    render: h => h(App)
}).$mount('#app')
