// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './app'
import router from './router'
import nprogress from 'nprogress/nprogress.js'

import 'animate.css'
import 'font-awesome/css/font-awesome.css'
import 'lodash'
import 'nprogress/nprogress.css'
// muse-ui 包含 normalize.css
import MuseUI from 'muse-ui'
import 'muse-ui/dist/muse-ui.css'
import './ws.js'
Vue.use(MuseUI)

import marked from 'marked'
import Prism from 'prismjs'
import 'prismjs/themes/prism-tomorrow.css'

import 'prismjs/components/prism-autohotkey.js'
import 'prismjs/components/prism-bash.js'
import 'prismjs/components/prism-batch.js'
import 'prismjs/components/prism-c.js'
import 'prismjs/components/prism-clike.js'
import 'prismjs/components/prism-cpp.js'
import 'prismjs/components/prism-csharp.js'
import 'prismjs/components/prism-css.js'
import 'prismjs/components/prism-css-extras.js'
import 'prismjs/components/prism-git.js'
import 'prismjs/components/prism-glsl.js'
import 'prismjs/components/prism-go.js'
import 'prismjs/components/prism-ini.js'
import 'prismjs/components/prism-java.js'
import 'prismjs/components/prism-javascript.js'
import 'prismjs/components/prism-json.js'
import 'prismjs/components/prism-lua.js'
import 'prismjs/components/prism-markdown.js'
import 'prismjs/components/prism-python.js'
import 'prismjs/components/prism-sql.js'
import 'prismjs/components/prism-nginx.js'

let renderer = new marked.Renderer()

renderer.code = function (code, lang, escaped) {
    if (this.options.highlight) {
        var out = this.options.highlight(code, lang)
        // 这里存在问题，对部分简单代码来说 out == code 是完全可能的
        // 但是 escape 之后代价就是例如空格转换成%20，用户看来是成了乱码
        // if (out != null && out !== code) {
        if (out != null) {
            escaped = true
            code = out
        }
    }

    if (!lang) {
        return `<pre class="${this.options.langPrefix}PLACEHOLDER"><code>` +
            // + (escaped ? code : escape(code, true))
            code + '\n</code></pre>'
    }

    let langText = this.options.langPrefix + escape(lang, true)
    return `<pre class="${langText}"><code class="${langText}">` +
        (escaped ? code : escape(code, true)) +
        '\n</code></pre>\n'
}

marked.setOptions({
    renderer: renderer,
    gfm: true,
    breaks: true,
    sanitize: true,
    langPrefix: 'language-',
    highlight: function (code, lang) {
        if (lang) {
            let stdlang = lang.toLowerCase()
            if (Prism.languages[stdlang]) {
                return Prism.highlight(code, Prism.languages[stdlang])
            }
        }
    }
})

import './assets/css/base.css'
import './assets/css/button.css'
import './assets/css/form.css'
import './assets/css/am-alert.css'
import './tools.js'

import state from './state.js'
import api from './netapi.js'
// import config from './config.js'

import Paginator from './components/utils/paginator.vue'
import Loading from './components/utils/loading.vue'
import Avatar from './components/utils/avatar.vue'
import ICTime from './components/utils/ic-time.vue'
import UserLink from './components/utils/user-link.vue'
// import MsgBox from './components/utils/msgbox.vue'

Vue.component('paginator', Paginator)
Vue.component('loading', Loading)
Vue.component('avatar', Avatar)
Vue.component('ic-time', ICTime)
Vue.component('user-link', UserLink)

Vue.config.productionTip = false
nprogress.configure({showSpinner: false})

router.beforeEach(async function (to, from, next) {
    state.loading = 1
    nprogress.start()
    $.tpClear()

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
                return next()
            }

            ret = await api.user.get({id: ret.data.id}, 'user')
            if (ret.code !== api.retcode.SUCCESS) {
                // 执行未成功
                Vue.set(state, 'initLoadDone', true)
                return next('/')
            }

            let unread = await api.notif.count()
            if (unread.code === api.retcode.SUCCESS) {
                Vue.set(state, 'unread', unread.data)
            }

            Vue.set(state, 'user', ret.data)
            Vue.set(state, 'initLoadDone', true)
        }
    }

    next()
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
