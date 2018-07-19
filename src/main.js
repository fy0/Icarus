// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
/* eslint-disable import/first */

import Vue from 'vue'
import App from './app'
import router from './router'
import nprogress from 'nprogress/nprogress.js'

import 'animate.css'
import 'font-awesome/css/font-awesome.css'
import 'lodash'
import 'qiniu-js'
import 'nprogress/nprogress.css'
// muse-ui 包含 normalize.css
import MuseUI from 'muse-ui'
import 'muse-ui/dist/muse-ui.css'

// social share
import 'social-share.js/dist/js/social-share.min.js'
import 'social-share.js/dist/css/share.min.css'

Vue.use(MuseUI)

import 'vue-loaders/dist/vue-loaders.css'
import * as VueLoaders from 'vue-loaders'
Vue.use(VueLoaders)

import './assets/css/base-ui.scss'
import './md.js'
import './tools.js'

import state from './state.js'
import api from './netapi.js'
import ws from './ws.js'
// import config from './config.js'

import PageNotFound from './components/404.vue'
import Redirecting from './components/utils/redirecting.vue'
import Paginator from './components/utils/paginator.vue'
import Loading from './components/utils/loading.vue'
import Avatar from './components/utils/avatar.vue'
import ICTime from './components/utils/ic-time.vue'
import UserLink from './components/utils/user-link.vue'
import PostLink from './components/utils/post-link.vue'
import ICDialog from './components/utils/dialogs/_dialog.vue'
// import MsgBox from './components/utils/msgbox.vue'

import DialogTopicManage from './components/utils/dialogs/topic-manage.vue'
import DialogUserManage from './components/utils/dialogs/user-manage.vue'
import DialogCommentManage from './components/utils/dialogs/comment-manage.vue'
import DialogUserSetAvatar from './components/utils/dialogs/user-set-avatar.vue'

Vue.component('page-not-found', PageNotFound)
Vue.component('redirecting', Redirecting)
Vue.component('paginator', Paginator)
Vue.component('loading', Loading)
Vue.component('avatar', Avatar)
Vue.component('ic-time', ICTime)
Vue.component('user-link', UserLink)
Vue.component('post-link', PostLink)
Vue.component('ic-dialog', ICDialog)
Vue.component('dialog-topic-manage', DialogTopicManage)
Vue.component('dialog-user-manage', DialogUserManage)
Vue.component('dialog-comment-manage', DialogCommentManage)
Vue.component('dialog-user-set-avatar', DialogUserSetAvatar)

Vue.directive('title', {
    inserted: function (el, binding) {
        document.title = el.innerText
        el.remove()
    }
})

Vue.config.productionTip = false
nprogress.configure({showSpinner: false})

ws.conn.callback['notif.refresh'] = (data) => {
    if (data) {
        $.message_text(`收到 ${data} 条新提醒，请点击右上角提醒按钮查看！`)
        Vue.set(state, 'unread', data)
    }
}

ws.conn.callback['user.online'] = (data) => {
    Vue.set(state, 'userOnline', data)
}

router.beforeEach(async function (to, from, next) {
    let toUrl = null
    state.loading = 1
    nprogress.start()
    $.tpClear()

    // 重置对话框
    state.dialog.topicManage = null

    if (state.misc === undefined) {
        let ret = await api.misc()
        if (ret.code === 0) {
            Vue.set(state, 'misc', ret.data)
            api.retcode = ret.data.retcode
            api.retinfo = ret.data.retinfo_cn
        }

        if (!state.user) {
            let ret = await api.user.getUserId()
            if (ret.code !== api.retcode.SUCCESS) {
                // 未登录，后续不必进行
                Vue.set(state, 'initLoadDone', true)
            } else {
                ret = await api.user.get({id: ret.data.id}, 'inactive_user')
                if (ret.code !== api.retcode.SUCCESS) {
                    // 执行未成功
                    state.loading = 0
                    nprogress.done()
                    Vue.set(state, 'initLoadDone', true)
                    $.message_error('获取用户信息失败，可能是网络问题或者服务器无响应')
                    toUrl = '/'
                } else {
                    if (state.misc.extra.daily_reward) {
                        $.message_success(`每日登陆，获得积分 ${state.misc.extra.daily_reward['credit']} 点`, 5000)
                    }

                    Vue.set(state, 'user', ret.data)
                    Vue.set(state, 'initLoadDone', true)
                    $.notifLoopOn()
                }
            }
        }
    }

    if (!state.user) {
        if (to.name === 'setting') {
            state.loading = 0
            nprogress.done()
            toUrl = '/'
        }
    } else {
        if (to.name === 'account_signin' || to.name === 'account_signup') {
            state.loading = 0
            nprogress.done()
            toUrl = '/'
        }
    }

    if (to.name) {
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

/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    template: '<App/>',
    components: { App }
})
