<!-- 评论 -->
<template>
<div class="ic-comment-post" id="ic-comment-post">
    <div class="ic-comment" v-if="false">
        <avatar :user="this.$user.data" class="avatar"></avatar>
        <div class="right-box">
            <div class="ic-paper round ic-z1 not-signin-content">你的账号需要激活后才能发言，请检查邮箱</div>
        </div>
    </div>

    <div class="ic-comment" v-else-if="this.$user.data">
        <avatar :depth="editing ? 3 : 1" :user="this.$user.data" class="avatar"></avatar>
        <div class="right-box" v-if="isClosed()">
            <div class="ic-paper round ic-z1 not-signin-content">评论已关闭</div>
        </div>
        <div class="right-box content" v-else>
            <textarea :class="[editing ? 'ic-z3' : 'ic-z1']" id="ic-comment-editor" @focus="onEditorFocus" @blur="onEditorBlur"
                class="ic-input ic-paper round" rows="5" v-model="commentInfo.content"
                :placeholder="'此处填写评论内容。\n可使用 markdown 语法。\n请理性讨论，友善发言，共同维护社区秩序。'">
            </textarea>
            <div style="display: flex; justify-content: space-between;" class="postBtnBox">
                <div v-if="!replyTo"></div>
                <div style="align-items: center; display: flex;" v-else>
                    <a href="javascript:void(0)" @click="setReplyTo(null)">×</a>
                    <div style="margin-left: 10px">
                        <template>正在回复：</template>
                        <a @click="highlightRepliedComment(replyTo.id)" :href="'#' + replyTo.id">{{replyTo.user_id.nickname}}#{{replyTo.post_number}}</a>
                    </div>
                </div>
                <div class="ic-paper round" :class="[editing ? 'ic-z3' : 'ic-z1']">
                    <button class="postBtn ic-btn primary" @click="commentPost">发表</button>
                </div>
            </div>
        </div>
    </div>

    <div class="ic-comment" v-else>
        <avatar :anonymous="true" class="avatar"></avatar>
        <div class="right-box">
            <div class="not-signin-content">
                需要 <nuxt-link :to="{ name: `account_signin` }">登录</nuxt-link> 后方可回复, 如果你还没有账号，那么可以 <nuxt-link :to="{ name: `account_signup` }">注册</nuxt-link> 一个帐号。
            </div>
        </div>
    </div>
</div>
</template>

<style scoped>
.ic-comment-post {
    margin-top: 20px
}

.ic-comment .not-signin-content {
    margin-left: 20px;
    min-height: 50px;
    padding: 10px 20px;
}

.ic-comment .content {
    min-height: 50px;
    line-height: 32px;
}

.ic-comment-post > .ic-comment {
    padding: 20px 0;
    border-bottom: none;
}

.right-box {
    flex: 1 0 0%;
    /* 视觉误差吧，总之加上之后舒服了一些*/
    margin-top: 1px;
}

#ic-comment-editor {
    width: 100%;
}

.postBtnBox {
    margin-top: 15px;
    margin-left: 15px;
}

.postBtn {
    padding-left: 20px;
    padding-right: 20px;
}
</style>

<script>
import anime from 'animejs'
import { scrollTo } from '@/utils/misc'

export default {
  props: {
    item: Object,
    postType: {}
  },
  data () {
    return {
      loading: false,
      replyTo: null,
      editing: false,
      commentInfo: {
        related_id: null,
        related_type: null,
        content: ''
      }
    }
  },
  created: function () {
  },
  mounted: function () {
    ;
  },
  methods: {
    isClosed () {
      if (this.postType === this.$misc.POST_TYPES.TOPIC) {
        return this.item.state <= this.$misc.POST_STATE.CLOSE
      }
      return false
    },
    setReplyTo: function (val) {
      this.replyTo = val
    },
    onEditorFocus: async function () {
      this.editing = true
    },
    onEditorBlur: async function () {
      this.editing = false
    },
    highlightRepliedComment: function (cid) {
      let el = document.getElementById(cid)
      scrollTo(el)
      anime({
        targets: el,
        duration: 2200,
        backgroundColor: ['rgba(255, 255, 255, 0)', '#ffffaa', 'rgba(255, 255, 255, 0)', '#ffffaa', 'rgba(255, 255, 255, 0)'],
        easing: 'easeInOutCirc'
      })
    },
    commentPost: async function () {
      if (this.loading) return
      this.loading = true
      this.commentInfo.related_id = this.item.id
      this.commentInfo.related_type = this.postType
      if (this.replyTo) this.commentInfo.reply_to_cmt_id = this.replyTo.id
      let ret = await this.$api.comment.new(this.commentInfo, 'user')
      this.$message.byCode(ret.code, ret.data)
      if (ret.code === 0) {
        this.editing = false
        this.replyTo = null
        this.commentInfo.content = ''
      }
      this.$emit('on-commented')
      this.loading = false
    }
  },
  components: {
  }
}
</script>
