// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import nprogress from 'nprogress/nprogress.js'

import 'lodash'
import 'normalize.css'
import 'animate.css'
import 'nprogress/nprogress.css'

import './assets/css/base.css'
import './assets/css/button.css'
import './assets/css/am-alert.css'
import './tools.js'

import './components/utils/msgbox.vue'
import state from './state.js'
import api from './netapi.js'
// import config from './config.js'

Vue.config.productionTip = false
nprogress.configure({showSpinner: false})

router.beforeEach(async function (to, from, next) {
    nprogress.start()

    if (!state.misc) {
        let ret = await api.misc()
        if (ret.code === 0) {
            Vue.set(state, 'misc', ret.data)
            api.retcode = ret.data.retcode
            api.retinfo = ret.data.retinfo_cn
        }

        /* ret = await api.userInfo()
        if (ret.code === 0) {
            Vue.set(state, 'user', ret.data)
        } */
    }
    next()
})

router.afterEach(async function (to, from, next) {
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
