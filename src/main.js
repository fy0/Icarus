// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import nprogress from 'nprogress/nprogress.js'

import 'normalize.css'
import 'animate.css'
import 'nprogress/nprogress.css'

import './assets/css/base.css'
import './assets/css/button.css'
import './tools.js'

Vue.config.productionTip = false

router.beforeEach(async function (to, from, next) {
    nprogress.start()

    /*
    if (!state.data.misc) {
        let ret = await api.misc()
        Vue.set(state.data, 'misc', ret.data)

        ret = await api.userInfo()
        if (ret.code === 0) {
            Vue.set(state.data, 'user', ret.data)
        }
    }
    */
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
