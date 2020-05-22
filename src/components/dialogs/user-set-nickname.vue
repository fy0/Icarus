<template>
<ic-dialog v-if="$user.data" :width="'360px'" v-model="userSetNickname" :title="`修改用户昵称`" scrollable>
    <div>
        <form class="ic-form">
            <check-row>
                <label for="nickname">当前昵称</label>
                <div>{{$user.data.nickname}}</div>
            </check-row>
            <check-row :results="formErrors.nickname" :check="(!info.nickname) || checkNicknameOK" :text="'至少两个汉字，或以汉字/英文字符开头至少4个字符'">
                <label for="nickname">新昵称</label>
                <input class="ic-input" type="text" name="nickname" id="nickname" v-model="info.nickname">
            </check-row>
        </form>
    </div>
    <div class="bottom">
        <span class="ic-btn primary" @click="ok">确定</span>
        <span class="ic-btn secondary" @click="cancel">取消</span>
    </div>
</ic-dialog>
</template>

<style lang="scss" scoped>
.ic-form {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    margin-bottom: 20px;
    margin-top: -20px;
}

.ic-form-row > * {
    width: 100%;
}

.ic-form-row {
    width: 100%;
    padding-top: 10px;
    padding-bottom: 10px;
}

.bottom {
    text-align: center;

    .ic-btn {
        padding-left: 30px;
        padding-right: 30px;
        margin-left: 10px;
    }
}
</style>

<script>
import { mapState } from 'vuex'
import { retcode } from 'slim-tools'
import { checkNickname } from '@/utils/user'

export default {
  data () {
    return {
      formErrors: {
        nickname: []
      },
      info: {
        nickname: ''
      },
      sending: false
    }
  },
  computed: {
    ...mapState('dialog', [
      'userSetNickname'
    ])
  },
  methods: {
    ok: async function () {
      if (await this.changeNickname()) {
        this.$dialogs.setUserNickname(false)
      }
    },
    cancel: async function () {
      this.$dialogs.setUserNickname(false)
    },
    checkNicknameOK: function () {
      return checkNickname(this.info.nickname)
    },
    changeNickname: async function () {
      if (this.sending) return
      this.sending = true

      let ret = await this.$api.user.changeNickname(this.info.nickname)
      if (ret.code === retcode.SUCCESS) {
        this.$message.success('修改成功！')
        let newData = Object.assign({}, this.$user.data)
        newData.nickname = ret.data.nickname
        newData.change_nickname_chance = ret.data.change_nickname_chance
        newData.is_new_user = false
        this.$store.commit('user/SET_USER_DATA', newData)
        this.sending = false
        return true
      } else if (ret.code === retcode.INVALID_POSTDATA) {
        this.formErrors = ret.data
      }
      this.sending = false
    }
  }
}
</script>
