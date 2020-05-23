<template>
  <div class="ic-container">
    <h3 class="ic-header-no-line">用户提醒</h3>
    <ic-timeline v-if="page.items">
        <ic-timeline-item v-for="i in page.items" :key="i.id">
            <span slot="time">
                <ic-time :timestamp="i.time"/>
            </span>
            <div v-if="i.type === NOTIF_TYPE.MANAGE_INFO_ABOUT_ME" class="notif-content" slot="content">
                <div v-if="i.related_type === POST_TYPES.COMMENT">
                    <div style="display: flex">
                        <template>你在</template><template>{{typeName(i.loc_post_type)}}</template>
                        <!-- 某地 -->
                        <b class="limit m12">
                            <post-link :goto="false" :show-type="false" :type="i.loc_post_type" :item="{id: i.loc_post_id, post_title: i.loc_post_title}"/>
                        </b>
                        <template>下发表的{{typeName(i.related_type)}}以下评论：</template>
                    </div>
                    <div class="brief2" v-if="i.data.comment">{{atConvert(i.data.comment.content || '')}}</div>
                    <div>
                        <template>被</template>
                        <user-link :user="posts[i.sender_ids[0]]" />
                        <template>进行了以下操作：</template>
                    </div>
                </div>
                <div v-else style="display: flex">
                    <template>你发表的</template>
                    <template>{{typeName(i.related_type)}}</template>
                    <b class="limit m12">
                        <post-link :goto="false" :show-type="false" :type="i.related_type" :item="posts[i.related_id]"/>
                    </b>
                    <template>被</template>
                    <user-link :user="posts[i.sender_ids[0]]" />
                    <template>进行了以下操作：</template>
                </div>
                <div style="font-weight: bolder">
                    <template>{{MOPT[i.data.op]}}</template>
                    <template v-if="i.note"> - {{i.note}}</template>

                    <span style="margin-left: 0.5em;" v-if="i.data.op === MOP.TOPIC_BOARD_MOVE">
                        <template v-if="i.data.value">
                        <template>(</template>
                        <post-link :goto="false" :type="POST_TYPES.BOARD" :item="posts[i.data.value.change[0]]"/>
                        <template> -> </template>
                        <post-link :goto="false" :type="POST_TYPES.BOARD" :item="posts[i.data.value.change[1]]"/>
                        <template>)</template>
                        </template>
                    </span>
                    <ManageLogItemDetail v-else :item="i.data" :simple="true" />
                </div>
            </div>
            <div v-else class="notif-content" slot="content">
                <!-- 某人，使动者 -->
                <user-link :user="posts[i.sender_ids[0]]" />
                <!-- 介词 + 定语 -->
                <template v-if="i.type === NOTIF_TYPE.BE_COMMENTED">在你发表的</template>
                <template v-else>在</template><template>{{typeName(i.loc_post_type)}}</template>
                <!-- 某地 -->
                <b class="limit m12">
                    <post-link :goto="false" :show-type="false" :type="i.loc_post_type" :item="posts[i.loc_post_id]"/>
                </b>

                <!-- 做了某事，与某某有关 -->
                <template v-if="i.type === NOTIF_TYPE.BE_COMMENTED">
                    <!-- 发表评论（结合上文，实际是对你发表） -->
                    <template>下发表了{{typeName(i.related_type)}}</template>
                </template>
                <template v-else-if="i.type === NOTIF_TYPE.BE_REPLIED">
                    <!-- 回复（目前只能回复评论） -->
                    <template>下回复了你的{{typeName(i.related_type)}}</template>
                </template>
                <template v-else-if="i.type === NOTIF_TYPE.BE_MENTIONED">
                    <!-- 在某地的XX（如评论）中提到了你 -->
                    <template v-if="i.related_type">的{{typeName(i.related_type)}}</template><template>中提到了你</template>
                </template>
                <div v-else>{{i}}</div>

                <!-- 附加内容 -->
                <div class="brief">{{atConvert(i.brief || '')}}</div>
            </div>
        </ic-timeline-item>
    </ic-timeline>
    <div v-else class="empty">尚未有任何提醒</div>
    <paginator :page-info='page' :route-name='"account_notif"' :link-method="'query'" />
  </div>
</template>

<style lang="scss" scoped>
.notif-content {
  margin-top: 10px;
  white-space: nowrap;

  .brief {
    color: lighten($gray-600, 0.4);
    margin-top: 10px;
  }

  .brief2 {
    color: lighten($gray-600, 0.4);
    margin-top: 10px;
    margin-bottom: 10px;
  }
}
</style>

<script>
import { retcode } from 'slim-tools'
import ManageLogItemDetail from '@/components/misc/manage-log-item-detail.vue'
import { atConvert } from '@/utils/misc'

export default {
  data () {
    return {
      posts: {},
      POST_TYPES: this.$misc.POST_TYPES,
      NOTIF_TYPE: this.$misc.NOTIF_TYPE,
      MOP: this.$misc.MANAGE_OPERATION,
      MOPT: this.$misc.MANAGE_OPERATION_TXT,
      page: {}
    }
  },
  created: async function () {
    await this.fetchData()
  },
  methods: {
    atConvert,
    typeName: function (type) {
      return this.$misc.POST_TYPES_TXT[type]
    },
    fetchData: async function () {
      this.$store.commit('LOADING_INC', 1)
      let params = this.$route.query
      this.page.curPage = params.page
      let ret = await this.$api.notif.list({
        receiver_id: this.$user.data.id,
        order: 'time.desc'
        // loadfk: {user_id: null, board_id: null}
      }, params.page, { role: this.$user.basicRole })

      if (ret.code === retcode.SUCCESS) {
        let userIds = new Set()
        let manageInfoList = []

        for (let i of ret.data.items) {
          for (let uid of i.sender_ids) {
            userIds.add(uid)
          }
          if (i.type === this.$misc.NOTIF_TYPE.MANAGE_INFO_ABOUT_ME) {
            // 跳过一种出问题的情况
            if (!i.data.value) continue
            this.posts[i.related_id] = {
              'id': i.related_id,
              'post_type': i.related_type,
              'post_title': i.data.title
            }
            if (i.data.op === this.MOP.TOPIC_BOARD_MOVE) {
              this.posts[i.data.value.change[0]] = {
                'id': i.data.value.change[0],
                'post_type': this.POST_TYPES.BOARD,
                'post_title': i.data.move_info[0]
              }
              this.posts[i.data.value.change[1]] = {
                'id': i.data.value.change[1],
                'post_type': this.POST_TYPES.BOARD,
                'post_title': i.data.move_info[1]
              }
            }
            continue
          }
          this.posts[i.loc_post_id] = {
            'id': i.loc_post_id,
            'post_type': i.loc_post_type,
            'post_title': i.loc_post_title // 一个虚假的列，在post-link中高于其他声明
          }
        }

        let posts2 = await $.getBasePostsByIDs(async (i) => {
          return [
            {
              'type': i.related_type,
              'id': i.related_id
            }
          ]
        }, manageInfoList)
        // , null, this.$api, this.$store

        for (let [k, v] of Object.entries(posts2)) {
          this.posts[k] = v
        }

        if (userIds.size > 0) {
          let users = await this.$api.user.list({
            'id.in': JSON.stringify(new Array(...userIds)),
            'select': 'id, nickname'
          }, 1)
          for (let t of users.data.items) {
            this.posts[t.id] = t
          }
        }

        this.page = ret.data
        // let pageNumber = this.$route.query.page
        // if (pageNumber) this.commentPage = parseInt(pageNumber)

        let ret2 = await this.$api.notif.setRead()
        if (ret2.code === retcode.SUCCESS) {
          // 会出现负数问题
          // state.unread -= ret2.data
          this.$store.commit('user/SET_UNREAD', 0)
        }
      } else {
        if (ret.code === retcode.NOT_FOUND) {
        } else {
          this.$message.byCode(ret.code)
        }
      }
      this.$store.commit('LOADING_DEC', 1)
    }
  },
  components: {
    ManageLogItemDetail
  },
  watch: {
    '$route': 'fetchData'
  }
}
</script>
