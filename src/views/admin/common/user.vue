<template>
  <admin-base>
    <h3 class="ic-header">用户管理</h3>

    <div class="search-box">
        <input type="text" class="ic-input" v-model.trim="searchTxt" @keyup.enter="doSearch()" placeholder="搜索 用户名/uid/邮箱" />
        <span @click="doSearch()" class="ic-btn primary search-btn">搜索</span>
    </div>
    <div>
        <ul class="ic-collection" v-if="page.items">
            <li class="item ic-collection-item" v-for="i in page.items" :key="i.id">
                <avatar :user="i" class="avatar" />
                <div class="right">
                    <user-link :user="i" />
                    <div class="info">
                        <span>注册于 <ic-time :ago="false" :timestamp="i.time" /></span> ·
                        <span>{{$misc.USER_GROUP_TXT[i.group]}}</span> ·
                        <span>{{$misc.POST_STATE_TXT[i.state]}}</span> ·
                        <i class="ic-topic-manage-icon icarus icon-39" title="管理" @click="$dialogs.setUserManage(true, i)"></i>
                    </div>
                    <div>
                        <a @click="userPasswordReset(i)" href="javascript:void(0);" style="margin-right: 10px;">密码重置</a>
                        <a @click="userKeyReset(i)" href="javascript:void(0);">会话重置</a>
                    </div>
                </div>
            </li>
        </ul>
        <div v-else>未找到结果</div>
    </div>
    <paginator :page-info='page' :route-name='"admin_common_user"' />
  </admin-base>
</template>

<style scoped>
.item {
  display: flex;
}

.item > .right {
  padding-left: 10px;
}

.search-box {
  flex: 1;
  align-items: center;
  display: flex;
}

.search-box > input {
  width: 40%;
  border-radius: 2px;
  border: 1px solid #ddd;
  box-sizing: border-box;
}

.search-box > .search-btn {
  margin-left: 10px;
}
</style>

<script>
import swal from 'sweetalert2'
import { retcode } from 'slim-tools'
import AdminBase from '../base/base.vue'
import { regex } from '@/utils/misc'

export default {
  data () {
    return {
      searchTxt: '',
      page: {}
    }
  },
  head () {
    return {
      title: '用户管理 - 管理界面',
      meta: [
        { hid: 'description', name: 'description', content: '用户管理 - 管理界面' }
      ]
    }
  },
  methods: {
    doSearch: async function () {
      let found = false
      let role = this.$user.mainRole

      if (regex.email.test(this.searchTxt)) {
        let retList = await this.$api.user.list({ email: this.searchTxt, order: 'id.desc' }, 1, { role })
        if (retList.code === retcode.SUCCESS) {
          this.page = retList.data
          found = true
        }
      } else {
        if (regex.nickname.test(this.searchTxt)) {
          let retList = await this.$api.user.list({ nickname: this.searchTxt, order: 'id.desc' }, 1, { role })
          if (retList.code === retcode.SUCCESS) {
            this.page = retList.data
            found = true
          }
        }
        if (regex.id.test(this.searchTxt)) {
          let retList = await this.$api.user.list({ id: this.searchTxt, order: 'id.desc' }, 1, { role })
          if (retList.code === retcode.SUCCESS) {
            if (found) {
              this.page.items.push(retList.data.items[0])
            } else {
              this.page = retList.data
            }
            found = true
          }
        }
      }
      if (!found) {
        this.page = {}
      }
    },
    userPasswordReset: function (user) {
      swal({
        title: '重要：密码重置操作',
        text: '请输入一个新的密码',
        input: 'text',
        showCancelButton: true,
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        showLoaderOnConfirm: true,
        preConfirm: async (password) => {
          if (password === '') {
            swal.showValidationError('密码不能为空。')
          }
          return this.$api.user.set({ id: user.id }, { password: await $.passwordHash(password) })
        }
      }).then((result) => {
        if (result.value == null) return
        if (result.value.code === retcode.SUCCESS) {
          swal({
            title: '操作成功！',
            type: 'success'
          })
        } else {
          swal({
            type: 'error',
            title: '出错了',
            text: result.value.data
          })
        }
      })
    },
    userKeyReset: function (user) {
      swal({
        title: '重要：重置用户会话',
        text: '重置之后，用户的自动登录将会失效，当前登陆的用户会自动登出',
        type: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#DD6B55',
        cancelButtonText: '取消',
        confirmButtonText: '确定，我要重置',
        showLoaderOnConfirm: true,
        preConfirm: async () => {
          return this.$api.user.set({ id: user.id }, { 'key': '1' })
        }
      }).then((result) => {
        if (result.value == null) return
        if (result.value.code === retcode.SUCCESS) {
          swal({
            title: '如你所愿',
            text: '',
            type: 'success'
          })
        } else {
          swal({
            type: 'error',
            title: '出错了',
            text: result.value.data
          })
        }
      })
    },
    fetchData: async function () {
      let params = this.$route.params
      let retList = await this.$api.user.list({
        order: 'id.desc'
      }, params.page)
      if (retList.code === retcode.SUCCESS) {
        this.page = retList.data
      }
    }
  },
  created: async function () {
    this.$store.commit('LOADING_INC', 1)
    await this.fetchData()
    this.$store.commit('LOADING_DEC', 1)
  },
  watch: {
    // 如果路由有变化，会再次执行该方法
    '$route': 'fetchData'
  },
  components: {
    AdminBase
  }
}
</script>
