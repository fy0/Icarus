<template>
  <ic-dialog :width="'70%'" v-model="boardManage" :title="`对板块 ${board.name} 进行管理操作`" @close="close" scrollable>
    <div class="wrapper ic-form">
        <div class="manage-form-item" style="margin-top: 0px;">
            <span class="label">ID</span>
            <div class="right">{{board.id}}</div>
        </div>
        <div class="manage-form-item">
            <span class="label">创建者</span>
            <div class="right">
                <user-link v-if="board.user_id" :user="board.user_id" />
                <div v-else>系统</div>
            </div>
        </div>
        <div class="manage-form-item">
            <span class="label">板块名</span>
            <div class="right">
                <input class="ic-input" type="text" v-model="board.name">
            </div>
        </div>
        <div class="manage-form-item">
            <span class="label">简介</span>
            <div class="right">
                <input class="ic-input" type="text" v-model="board.brief">
            </div>
        </div>
        <div class="manage-form-item">
            <span class="label">权重</span>
            <div class="right">
                <input class="ic-input" type="number" v-model="board.weight">
            </div>
        </div>
        <div class="manage-form-item">
            <span class="label">色彩</span>
            <div class="right">
                <input class="ic-input" type="text" placeholder="需为十六进制颜色，不要带#" v-model="board.color">
            </div>
        </div>
        <div class="manage-form-item" style="align-items: center">
            <span class="label">上级板块</span>
            <div class="right">
                <multiselect v-model="board.parent_id" :allow-empty="true" :options="boardList" :custom-label="getSelectOptionName" placeholder="选择一个板块" style="z-index: 2; width: 70%;" open-direction="bottom"></multiselect>
            </div>
        </div>
        <div class="manage-form-item" style="align-items: center">
            <span class="label">状态</span>
            <div class="right" style="display: flex">
                <span style="margin-right: 10px" v-for="(i, j) in POST_STATE_TXT" :key="j">
                    <label :for="'radio-state-'+i">
                        <input class="ic-input" type="radio" name="state" :value="j" :id="'radio-state-'+i" v-model="board.state" />
                        <span>{{i}}</span>
                    </label>
                </span>
            </div>
        </div>
        <div class="manage-form-item" style="align-items: center">
            <span class="label">可见性</span>
            <div class="right">
                <span style="margin-right: 10px" v-for="(i, j) in POST_VISIBLE_TXT" :key="j">
                    <label :for="'radio-visible-'+i">
                        <input class="ic-input" type="radio" name="visible" :value="j" :id="'radio-visible-'+i" v-model="board.visible" />
                        <span>{{i}}</span>
                    </label>
                </span>
            </div>
        </div>
        <div class="manage-form-item" style="align-items: center">
            <span class="label">发帖权限</span>
            <div class="right">
                <span style="margin-right: 10px">
                    <label :for="'radio-can_post_rank-0'">
                        <input class="ic-input" type="radio" name="can-post-rank" :value="0" :id="'radio-can_post_rank-0'" v-model="board.can_post_rank" />
                        <span>普通用户</span>
                    </label>
                </span>
                <span style="margin-right: 10px">
                    <label :for="'radio-can_post_rank-100'">
                        <input class="ic-input" type="radio" name="can-post-rank" :value="100" :id="'radio-can_post_rank-100'" v-model="board.can_post_rank" />
                        <span>管理</span>
                    </label>
                </span>
            </div>
        </div>
        <div class="manage-form-item" style="align-items: center">
            <span class="label">公告</span>
            <div class="right">
                <textarea class="ic-input" rows="3" v-model="board.desc" />
            </div>
        </div>

        <!-- 注意，暂时解决不了底边留白问题，很尬，只好用margin顶一下 -->
        <div class="bottom manage-form-item" style="margin: 20px 0">
            <span class="label"></span>
            <div class="right">
                <span class="ic-btn primary" @click="ok">确定</span>
                <span class="ic-btn secondary" @click="close">取消</span>
            </div>
        </div>
    </div>
  </ic-dialog>
</template>

<style lang="scss" scoped>
.wrapper {
  height: 70vh;
}

.ic-input[type=text], .ic-input[type=number], textarea.ic-input {
  width: 70%;
}

.bottom {
  .ic-btn {
    padding-left: 30px;
    padding-right: 30px;
    margin-right: 10px;
  }
}
</style>

<script>
import Multiselect from 'vue-multiselect'
import { mapState, mapGetters } from 'vuex'
import 'vue-multiselect/dist/vue-multiselect.min.css'
import '@/assets/css/_manage.scss'
import { retcode } from 'slim-tools'

export default {
  data () {
    return {
      value: 1,
      save: {},
      board: { name: '' },
      boardList: [],
      boardsInfoDict: {}
    }
  },
  computed: {
    ...mapState('dialog', [
      'boardManage',
      'boardManageData'
    ]),
    ...mapGetters([
      'POST_STATE_TXT',
      'POST_VISIBLE_TXT'
    ])
  },
  methods: {
    getSelectOptionName (id) {
      if (!this.boardsInfoDict[id]) return '无'
      const { name, brief } = this.boardsInfoDict[id]
      return `${name} — [${brief}]`
    },
    handleChange (value) {
      this.value = value
    },
    ok: async function () {
      let data = $.objDiff(this.board, this.save)

      if (Object.keys(data).length === 0) {
        // 什么都没修改
        return this.quit()
      }

      // let keys = new Set(['brief', 'category', 'desc', 'name', 'state', 'weight', 'color', 'parent_id', 'visible', 'can_post_rank'])
      let ret = await this.$api.board.set({ id: this.board.id }, data)

      if (ret.code === 0) {
        if (this.boardManageData) {
          this.$store.commit('dialog/WRITE_BOARD_MANAGE_DATA', data)
        }
        // 重新载入板块数据
        await this.$store.dispatch('forum/load')
        this.$message.success('板块信息设置成功')
      } else this.$message.byCode(ret.code)

      this.quit()
    },
    quit () {
      this.$store.commit('dialog/SET_BOARD_MANAGE', { val: false })
    },
    close () {
      this.quit()
    }
  },
  watch: {
    'boardManage': async function (val) {
      if (val) {
        let info = await this.$api.board.get({
          id: this.boardManageData.id,
          loadfk: { 'user_id': null }
        })

        if (info.code === retcode.SUCCESS) {
          this.board = info.data
          this.save = _.clone(this.board)

          let ret = await this.$api.board.list({
            order: 'weight.desc,time.asc'
          }, 1)
          if (ret.code === retcode.SUCCESS) {
            // vue-select 目前不允许写 null，要再等一等
            this.boardList = []
            this.boardsInfoDict = {}
            for (let i of ret.data.items) {
              if (i.id !== this.board.id) {
                this.boardList.push(i.id)
                this.boardsInfoDict[i.id] = i
              }
            }
          }
        } else {
          this.$message.byCode(info.code)
        }
      }
    }
  },
  components: {
    Multiselect
  }
}
</script>
