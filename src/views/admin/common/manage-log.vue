<template>
<admin-base>
    <h3 class="ic-header">管理日志</h3>

    <div v-if="page.items.length === 0" class="no-comment">目前没有日志</div>
    <div v-else class="comment-box">
        <div v-for="i in page.items" :key="i.id" :id="i.id" class="comment">
            <avatar :system="i.user_id === null" :user="i.user_id" class="avatar"></avatar>
            <div class="info">
                <div>
                    <post-link :text-limit="20" :goto="true" :show-type="true" :type-bold="true" :type="i.related_type" :item="postsOfComments[i.related_id]"/>
                    <span>被进行了以下操作：</span>
                </div>
                <div>
                    <span style="font-weight: bolder">
                        <template>{{MOPT[i.operation]}}</template>
                        <template v-if="i.note"> - {{i.note}}</template>
                    </span>
                    <ManageLogItemDetail :item="i" />
                </div>
                <ic-time class="time" :timestamp="i.time" />
            </div>
            <div class="manager">
                <span>操作者</span>
                <b>
                    <user-link v-if="i.user_id" :user="i.user_id" />
                    <span v-else>系统</span>
                </b>
            </div>
            <div class="role">
                <span>执行身份</span>
                <template v-if="i.role">{{i.role}}</template>
                <template v-else>系统</template>
            </div>
            <div class="time1" v-html="toMonth(i.time)"></div>
        </div>
    </div>
    <paginator :page-info='page' :route-name='"admin_common_manage_log"' />
</admin-base>
</template>

<style scoped>
.state {
    margin-left: 10px;
}

.time1 {
    text-align: center;
    align-self: center;
    padding-right: 20px;
}

.manager {
    display: flex;
    flex-direction: column;
    text-align: center;
    align-self: center;
}

.role {
    display: flex;
    flex-direction: column;
    text-align: center;
    align-self: center;
    padding: 0 20px;
}

.comment-box {
    border: 1px solid #e0e0e0;
}

.comment {
    display: flex;
    flex-direction: row;
    border-bottom: 1px solid #e0e0e0;
    padding: 20px;
    justify-content: space-between;
}

.comment > .info {
    display: flex;
    flex: 1 0 0;
    flex-direction: column;
    padding: 0 20px;
}
</style>

<script>
import { retcode } from 'slim-tools'
import { marked } from '@/utils/md.ts'
import { dateFormat } from '@/utils/time'
import AdminBase from '../base/base.vue'
import ManageLogItemDetail from '@/components/misc/manage-log-item-detail.vue'

export default {
  data () {
    return {
      marked,
      page: { info: {}, items: [] },
      postsOfComments: {},
      MOP: this.$misc.MANAGE_OPERATION,
      MOPT: this.$misc.MANAGE_OPERATION_TXT
    }
  },
  head () {
    return {
      title: '管理日志 - 管理界面',
      meta: [
        { hid: 'description', name: 'description', content: '管理日志 - 管理界面' }
      ]
    }
  },
  methods: {
    toMonth: function (ts) {
      let date = new Date()
      date.setTime(ts * 1000)
      return dateFormat(date, 'MM-dd<br>hh:mm')
    },
    fetchData: async function () {
      this.$store.commit('LOADING_INC', 1)
      let params = this.$route.params
      // let ret = await this.$api.topic.get({
      //     id: params.id,
      // })
      let ret = await this.$api.logManage.list({
        loadfk: { user_id: null },
        order: 'time.desc'
      }, params.page)

      if (ret.code === retcode.SUCCESS) {
        this.postsOfComments = await $.getBasePostsByIDs(async (i) => {
          return [
            {
              'type': i.related_type,
              'id': i.related_id
            }
          ]
        }, ret.data.items, this.$user.mainRole)

        this.page = ret.data // 提示：注意次序，渲染page依赖上层内容
      }
      this.$store.commit('LOADING_DEC', 1)
    }
  },
  created: async function () {
    await this.fetchData()
  },
  watch: {
    // 如果路由有变化，会再次执行该方法
    '$route': 'fetchData'
  },
  components: {
    AdminBase,
    ManageLogItemDetail
  }
}
</script>
