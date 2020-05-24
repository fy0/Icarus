<template>
  <div class="ic-container" v-if="topic.user_id">
    <div class="nav ic-xs-hidden">
        <span>
            <nuxt-link :to="{ name: 'forum' }">社区</nuxt-link>
        </span>
        <span class="item-separator">/</span>
        <span>
            <nuxt-link :to="{ name: 'forum_board', params: {id: topic.board_id.id} }" :title="topic.board_id.name">{{textLimit(topic.board_id.name, 8)}}</nuxt-link>
        </span>
        <span class="item-separator">/</span>
        <span>
            <span :title="topic.title">{{topic.title}}</span>
            <span v-if="topic.state === POST_STATE.CLOSE">[关闭]</span>
        </span>
    </div>

    <!-- 移动端使用独立的标题 -->
    <div class="ic-xs ic-hidden">
        <div style="display: flex; justify-content: space-between; width: 100%">
            <div style="display: flex; white-space: nowrap;">
                <span>
                    <nuxt-link :to="{ name: 'forum' }">社区</nuxt-link>
                </span>
                <span class="item-separator">/</span>
                <span style="display: flex">
                    <nuxt-link class="limit m8" :to="{ name: 'forum_board', params: {id: topic.board_id.id} }">{{topic.board_id.name}}</nuxt-link>
                </span>
            </div>
            <div style="display:flex; flex-direction: column;">
                <div style="margin-left: 10px">发布于 <ic-time :timestamp="topic.time" /></div>

                <div style="display: flex; align-items: center; margin-left: -3px; justify-content: flex-end;">
                    <user-link style="display: flex; padding: 6px 0; align-items: center;" class="user-link" :nickname="false" :user="topic.user_id">
                        <avatar style="margin-right: 6px;" :user="topic.user_id" :size="24" class="avatar"></avatar>
                        <span>{{topic.user_id.nickname}}</span>
                    </user-link>
                </div>
            </div>
        </div>
    </div>
    <h2 class="ic-xs ic-hidden">{{topic.title}}</h2>

    <div class="topic-box">
        <div class="main">
            <div class="article typo">
                <!--<h1>{{topic.title}}</h1>-->
                <div class="content" v-if="topic.visible === POST_VISIBLE.CONTENT_IF_LOGIN && (!topic.content)">
                    <p>登陆后可见正文</p>
                </div>
                <div class="content" v-else v-html="marked(topic.content || '')"></div>
                <!-- 操作日志 -->
                <div v-if="mlog && mlog.items" class="post-manage-log">
                    <div class="post-manage-log-item" v-for="i in mlog.items.slice(0, 5)" :key="i.id">
                        <span>🛠️<user-link :user="i.user_id" /> 对此主题进行了<b>{{MANAGE_OPERATION_TXT[i.operation]}}</b>操作 - <ic-time :timestamp="i.time" /></span>
                    </div>
                    <div v-if="mlog.items.length > 5">...</div>
                </div>

                <div style="display: flex; align-items: center;">
                    <span>分享：</span>
                    <social-share />
                </div>

                <p class="ic-hr-30" ref="comment-hr"></p>
                <comment-list :item="topic" :cur-page="commentPage" :post-type="POST_TYPES.TOPIC"/>
            </div>
        </div>

        <div class="info ic-xs-hidden">
            <div class="box">
                <div class="author">
                    <div style="display: flex; align-items: center;">
                        <avatar :user="topic.user_id" :size="60" class="avatar"></avatar>
                        <div style="margin-left: 6px; line-height: 1.3em;">
                            <user-link :user="topic.user_id" />
                            <div>{{USER_GROUP_TXT[topic.user_id.group]}}</div>
                        </div>
                    </div>
                </div>
                <div class="other">
                    <div class="txt3">
                        <div>发布时间：<ic-time :timestamp="topic.time" /></div>
                        <div>最后修改：<ic-time :timestamp="topic.edit_time" /></div>
                        <div>阅读次数：<span>{{topic.s.click_count}}</span></div>
                    </div>

                    <div v-if="false">
                        <a  class="furbtn furbtn-s furbtn-blue"><i class="fa fa-star-o"></i> 关注作者</a>
                        <a class="furbtn furbtn-s furbtn-green"><i class="fa fa-heart-o"></i> 收藏主题</a>
                        <a class="furbtn furbtn-s furbtn-green" fav="1"><i class="fa fa-heart"></i> 取消收藏</a>
                        <a class="furbtn furbtn-s furbtn-blue" follow="1"><i class="fa fa-star"></i> 取消关注</a>
                    </div>

                    <p><nuxt-link v-if="$user.data && (topic.user_id.id == $user.data.id)" :to="{ name: 'forum_topic_edit', params: {id: topic.id} }">编辑文章</nuxt-link></p>
                    <div class="last-edit" v-if="topic.edit_time" style="font-size: 0.8em">
                        <p>此文章由 <user-link :user="topic.last_edit_user_id" /> 最后编辑于 <ic-time :timestamp="topic.edit_time" /></p>
                        <p>历史编辑次数 {{topic.edit_count}} 次</p>
                    </div>
                    <div class="topic-manage" v-if="isBoardAdmin">
                        <i class="icarus icon-39" title="管理" style="color: #71c1ef; cursor: pointer" @click="setTopicManage({ 'val': true, 'data': topic })"></i>
                    </div>

                    <div v-if="topicIndex && topicIndex.length" class="topic-index-container" ref="index" :class="{'sticky': indexSticky}">
                        <h2>目录</h2>
                        <ul class="topic-index">
                            <li v-for="(i, _) in topicIndex" :key="_">
                                <a :class="[indexActive == _ ? 'active' : '', `h${i.depth}`]" :href="`#til-${_+1}`" @click.prevent.stop="scrollTo(`til-${_+1}`)">{{i.text}}</a>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <ic-hangbtn title="去往评论区" style="right: calc(8% + 45px)" :check-display="inCommentArea" :onclick="goComment">
        <i class="icarus icon-comment-multiple-out"></i>
        <!-- <i class="icarus icon-comment-outline"></i> -->
    </ic-hangbtn>
    <dialog-topic-manage />
  </div>
  <page-not-found v-else />
</template>

<style>
.topic-box {
  margin-top: 25px;
}

/* 列表靠左对齐：不行，这会毁灭多级列表，子级会失去相对父级的缩进 */
/* .topic-box .article > .content ul {
  padding-left: 0;
  list-style-position: inside;
}

.topic-box .article > .content ol {
  padding-left: 0;
  list-style-position: inside;
} */
</style>

<style lang="scss" scoped>
.nav {
  width: 65%;
  overflow: hidden;
  text-overflow: ellipsis;
  /* word-break: break-all; */
  white-space: nowrap;
  font-size: 18px;
}

.post-manage-log {
  padding: 5px 0;
  margin-top: 20px;
  font-size: 14px;

  .post-manage-log-item {
    color: $gray-500;
  }
}

.item-separator {
  margin: 0 8px;
  color: #d7dde4;
}

.topic-manage > .group {
  display: flex;
}

.topic-manage > .group > a {
  padding: 5px 10px;
}

.topic-box {
  display: flex;
}

.topic-box > .main {
  flex: 18 0 0%;
  width: 0%;
}

.info {
  max-width: $page-left-max-width;

  > .box {
    padding: 0 20px;

    > .other {
      padding-top: 30px;
    }
  }
}

.other > .txt3 {
  font-size: 14px;
}

.info > .author {
  display: flex;
  flex-direction: column;
  font-size: 16px;
}

.main > .article > h1 {
  font-size: 28px;
  line-height: 48px;
  text-align: center;
}

.topic-box > .info {
  flex: 6 0 0%;
}

.topic-index-container {
  &.sticky {
    position: fixed;
    top: 0;
  }

  > h2 {
    font-size: 16px;
    margin-top: 10px;
  }
}

.topic-index {
  font-size: 14px;
  padding-left: 0;
  margin-top: 0;
  list-style-position: inside;

  li {
    font-size: 14px;
    list-style: none;
    font-weight: normal;
    padding-bottom: 5px;
    margin-left: 0;

    a {
      color: $gray-500;
      margin-left: 3em;
      display: block;
      height: 100%;
    }

    a.active {
      font-weight: bold;
      color: $gray-600;
    }

    .h1, .h2 { margin-left: 1em; }
    .h3, .h4 { margin-left: 2em; }
    .h2::before { content:"∎ "; }
    .h3::before { content:"> "; }
    .h4::before { content:"⎔ "; }
    .h5::before { content:"○ "; }
    .h6::before { content:"⋄ "; }
  }
}
</style>

<script>
import { marked, mdGetIndex } from '@/utils/md.ts'
import { mapState, mapGetters, mapMutations } from 'vuex'
import { BaseWrapper, createFetchWrapper } from '@/fetch-wrap'
import CommentList from '@/components/misc/comment-list.vue'
import SocialShare from '@/components/misc/social-share.vue'
import '@/assets/css/_forum.scss'
import { retcode } from 'slim-tools'
import { scrollTo } from '@/utils/misc'

class FetchCls extends BaseWrapper {
  async fetchData () {
    let params = this.$route.params
    let role = this.$user ? this.$user.basicRole : null

    let ret = await this.$api.topic.get({
      id: params.id,
      loadfk: { user_id: null, board_id: null, last_edit_user_id: null, 'id': { 'as': 's' } }
    }, { role })

    if (ret.code === retcode.SUCCESS) {
      let mlog = await this.$api.logManage.list({
        related_id: ret.data.id,
        order: 'time.desc',
        loadfk: { 'user_id': null }
      })
      if (mlog.code === retcode.SUCCESS) {
        this.mlog = mlog.data
      }

      let pageNumber = this.$route.query.page
      if (pageNumber) this.commentPage = parseInt(pageNumber)
      this.topic = ret.data
      this.topicIndex = mdGetIndex(ret.data.content)
    } else {
      if (ret.code !== retcode.NOT_FOUND) {
        this.$message.byCode(ret.code)
      }
    }
  }
}

export default {
  data () {
    return {
      commentPage: 1,
      loading: true,
      topic: { board_id: { id: 1 } },
      topicIndex: [],
      indexActive: -1,
      indexSticky: false,
      mlog: null
    }
  },
  head () {
    return {
      title: `${this.topic.title} - ${this.topic.board_id.name}`,
      meta: [
        { hid: 'description', name: 'description', content: '文章' }
      ]
    }
  },
  computed: {
    ...mapState(['config']),
    ...mapGetters([
      'POST_STATE',
      'POST_TYPES',
      'POST_VISIBLE',
      'USER_GROUP_TXT',
      'MANAGE_OPERATION_TXT'
    ]),
    ...mapGetters('forum', [
      'isNewSite'
    ]),
    isBoardAdmin () {
      // TOOD: 检查是否为版主
      return this.$user.isForumAdmin
    }
  },
  methods: {
    ...mapMutations('dialog', {
      'setTopicManage': 'SET_TOPIC_MANAGE'
    }),
    marked,
    textLimit: $.textLimit,
    scrollTo: function (id) {
      let el = document.getElementById(id)
      scrollTo(el)
    },
    fetchData: async function () {

    },
    inCommentArea: function () {
      let el = this.$refs['comment-hr']
      return document.documentElement.scrollTop + 1 < el.offsetTop + el.clientHeight
    },
    goComment: function () {
      let el = this.$refs['comment-hr']
      scrollTo(el)
    }
  },
  watch: {
    '$route.query.page': async function (val) {
      this.commentPage = val
    }
  },
  created: async function () {
    // 注意：从这里观察出一个现象：
    // created 会比 mounted 早触发，但并不一定更早完成
    // await 占用时间的时候，挂载流程仍将继续
    if (!process.browser) return
    this.$nextTick(() => {
      // 右侧目录跟随滚动
      let elTop = 0
      let scrollHandle = (e) => {
        let el = this.$refs.index
        let el2 = this.$refs['comment-hr']
        if (!el || !el2) {
          window.removeEventListener('scroll', scrollHandle)
          return
        }

        // 目录，上不超过他自己所在的位置，下不超过评论分界线
        let del = document.documentElement
        let scrollTop = del.scrollTop
        let end1 = del.offsetTop + del.clientHeight // 自身最底部（如果文章内容短而目录多，会发生目录伸到下面的情况）
        let end2 = el2.offsetTop - el.clientHeight // 评论界限
        let end = Math.max(end1, end2)
        elTop = Math.max(el.offsetTop, elTop)

        this.indexSticky = scrollTop > elTop

        // 超越最大边界
        if (scrollTop >= end) {
          el.style.transform = 'translateY(-' + (scrollTop - end) + 'px)'
        } else {
          el.style.transform = ''
        }
      }

      window.addEventListener('scroll', scrollHandle)

      let loop = () => {
        if (!this.$refs.index) return
        let scrollTop = document.documentElement.scrollTop

        for (let i = 0; i < this.topicIndex.length; i++) {
          let el = document.getElementById(`til-${i + 1}`)
          if (el.offsetTop >= (scrollTop - 5)) {
            this.indexActive = i
            break
          }
        }
        setTimeout(loop, 100)
      }
      setTimeout(loop, 100)
    })
  },
  async asyncData (ctx) {
    let f = createFetchWrapper(FetchCls, ctx)
    await f.fetchData()
    return f._data
  },
  mounted: function () {
  },
  components: {
    SocialShare,
    CommentList
  }
}
</script>
