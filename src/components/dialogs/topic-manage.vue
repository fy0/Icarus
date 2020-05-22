<template>
<ic-dialog v-model="topicManage" :title="`对文章 ${topic.title} 进行管理操作`" @close="closeOutside">
    <div v-if="stage == 1">
        <div class="manage-form-item">
            <span class="label">
                <nuxt-link :to="{ name: 'forum_topic_edit', params: {id: topic.id}, query: {manage: true} }">编辑文章</nuxt-link>
            </span>
            <div class="right">
            </div>
        </div>
        <div class="manage-form-item">
            <span class="label">置顶级别</span>
            <div class="right">
                <span style="margin-right: 10px" v-for="i in [0, 1, 2, 3, 4, 5]" :key="i">
                    <label :for="'radio-sticky-'+i">
                        <input class="ic-input" type="radio" name="sticky" :value="i" :id="'radio-sticky-'+i" v-model="vSticky" />
                        <span>{{i}}</span>
                    </label>
                </span>
            </div>
        </div>
        <div class="manage-form-item">
            <span class="label">提升下沉</span>
            <div class="right" style="display: flex; align-items: center;">
                <input class="ic-input primary" style="width:100%" v-model="vWeight" :step="1" :min="-100" :max="100" type="range" />
                <span style="min-width: 40px; text-align: center">{{vWeight}}</span>
            </div>
        </div>
        <div class="manage-form-item">
            <span class="label">文章评分</span>
            <div class="right" style="display: flex; align-items: center;">
                <input class="ic-input primary" style="width:100%" v-model="vCredit" :step="1" :min="-50" :max="50" type="range" />
                <span style="min-width: 40px; text-align: center">{{vCredit}}</span>
            </div>
        </div>
        <div class="manage-form-item">
            <span class="label">声望奖励</span>
            <div class="right" style="display: flex; align-items: center;">
                <input class="ic-input primary" style="width:100%" v-model="vRepute" :step="1" :min="-10" :max="10" type="range" />
                <span style="min-width: 40px; text-align: center">{{vRepute}}</span>
            </div>
        </div>
        <div class="manage-form-item">
            <span class="label">状态</span>
            <div class="right">
                <span style="margin-right: 10px" v-for="(i, j) in POST_STATE_TXT" :key="j">
                    <label :for="'radio-state-'+j">
                        <input class="ic-input" type="radio" name="state" :value="j" :id="'radio-state-'+j" v-model="vState" />
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
                        <input class="ic-input" type="radio" name="visible" :value="j" :id="'radio-visible-'+i" v-model="vVisible" />
                        <span>{{i}}</span>
                    </label>
                </span>
            </div>
        </div>
        <div class="manage-form-item">
            <span class="label">优秀</span>
            <div class="right">
                <ic-checkbox v-model="vAwesome" />
            </div>
        </div>
    </div>
    <div v-else>
        <span v-if="Object.keys(changed) == 0">无任何改动</span>
        <div v-else>
            <div class="manage-form-item" v-if="changed.vSticky">
                <span class="label">文章置顶</span>
                <div class="right">
                <div class="right"><span class="hl">{{changed.vSticky[0]}}</span> -> <span class="hl">{{changed.vSticky[1]}}</span></div>
                </div>
            </div>
            <div class="manage-form-item" v-if="changed.vWeight">
                <span class="label">提升下沉</span>
                <div class="right"><span class="hl">{{changed.vWeight[0]}}</span> -> <span class="hl">{{changed.vWeight[1]}}</span></div>
            </div>
            <div class="manage-form-item" v-if="changed.vCredit">
                <span class="label">文章评分</span>
                <div class="right"><span class="hl">{{changed.vCredit[1]}}</span></div>
            </div>
            <div class="manage-form-item" v-if="changed.vState">
                <span class="label">文章状态</span>
                <div class="right">
                    <span class="hl">{{POST_STATE_TXT[changed.vState[0]]}}</span>
                    <span> -> </span>
                    <span class="hl">{{POST_STATE_TXT[changed.vState[1]]}}</span>
                </div>
            </div>
            <div class="manage-form-item" v-if="changed.vVisible">
                <span class="label">文章可见性</span>
                <div class="right">
                    <span class="hl">{{POST_VISIBLE_TXT[changed.vVisible[0]]}}</span>
                    <span> -> </span>
                    <span class="hl">{{POST_VISIBLE_TXT[changed.vVisible[1]]}}</span>
                </div>
            </div>
            <div class="manage-form-item" v-if="changed.vRepute">
                <span class="label">声望奖励</span>
                <div class="right"><span class="hl">{{changed.vRepute[1]}}</span></div>
            </div>
            <div class="manage-form-item" v-if="changed.vAwesome">
                <span class="label">精华文章</span>
                <div class="right"><span class="hl">{{changed.vAwesome[0]}}</span> -> <span class="hl">{{changed.vAwesome[1]}}</span></div>
            </div>

            <div style="margin-top: 10px" v-if="stage == 3">
                <b v-if="currentApply == -1">完成</b>
                <b v-else>正在应用改动 - <span>{{currentApply+1}}</span></b>
                <ic-progress :show-percent="true" :classes="'striped animated'" :value="applyValue"/>
            </div>
        </div>
    </div>

    <div class="bottom">
        <span class="ic-btn primary" v-if="stage <= 2" @click="next">确定</span>
        <span class="ic-btn secondary" v-if="stage <= 2" @click="close">取消</span>
        <span class="ic-btn primary" v-if="stage === 4" @click="close">完成</span>
    </div>
</ic-dialog>
</template>

<style lang="scss" scoped>
.manage-form-item {
    margin-bottom: 15px;
}

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
import { mapState, mapGetters } from 'vuex'
import { retcode } from 'slim-tools'

export default {
  data () {
    return {
      save: { title: '' },
      vSticky: '0',
      vWeight: 0,
      vCredit: 0,
      vState: '0',
      vVisible: 0,
      vRepute: 0,
      vAwesome: false,
      stage: 1,
      currentApply: 0,
      applyValue: 0
    }
  },
  computed: {
    ...mapState('dialog', [
      'topicManage',
      'topicManageData'
    ]),
    ...mapGetters([
      'POST_TYPES',
      'POST_TYPES_TXT',
      'POST_STATE_TXT',
      'POST_VISIBLE_TXT'
    ]),
    topic: function () {
      // TODO: 重构此页面。
      // 看起来不合理是早期很多工具没有，又嫁接了一些后期需求导致的。
      return this.save
    },
    changed: function () {
      let change = {}
      let topic = this.save
      // 置顶
      if (parseInt(this.vSticky) !== topic.sticky_weight) {
        change.vSticky = [topic.sticky_weight, parseInt(this.vSticky)]
      }
      // 提升下沉
      if (this.vWeight !== 0) {
        change.vWeight = [0, this.vWeight]
      }
      // 积分奖励
      if (this.vCredit !== 0) {
        change.vCredit = [0, this.vCredit]
      }
      // 文章状态
      if (parseInt(this.vState) !== topic.state) {
        change.vState = [topic.state, parseInt(this.vState)]
      }
      // 文章可见性
      if (this.vVisible !== topic.visible) {
        change.vVisible = [topic.visible, this.vVisible]
      }
      // 声望奖励
      if (this.vRepute !== 0) {
        change.vRepute = [0, this.vRepute]
      }
      // 精华文章
      if (this.vAwesome !== Boolean(topic.awesome)) {
        change.vAwesome = [false, this.vAwesome]
      }
      return change
    }
  },
  methods: {
    next: async function () {
      this.stage++
      if (this.stage === 3) {
        let change = this.changed

        let i = 0
        let len = Object.keys(change).length

        let updateOne = () => {
          this.currentApply = i++
          this.applyValue = this.currentApply * 100.0 / len
        }

        // 置顶
        if (change.vSticky) {
          updateOne()
          let ret = await this.$api.topic.set({ id: this.topic.id }, { 'sticky_weight': change.vSticky[1] })
          if (ret.code === 0) this.$message.success('文章置顶设置成功')
          else this.$message.byCode(ret.code)
        }

        // 真正的提升下沉实现起来比较难，直接改变权重值吧
        if (change.vWeight) {
          updateOne()
          let ret = await this.$api.topic.set({ id: this.topic.id }, { 'weight.incr': change.vWeight[1] })
          if (ret.code === 0) this.$message.success('提升/下沉设置成功')
          else this.$message.byCode(ret.code)
        }

        // 文章状态
        if (change.vState) {
          updateOne()
          let ret = await this.$api.topic.set({ id: this.topic.id }, { state: change.vState[1] })
          if (ret.code === 0) this.$message.success('文章状态修改成功')
          else this.$message.byCode(ret.code)
        }

        // 文章可见性
        if (change.vVisible) {
          updateOne()
          let ret = await this.$api.topic.set({ id: this.topic.id }, { visible: change.vVisible[1] })
          if (ret.code === 0) this.$message.success('文章可见性修改成功')
          else this.$message.byCode(ret.code)
        }

        // 积分奖励
        if (change.vCredit) {
          updateOne()
          let ret = await this.$api.user.set({ id: this.topic.user_id }, {
            'credit.incr': change.vCredit[1],
            '$src': JSON.stringify({
              'id': this.topic.id,
              'type': this.POST_TYPES.TOPIC
            })
          })
          if (ret.code === 0) this.$message.success('加分/扣分设置成功')
          else this.$message.byCode(ret.code)
        }

        // 声望奖励
        if (change.vRepute) {
          updateOne()
          let ret = await this.$api.user.set({ id: this.topic.user_id }, {
            'repute.incr': change.vCredit[1],
            '$src': JSON.stringify({
              'id': this.topic.id,
              'type': this.POST_TYPES.TOPIC
            })
          })
          if (ret.code === 0) this.$message.success('声望变更设置成功')
          else this.$message.byCode(ret.code)
        }

        // 优秀文章
        if (change.vAwesome) {
          updateOne()
          let ret = await this.$api.topic.set({ id: this.topic.id }, { awesome: change.vAwesome[1] ? 1 : 0 })
          if (ret.code === 0) this.$message.success('优秀文章设置成功')
          else this.$message.byCode(ret.code)
        }

        // done
        this.currentApply = -1
        this.applyValue = 100
        this.stage = 4
      }
    },
    closeOutside () {
      if (this.stage === 1) this.close()
    },
    close () {
      if (this.stage === 2) this.stage = 1
      else this.$store.commit('dialog/SET_TOPIC_MANAGE', { val: false })
      if (this.stage === 4) {
        this.$router.go(0)
      }
    }
  },
  watch: {
    'topicManage': async function (val) {
      if (val) {
        let info = await this.$api.topic.get({
          id: this.topicManageData.id
        })

        if (info.code === retcode.SUCCESS) {
          this.save = info.data
          let topic = info.data
          this.vSticky = topic.sticky_weight
          this.vState = topic.state
          this.vVisible = topic.visible
          this.vAwesome = Boolean(topic.awesome)
          this.stage = 1
        } else {
          this.$message.byCode(info.code, info)
        }
      }
    }
  }
}
</script>
