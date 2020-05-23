<template>
  <div v-if="!notFound">
    <div
      v-if="false"
      class="ic-paper board-header"
      :style="lineStyleBG(board.id)"
      style="margin-bottom: 30px; margin-top: -15px; width: 100%"
    >
      <div class="left">
        <h3 class="name">{{ board.name }}</h3>
        <div class="brief">{{ board.brief }}</div>
      </div>
    </div>

    <!-- 刷新标题 -->
    <!-- <template v-if="board">
      <div v-title-dynamic v-if="$route.params.page && $route.params.page > 1">{{ board.name }} - 第{{$route.params.page}}页 - {{config.title}}</div>
      <div v-title-dynamic v-else>{{ board.name }} - {{config.title}}</div>
  </template>
    <div v-else v-title>全部主题 - {{config.title}}</div>-->

    <div class="ic-container forum-box">
      <div class="wrapper">
        <div class="ic-xs ic-hidden">
          <!-- <i @click="showSlideMenu = !showSlideMenu" class="icarus icon-comment-multiple-out" style="position: fixed; top: 6px; left: 20px; font-size: 22px; z-index: 1; color: #777" /> -->

          <!-- xs 时的边栏 -->
          <transition enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
            <div v-if="showSlideMenu" class="dialog-overlay" @click="showSlideMenu = false"></div>
          </transition>

          <transition
            enter-active-class="animated slideInLeft faster"
            leave-active-class="animated slideOutLeft"
          >
            <div v-if="showSlideMenu" class="left-nav bs4-xs" style="overflow-y: auto;">
              <div class="left-nav-box">
                <nuxt-link
                  class="ic-btn primary post-new-topic"
                  @mouseover.native="mouseOverPostNewBtn = true"
                  @mouseleave.native="mouseOverPostNewBtn = false"
                  :style="postNewTopicStyle"
                  :to="{ name: 'forum_topic_new', params: {'board_id': boardId } }"
                >发表主题</nuxt-link>

                <div class="ul-boards">
                  <nuxt-link
                    :to="{ name: 'index', query: $route.query}"
                    class="item"
                    :class="{'showAll': !isBoard}"
                    style="margin-top: 21px"
                  >
                    <div class="sign"></div>
                    <span class="title">全部主题</span>
                  </nuxt-link>

                  <label v-if="isBoard" class="with-subboard-topic">
                    <ic-checkbox :size="14" v-model="withSubBoardTopic">包含子板块内容</ic-checkbox>
                  </label>
                  <!-- <div style="margin-bottom: 3px;"></div> -->
                  <nuxt-link
                    v-for="j in dymBoardList"
                    :key="j.id"
                    :class="{'subboard': j.parent_id}"
                    class="item"
                    :to="{ name: 'forum_board', params: {id: j.id}, query: $route.query }"
                  >
                    <div v-if="j.parent_id === null" class="sign" :style="lineStyleBG(j.id)"></div>
                    <span class="title" :style="boardNavStyle(j)">{{boardNavTitle(j)}}</span>
                  </nuxt-link>
                </div>
              </div>
            </div>
          </transition>
        </div>

        <div class="left-nav ic-xs-hidden">
          <div class="left-nav-box">
            <!-- <span class="post-new-topic">板块列表</span> -->
            <nuxt-link
              class="ic-btn primary post-new-topic"
              @mouseover.native="mouseOverPostNewBtn = true"
              @mouseleave.native="mouseOverPostNewBtn = false"
              :style="postNewTopicStyle"
              :to="{ name: 'forum_topic_new', params: {'board_id': boardId } }"
            >发表主题</nuxt-link>

            <div class="ul-boards">
              <nuxt-link
                :to="{ name: 'index', query: $route.query}"
                class="item"
                :class="{'showAll': !isBoard}"
                style="margin-top: 22px"
              >
                <div class="sign"></div>
                <span class="title">全部主题</span>
              </nuxt-link>

              <label v-if="isBoard" class="with-subboard-topic">
                <ic-checkbox :size="14" v-model="withSubBoardTopic">包含子板块内容</ic-checkbox>
              </label>
              <!-- <div style="margin-bottom: 3px;"></div> -->
              <nuxt-link
                v-for="j in dymBoardList"
                :key="j.id"
                :class="{'subboard': j.parent_id}"
                class="item"
                :to="{ name: 'forum_board', params: {id: j.id}, query: $route.query }"
              >
                <div v-if="j.parent_id === null" class="sign" :style="lineStyleBG(j.id)"></div>
                <span class="title" :style="boardNavStyle(j)">{{boardNavTitle(j)}}</span>
              </nuxt-link>
            </div>
          </div>
        </div>

        <div class="right" id="board-list">
          <top-btns :board="board"></top-btns>
          <div
            class="ic-xs-hidden"
            style="border-bottom: 1px solid #eee; margin: 8px 10px 5px 10px;"
          ></div>
          <div style="flex: 1 0 0%;">
            <!-- 加载占位条目 -->
            <template v-if="loading">
              <div class="board-item-box" v-for="i in placeholderCount" :key="i">
                <a class="board-item">
                  <div class="title-recent">
                    <avatar :size="32" :placeholder="true" class="avatar"></avatar>
                    <div class="right">
                      <h2>
                        <span class="placeholder-text f18"></span>
                      </h2>
                      <p class="topic-info" style="width: 50%">
                        <span class="placeholder-text f14"></span>
                      </p>
                    </div>
                    <div class="append-icons"></div>
                  </div>
                  <div class="detail ic-xs-hidden">
                    <div class="count-block">
                      <div class="count">
                        <p class="num">
                          <span class="placeholder-text f16" style="width: 40%"></span>
                        </p>
                        <p class="txt">
                          <span class="placeholder-text f12" style="width: 30%"></span>
                        </p>
                      </div>
                      <div class="count">
                        <p class="num">
                          <span class="placeholder-text f16" style="width: 40%"></span>
                        </p>
                        <p class="txt">
                          <span class="placeholder-text f12" style="width: 30%"></span>
                        </p>
                      </div>
                    </div>
                    <div class="recent ic-xs-hidden ic-sm-hidden ic-md-hidden">
                      <span class="line"></span>
                      <div class="post">
                        <span class="placeholder-text f12" style="width: 50%"></span>
                        <span class="placeholder-text f12"></span>
                        <span class="placeholder-text f12" style="width: 75%"></span>
                      </div>
                      <div class="time">N/A</div>
                    </div>
                  </div>
                </a>
              </div>
            </template>

            <!-- 实际渲染条目 -->
            <template v-else-if="topics.items.length">
              <div
                class="board-item-box"
                :key="i.global_sticky_flag ? `gs-${i.id}` : i.id"
                v-for="i in topics.items"
                @mouseover="itemHover(i.id)"
                @mouseleave="itemHover(null)"
              >
                <!-- <nuxt-link :to="{ name: 'forum_topic', params: {id: i.id} }" class="board-item" :class="{'top-post': i.sticky_weight}"> -->
                <div
                  class="board-item"
                  :class="{'top-post': i.sticky_weight}"
                  @click="$router.push({ name: 'forum_topic', params: {id: i.id} })"
                >
                  <div class="title-recent">
                    <avatar @click.stop :user="i.user_id" :size="32" class="avatar" />
                    <div class="right">
                      <h2>
                        <nuxt-link
                          @click.stop
                          :title="i.title"
                          :to="{ name: 'forum_topic', params: {id: i.id} }"
                        >
                          <span>{{i.title}}</span>
                          <span v-if="i.state === POST_STATE.CLOSE">[关闭]</span>
                        </nuxt-link>
                      </h2>

                      <p class="topic-info">
                        <span @click.stop>
                          <nuxt-link
                            class="board-badge"
                            :to="{ name: 'forum_board', params: {id: i.board_id} }"
                            @click.stop
                          >
                            <span :style="lineStyleBG(i.board_id)" class="sign"></span>
                            <span class="name limit l2">{{boardBadgeTitleById(i.board_id)}}</span>
                          </nuxt-link>
                        </span>
                        <span class="author limit l2" @click.stop>
                          <user-link :user="i.user_id" />
                        </span>
                        <span class="time" @click.stop>
                          <ic-time :timestamp="i.edit_time || i.time" />
                        </span>
                      </p>
                    </div>

                    <span @click.stop class="icons">
                      <i
                        v-if="i.awesome == 1"
                        class="awesome icarus icon-diamond"
                        title="优秀"
                        @click.prevent
                      ></i>
                      <i v-if="false" class="icarus icon-crown" title="精华" style="color: #e8a85d"></i>
                      <i
                        v-if="$user.isForumAdmin && i.id === hoverId"
                        class="manage icarus icon-39 animated rotateIn"
                        title="管理"
                        @click.stop="setTopicManage({ 'val': true, 'data': i })"
                      ></i>
                    </span>

                    <div @click.stop class="append-icons">
                      <i v-if="i.sticky_weight" class="icarus icon-pin" title="置顶" />
                    </div>
                  </div>

                  <div class="detail ic-xs-hidden">
                    <div class="count-block">
                      <div class="count">
                        <p class="num">{{i.s.click_count}}</p>
                        <p class="txt">点击</p>
                      </div>
                      <div class="count">
                        <p class="num">{{i.s.comment_count}}</p>
                        <p class="txt">回复</p>
                      </div>
                    </div>
                    <div class="recent ic-xs-hidden ic-sm-hidden ic-md-hidden">
                      <span class="line" :style="lineStyle(i.board_id)"></span>
                      <div
                        class="post"
                        v-if="i.s.last_comment_id && i.s.last_comment_id.id"
                        @click.stop
                      >
                        <strong>
                          <i class="icon icarus icon-reply"></i>
                          <user-link :user="i.s.last_comment_id.user_id" />:
                        </strong>
                        <nuxt-link
                          tag="div"
                          class="post-content"
                          :to="{ name: 'forum_topic', params: {id: i.s.last_comment_id.related_id} }"
                        >{{atConvert(i.s.last_comment_id.content)}}</nuxt-link>
                      </div>
                      <div class="post" v-else>无回复</div>
                      <ic-time
                        v-if="i.s.last_comment_id"
                        class="time"
                        :timestamp="i.s.last_comment_id.time"
                      />
                      <div v-else class="time">N/A</div>
                    </div>
                  </div>
                </div>
                <!-- </nuxt-link> -->
              </div>
              <paginator v-if="isBoard" :page-info="topics" :route-name="'forum_board'" />
              <paginator v-else :page-info="topics" :route-name="'forum_main'" />
            </template>

            <template v-else>
              <div style="margin-left: 10px;">尚未有人发言……</div>
            </template>

            <!-- <div style="flex: 1 0 0%" v-if="(!loading) && (!(topics && topics.items.length))"> -->
          </div>
        </div>
      </div>
      <dialog-site-new v-if="isSiteNew" />
      <dialog-user-set-nickname
        v-else-if="$user.isNewUser && $user.data.change_nickname_chance > 0"
      />
      <dialog-topic-manage />
      <!-- <dialog-user-inactive-warn /> -->

      <ic-hangbtn
        class="ic-xs ic-hidden"
        title="打开侧栏"
        style="right: calc(8% + 45px)"
        :check-display="() => true"
        :onclick="() => { showSlideMenu = !showSlideMenu }"
      >
        <i class="icarus icon-control"></i>
      </ic-hangbtn>
    </div>
  </div>
  <page-not-found v-else />
</template>

<style scoped lang="scss">
.wrapper {
  display: flex;

  .left-nav {
    flex: 5 1 0%;
    max-width: $page-left-max-width;
  }

  .left-nav.bs4-xs {
    position: fixed;
    height: 100%;
    top: 0;
    left: 0;
    background: #fff;
    z-index: 3;
    padding-left: 15px;
    padding-top: 30px;
    width: 180px;
  }

  .right {
    flex: 19 1 0%;
  }
}

.dialog-overlay {
  top: 0;
  z-index: 2;
}

$left-nav-padding-right: 30px;
$left-nav-sign-padding: 10px;

.ul-boards {
  margin: 0;
  list-style: none;
  font-weight: 300;

  .item {
    min-height: 42px; // 右侧单项的一半
    display: flex;
    align-items: center;
    padding: 7px 0;
    font-size: 14px;
    font-weight: bolder;
    color: lighten($gray-600, 10%);

    &.subboard {
      padding-left: 16px;
    }

    &.showAll {
      font-weight: bold;
      color: $primary;
    }

    .sign {
      width: 1em;
      height: 1em;
      background-color: #000;
      border-radius: 3px;
      flex-shrink: 0;
    }

    .title {
      margin-left: $left-nav-sign-padding;
    }
  }
}

.left-nav-box {
  padding: 0 $left-nav-padding-right 0 0;
}

.post-new-topic {
  width: 100%;
  display: block;
}

.with-subboard-topic {
  display: flex;
  align-items: center;
  font-size: 14px;
  min-height: 42px;
  user-select: none;
  // margin-bottom: 7px;
  color: $gray-600;

  > .ic-checkbox {
    width: 100%;
  }

  span {
    margin-left: $left-nav-sign-padding;
  }
}

.board-header {
  background: #1f8dd6;
  padding: 2em 1em;
  color: #fff;
  display: flex;
  justify-content: center;
  text-align: center;
}
</style>

<script>
import '@/assets/css/_forum.scss'
import { retcode } from 'slim-tools'
import TopBtns from './topbtns.vue'
import { BaseWrapper, createFetchWrapper } from '@/fetch-wrap'
import { mapState, mapGetters, mapActions, mapMutations } from 'vuex'
import { atConvert } from '@/utils/misc'

class FetchCls extends BaseWrapper {
  getBoardExInfoById (boardId) {
    return this.$store.state.forum.exInfoMap[boardId] || {}
  }

  async fetchData () {
    let baseQuery1 = {
      select:
        'id, time, edit_time, user_id, board_id, title, state, awesome, weight, update_time, sticky_weight',
      loadfk: {
        user_id: null,
        id: {
          as: 's',
          loadfk: { last_comment_id: { loadfk: { user_id: null } } }
        }
      }
    }
    let baseQuery = _.cloneDeep(baseQuery1)
    let params = this.$route.params
    let page = 1

    // 包含子板块内容
    if (this.$storage.getUniversal('sbt')) {
      this.withSubBoardTopic = true
    }
    this.withSubBoardTopicOptionReady = true

    // 获取全局板块信息
    await this.$store.dispatch('forum/load')

    // 如果板块不存在
    if (params.id && !this.$store.state.forum.infoMap[params.id]) {
      this.notFound = true
      return
    }

    if (this.$store.getters['forum/isSiteNew']) {
      this.$dialogs.setSiteNew(true)
    } else {
      if (this.$user.isNewUser) {
        this.$dialogs.setUserNickname(true)
      }
    }

    // 具体板块
    if (this.$route.name === 'forum_board') {
      // 若是要求包含子板块内容
      if (this.$storage.getUniversal('sbt')) {
        let lst = [params.id]
        for (let i of this.getBoardExInfoById(params.id).subboardsAll) {
          lst.push(i.id)
        }
        baseQuery['board_id.in'] = JSON.stringify(lst)
      } else {
        baseQuery['board_id'] = params.id
      }
      page = params.page
    } else {
      baseQuery['sticky_weight.ne'] = 5
      page = params.page
    }

    let query = this.$route.query
    let order = 'weight.desc, update_time.desc' // 权重降序

    if (query.type === '2' || query.type === 2) {
      // 最近更新：更新时间降序
      order = 'update_time.desc, time.desc'
    }

    if (query.type === '3' || query.type === 3) {
      // 最近发布：发布时间降序
      order = 'time.desc'
    }

    if (query.type === '4' || query.type === 4) {
      // 最近回复：回复时间排序
      // 好吧，这个好像暂时还实现不了
      order = 'update_time.desc, time.desc'
    }

    if (this.isBoard) {
      // 在板块模式下加入当前板块的置顶
      order = 'sticky_weight.desc, ' + order
    }

    let retList = await this.$api.topic.list(
      Object.assign(
        {
          order: order
        },
        baseQuery
      ),
      page
    )
    if (retList.code === retcode.SUCCESS) {
      if (!this.isBoard && (!page || page === 1)) {
        // 首页
        let retStickyTopics = await this.$api.topic.list(
          Object.assign(
            {
              sticky_weight: 5, // 全局置顶项
              order: order
            },
            baseQuery1
          )
        )
        if (retStickyTopics.code === retcode.SUCCESS) {
          for (let i of retStickyTopics.data.items) {
            i.global_sticky_flag = true
          }
          retList.data.items = _.concat(
            retStickyTopics.data.items,
            retList.data.items
          )
        }
      }

      this.topics = retList.data
      this.loading = false
      return
    } else {
      this.topics = { items: [] }
    }

    // this.$message.byCode(retList.code)
    this.loading = false
  }
}

// let pageOneHack = function (to, from, next, store) {
//     // 这一hack的目标是抹除 /r/1 的存在，使其与 / 看起来完全一致
//     // 但似乎由于 nprogress 的存在，显得有点僵硬
//     if (to.name === 'forum_main' && (to.params.page === '1' || to.params.page === 1)) {
//         if (from.name === 'index') {
//             store.commit('LOADING_SET', 0)
//             nprogress.done()
//             return next(false)
//         }
//         return next({ name: 'index', query: to.query })
//     }
//     next()
// }

export default {
  data () {
    return {
      hoverId: null,
      loading: true,
      notFound: false,
      topics: { items: [] },
      withSubBoardTopic: false,
      withSubBoardTopicOptionReady: false,
      mouseOverPostNewBtn: false,
      placeholderCount: 20,
      // xs大小时的边栏
      showSlideMenu: false
    }
  },
  computed: {
    ...mapState(['config']),
    ...mapState('user', ['userData']),
    ...mapGetters(['POST_STATE']),
    ...mapGetters('forum', ['isSiteNew']),
    postNewTopicStyle: function () {
      if (!this.boardId) return
      let exInfo = this.getBoardExInfoById(this.boardId)
      let bgColor = null
      if (exInfo) {
        bgColor = this.mouseOverPostNewBtn ? exInfo.colorHover : exInfo.color
      }
      return { 'background-color': bgColor || '#777' }
    },
    isBoard: function () {
      return this.$route.name === 'forum_board'
    },
    board: function () {
      let bid = this.boardId
      if (bid) return this.getBoardInfo(bid)
      return null
    },
    boardId: function () {
      if (this.isBoard) {
        return this.$route.params.id
      }
      return null
    },
    dymBoardList: function () {
      let lst = []
      let curBoardId = this.boardId
      let chain = this.getBoardChainById(curBoardId)
      let topBoardId = chain[chain.length - 1]
      let state = this.$store.state

      let pushSubBoards = (i, chainIndex) => {
        let topId = chain[--chainIndex]
        // $.getBoardExInfoById(i.id)
        for (let j of state.forum.exInfoMap[i.id].subboards) {
          lst.push(j)
          if (j.id === topId) {
            pushSubBoards(j, chainIndex)
          }
        }
      }

      for (let i of state.forum.lst) {
        lst.push(i)

        if (i.id === topBoardId) {
          pushSubBoards(i, chain.length - 1)
        }
      }

      return lst
    }
  },
  methods: {
    ...mapMutations('dialog', {
      setTopicManage: 'SET_TOPIC_MANAGE'
    }),
    ...mapActions('forum', {}),
    atConvert,
    boardBadgeTitleById: function (id) {
      let chain = this.getBoardChainById(id)
      let ret = ''
      if (!chain) return
      if (chain.length > 1) chain = chain.slice(0, -1)
      for (let i = chain.length - 1; i >= 0; i--) {
        let board = this.getBoardInfo(chain[i])
        ret += `${board.name}`
        if (i !== 0) ret += '/'
      }
      return ret
    },
    boardNavTitle: function (board) {
      if (board.parent_id) {
        let chain = this.getBoardChainById(board.id)
        let prefix = _.times(chain.length - 2, () => '>').join('')
        return `${prefix} ${board.name}`
      }
      return board.name
    },
    boardNavStyle: function (board) {
      if (this.isBoard) {
        let chain = this.getBoardChainById(this.boardId)
        if (chain.indexOf(board.id) !== -1) {
          let exInfo = this.getBoardExInfoById(board.id)
          return {
            color: exInfo.color,
            'font-weight': 'bold'
          }
        }

        // 如果上一级被选中且开启了“包含子版块内容”
        if (this.withSubBoardTopic && board.parent_id === this.boardId) {
          // let exInfo = $.getBoardExInfoById(board.id)
          // return {'color': exInfo.color}
          // 本来是各种颜色，但是花花绿绿怪怪的，改成一个色
          return { color: 'rgb(126, 140, 201)' }
        }
      }
    },
    itemHover: function (id) {
      this.hoverId = id
    },
    lineStyleById: function (boardId, key = 'border-left-color') {
      let exInfo = this.getBoardExInfoById(boardId)
      if (exInfo) {
        return { [key]: exInfo.color }
      }
      return {}
    },
    lineStyle: function (boardId, key = 'border-left-color') {
      return this.lineStyleById(boardId, key)
    },
    lineStyleBG: function (boardId) {
      return this.lineStyleById(boardId, 'background-color')
    },
    getBoardInfo: function (boardId) {
      return this.$store.state.forum.infoMap[boardId]
    },
    getBoardExInfoById: function (boardId) {
      return this.$store.state.forum.exInfoMap[boardId] || {}
    },
    getBoardChainById: function (boardId) {
      if (!boardId) {
        return [null]
      }
      let exinfo = this.$store.state.forum.exInfoMap[boardId]
      if (!exinfo) return []
      return exinfo.chain
    }
  },
  // beforeRouteEnter (to, from, next) {
  //     return pageOneHack(to, from, next, store)
  // },
  // beforeRouteUpdate (to, from, next) {
  //     return pageOneHack(to, from, next, store)
  // },
  // beforeRouteLeave (to, from, next) {
  //     // if (to.name === 'forum_topic_new' && this.state.isInactiveUser()) {
  //     //     state.dialog.userInactive = true
  //     //     return false
  //     // }
  //     return next()
  // },
  head () {
    let title = ''
    if (this.board) {
      if (this.$route.params.page && this.$route.params.page > 1) {
        title = `${this.board.name} - 第${this.$route.params.page}页`
      } else {
        title = `${this.board.name}`
      }
    } else {
      title = '全部主题'
    }
    return {
      title,
      meta: [{ hid: 'description', name: 'description', content: '首页' }]
    }
  },
  created () {
    if (!process.browser) return
    this.$nextTick(function () {
      let ZingTouch = require('zingtouch')
      $.zt = $.zt || new ZingTouch.Region(document.body, false, false)
      let el = document.querySelector('.main')
      if (!el) return
      $.zt.unbind(el, 'swipe')
      $.zt.bind(
        el,
        'swipe',
        e => {
          let info = e.detail.data[0]
          let d = info.currentDirection
          if (d < 50 || d > 310) {
            // 向右滑动
            this.showSlideMenu = true
          } else if (d > 130 && d < 230) {
            // 向左滑动
            this.showSlideMenu = false
          }
        },
        false
      )
    })
  },
  async asyncData (ctx) {
    let f = createFetchWrapper(FetchCls, ctx)
    await f.fetchData()
    return f._data
  },
  watch: {
    // 如果路由有变化，会再次执行该方法
    // '$route': 'fetchData',
    $route: async function () {
      // 暂时用强制刷新替代
      window.history.go(0)
    },
    userData: async function (newVal) {
      // 用户登入登出后进行板块信息重载
      // TODO: 不理解为什么不执行
      // 注：已在其它地方处理
      // await this.$store.dispatch('forum/load')
    },
    withSubBoardTopic: async function (newVal, oldVal) {
      if (this.withSubBoardTopicOptionReady) {
        this.$storage.removeUniversal('sbt')
        if (newVal) this.$storage.setUniversal('sbt', 1)
        // 要重新抓取页面内容，这里先用强制刷新替代吧
        window.history.go(0)
        // await this.fetchData()
      }
    }
  },
  components: {
    TopBtns
  }
}
</script>
