<template>
<ic-dialog v-if="commentManage">
    123
</ic-dialog>
</template>

<style>
.no-left-padding {
  padding-left: 0;
  margin-left: 0;
}
</style>

<style scoped>
.topic-manage-item {
  display: flex;
  align-items: baseline;
  min-height: 56px;
}

.topic-manage-item > .label {
  flex: 1 0 0;
}

.topic-manage-item > .right {
  flex: 4 0 0;
}

.demo-radio {
  margin-right: 15px;
}

.demo-slider {
  margin-bottom: 0;
}

.hl {
  color: red
}
</style>

<script>
import Dialog from './_dialog.vue'
import { mapState, mapGetters } from 'vuex'
// import { retcode } from 'slim-tools'

export default {
  data () {
    return {
      user: { name: '' },
      save: {}
    }
  },
  computed: {
    ...mapState('dialog', [
      'commentManage',
      'commentManageData'
    ]),
    ...mapGetters([
      'POST_STATE_TXT',
      'POST_VISIBLE_TXT'
    ])
  },
  methods: {
    ok: async function () {
    },
    close () {
      this.$store.commit('dialog/SET_USER_MANAGE', { val: false })
    }
  },
  components: {
    'ic-dialog': Dialog
  },
  watch: {
    'commentManage': async function (val) {
      // if (val) {
      //     let info = await this.$api.user.get({id: state.dialog.userManageData.id}, 'admin')
      //     if (info.code === retcode.SUCCESS) {
      //         this.user = info.data
      //         this.user.state = this.user.state.toString()
      //         this.user.group = this.user.group.toString()
      //         this.save = _.clone(this.user)
      //     } else {
      //         this.$message.byCode(info.code)
      //     }
      // }
    }
  }
}
</script>
