/* eslint-disable import/first */
/* eslint-disable import/no-duplicates */

import Vue from 'vue'

import 'normalize.css'
import 'qiniu-js'
import 'animate.css'

// 加载动画组件
import 'vue-loaders/dist/vue-loaders.css'
import * as VueLoaders from 'vue-loaders'
Vue.use(VueLoaders)

// import responsive from 'vue-responsive'
// Vue.use(responsive)

import '@/assets/css/base-ui.scss'
import '@/assets/icons/iconfont.css'
import '@/assets/css/_text.scss'
import '@/utils/md.ts'

// import ws from '@/ws.js'
// import store from '@/store/index.js'

import PageNotFound from '@/components/404.vue'
import Redirecting from '@/components/misc/redirecting.vue'
import UserLink from '@/components/misc/user-link.vue'
import PostLink from '@/components/misc/post-link.vue'
import ICDialog from '@/components/dialogs/_dialog.vue'

import Loading from '@/components/ui/loading.vue'
import Avatar from '@/components/ui/avatar.vue'
import Paginator from '@/components/ui/paginator.vue'
import ICTime from '@/components/ui/ic-time.vue'
import CheckRow from '@/components/ui/checkrow.vue'
import Timeline from '@/components/ui/timeline.vue'
import TimelineItem from '@/components/ui/timeline-item.vue'
import Tab from '@/components/ui/tab.vue'
import Tabs from '@/components/ui/tabs.vue'
import Progress from '@/components/ui/progress.vue'
import Badge from '@/components/ui/badge.vue'
import GoTop from '@/components/ui/gotop.vue'
import HangBtn from '@/components/ui/hangbtn.vue'
import CheckBox from '@/components/ui/checkbox.vue'
// import MsgBox from '@/components/msgbox.vue'

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
Vue.component('ic-hangbtn', HangBtn)
Vue.component('ic-checkbox', CheckBox)

import DialogTopicManage from '@/components/dialogs/topic-manage.vue'
import DialogUserManage from '@/components/dialogs/user-manage.vue'
import DialogCommentManage from '@/components/dialogs/comment-manage.vue'
import DialogSiteNew from '@/components/dialogs/site-new.vue'
import DialogUserSetAvatar from '@/components/dialogs/user-set-avatar.vue'
import DialogUserInactiveWarn from '@/components/dialogs/user-inactive-warn.vue'
import DialogUserSetNickname from '@/components/dialogs/user-set-nickname.vue'
import DialogUserSignout from '@/components/dialogs/user-signout.vue'

Vue.component('ic-dialog', ICDialog)
Vue.component('dialog-topic-manage', DialogTopicManage)
Vue.component('dialog-user-manage', DialogUserManage)
Vue.component('dialog-comment-manage', DialogCommentManage)
Vue.component('dialog-site-new', DialogSiteNew)
Vue.component('dialog-user-set-avatar', DialogUserSetAvatar)
Vue.component('dialog-user-inactive-warn', DialogUserInactiveWarn)
Vue.component('dialog-user-set-nickname', DialogUserSetNickname)
Vue.component('dialog-user-signout', DialogUserSignout)

// if (config.ws.enable) {
//     ws.conn.callback['notif.refresh'] = (data) => {
//         if (data) {
//             if (!state.unreadAlerted) {
//                 // this.$message.text(`收到 ${data} 条新提醒，请点击右上角提醒按钮查看！`)
//                 state.unreadAlerted = true
//             }
//             Vue.set(state, 'unread', data)
//         }
//     }

//     ws.conn.callback['user.online'] = (data) => {
//         Vue.set(state, 'userOnline', data)
//     }
// }
