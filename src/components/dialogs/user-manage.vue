<template>
<ic-dialog v-model="userManage" :title="`对用户 ${user.nickname} 进行管理操作`" @close="close" scrollable>
    <div class="manage-form-item" style="margin-top: 30px;">
        <span class="label">ID</span>
        <div class="right">{{user.id}}</div>
    </div>
    <div class="manage-form-item">
        <span class="label">Email</span>
        <div class="right">
            <div>{{user.email}}</div>
        </div>
    </div>
    <div class="manage-form-item">
        <span class="label">昵称</span>
        <div class="right">
            <div>{{user.nickname}}</div>
        </div>
    </div>
    <div class="manage-form-item">
        <span class="label">注册时间</span>
        <div class="right">
            <ic-time :ago="false" :timestamp="user.time" />
        </div>
    </div>
    <div class="manage-form-item">
        <span class="label">最后登录时间</span>
        <div class="right">
            <ic-time :ago="false" :timestamp="user.key_time" />
        </div>
    </div>
    <div class="manage-form-item">
        <span class="label">最后访问时间</span>
        <div class="right">
            <ic-time :ago="false" :timestamp="user.access_time" />
        </div>
    </div>
    <div class="manage-form-item">
        <span class="label">简介</span>
        <div class="right">
            <input type="text" class="ic-input" v-model="user.biology" />
        </div>
    </div>
    <div class="manage-form-item">
        <span class="label">附加权限</span>
        <div class="right">
            <ic-checkbox v-model="user.is_wiki_editor">百科编辑</ic-checkbox>
        </div>
    </div>
    <div class="manage-form-item" style="align-items: center">
        <span class="label">状态</span>
        <div class="right" style="display: flex">
            <span style="margin-right: 10px" v-for="(i, j) in POST_STATE_TXT" :key="j">
                <label :for="'radio-state-'+i">
                    <input class="ic-input" type="radio" name="state" :value="j" :id="'radio-state-'+i" v-model="user.state" />
                    <span>{{i}}</span>
                </label>
            </span>
        </div>
    </div>
    <div class="manage-form-item" style="align-items: center">
        <span class="label">用户组</span>
        <div class="right" style="display: flex">
            <span style="margin-right: 10px" v-for="(i, j) in USER_GROUP_TXT" :key="j">
                <label :for="'radio-group-'+i">
                    <input class="ic-input" type="radio" name="group" :value="j" :id="'radio-group-'+i" v-model="user.group" />
                    <span>{{i}}</span>
                </label>
            </span>
        </div>
    </div>

    <div class="bottom">
        <span class="ic-btn primary" @click="ok">确定</span>
        <span class="ic-btn secondary" @click="close">取消</span>
    </div>
</ic-dialog>
</template>

<style lang="scss" scoped>
.bottom {
    text-align: right;

    .ic-btn {
        padding-left: 30px;
        padding-right: 30px;
        margin-left: 10px;
    }
}
</style>

<script>
import { retcode } from 'slim-tools'
import { mapState, mapGetters } from 'vuex'

export default {
  data () {
    return {
      user: { name: '' },
      save: {}
    }
  },
  computed: {
    ...mapState('dialog', [
      'userManage',
      'userManageData'
    ]),
    ...mapGetters([
      'USER_GROUP_TXT',
      'POST_STATE_TXT'
    ])
  },
  methods: {
    ok: async function () {
      let data = $.objDiff(this.user, this.save)
      if (data.state) data.state = Number(data.state)
      if (data.group) data.group = Number(data.group)

      let ret = await this.$api.user.set({ id: this.user.id }, data)
      if (ret.code === 0) {
        this.$store.commit('dialog/WRITE_USER_MANAGE_DATA', data)
        this.$message.success('用户信息设置成功')
      } else this.$message.byCode(ret.code)

      this.$dialogs.setUserManage(false)
    },
    close () {
      this.$dialogs.setUserManage(false)
    }
  },
  watch: {
    'userManage': async function (val) {
      if (val) {
        let info = await this.$api.user.get({ id: this.userManageData.id })
        if (info.code === retcode.SUCCESS) {
          this.user = info.data
          this.user.state = this.user.state.toString()
          this.user.group = this.user.group.toString()
          this.save = _.clone(this.user)
        } else {
          this.$message.byCode(info.code)
        }
      }
    }
  }
}
</script>
