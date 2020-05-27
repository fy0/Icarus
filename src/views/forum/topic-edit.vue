<template>
  <loading v-if="pageLoading"/>
  <div v-else class="ic-container">
    <div class="edit-page-title">
        <h3 class="" v-if="!isEdit">新建主题</h3>
        <h3 class="" v-else>编辑主题<span v-if="asAdmin"> - 管理员模式</span></h3>
        <button class="ic-btn primary right-top-btn" type="primary" :loading="loading" @click="send">{{postButtonText}}</button>
    </div>

    <form class="ic-form" id="form_topic" method="POST" @submit.prevent="send">
        <check-row :results="formErrors.title" :multi="true">
            <input type="text" name="title" v-model="topicInfo.title" :placeholder="`这里填写标题，${$misc.BACKEND_CONFIG.TOPIC_TITLE_LENGTH_MIN} - ${$misc.BACKEND_CONFIG.TOPIC_TITLE_LENGTH_MAX} 字`">
        </check-row>
        <check-row :results="formErrors.board_id" :multi="true" v-if="(!isEdit) || asAdmin">
            <multiselect v-model="topicInfo.board_id" :allow-empty="false" :options="boardList" :custom-label="getSelectOptionName" placeholder="选择一个板块" style="z-index: 2" open-direction="bottom"></multiselect>
        </check-row>
        <check-row :results="formErrors.content" :multi="true">
            <markdown-editor ref="editor" v-model="topicInfo.content" rows="15" autofocus></markdown-editor>
        </check-row>
        <div class="ic-form-row">
            <button class="ic-btn primary" style="float: right" type="primary" :loading="loading">{{postButtonText}}</button>
        </div>
    </form>
  </div>
</template>

<style lang="scss" scoped>
#form_topic input[name='title'] {
  padding: 6px 12px;
  width: 100%;
  font-weight: bolder;
  border-radius: 5px;
  box-shadow: none;
  border: 1px solid #e8e8e8;
  outline: none;
}

.error {
  #form_topic input[name='title'] {
      border: 1px solid $danger;
  }
}

.edit-page-title {
  display: flex;
  padding: 20px 0;
  padding-top: 0;
  justify-content: space-between;
  align-items: center;
}

.ic-form-row {
  margin-bottom: 10px;
}

.form-select-row {
  /* 此举是为了避免 ic-form 对 input 的样式覆盖。
      不然select会出现外框套内框这样的事情 */
  margin-bottom: 10px;
}

.el-select > .el-input > input[readonly] {
  background-color: #fff;
  color: #1f2d3d;
}
</style>

<style>
div.markdown-editor > div.editor-toolbar {
  border-color: #ddd !important;
}

/* 这部分内容是动态生成的 因此写在scope中无效 */
.ic-form > .ic-form-row.error > div.markdown-editor > div.editor-toolbar {
  opacity: 1; /* 上下颜色一致 */
  border-color: #FF6060 !important;
}

.ic-form > .ic-form-row.error > .markdown-editor > .cm-s-easymde {
  border-left-color: #FF6060 !important;
  border-right-color: #FF6060 !important;
  border-bottom-color: #FF6060 !important;
}

.editor-preview img {
  width: 100%;
}

.multiselect__tags {
  border: 1px solid #ddd !important;
}
</style>

<script>
import Multiselect from 'vue-multiselect'
import 'vue-multiselect/dist/vue-multiselect.min.css'
import markdownEditor from '@/components/misc/markdown-editor.vue'
import Objectid from 'bson-objectid'
// import marked from '@/utils/md.ts'
import './topic-edit-fa'
import { retcode } from 'slim-tools'
import { asyncGetUploadToken } from '@/utils/upload'

export default {
  data () {
    return {
      asAdmin: false,
      pageLoading: true,
      loading: false,
      boardList: [],
      boardInfo: {},
      save: {},

      topicInfo: {
        title: '',
        board: null,
        board_id: null,
        content: ''
      },

      formErrors: {
        title: [],
        content: []
      }
    }
  },
  head () {
    return {
      title: `${this.isEdit ? '编辑主题' : '新建主题'}`,
      meta: [
        { hid: 'description', name: 'description', content: '百科' }
      ]
    }
  },
  computed: {
    isEdit () {
      return this.$route.name === 'forum_topic_edit'
    },
    postButtonText: function () {
      return this.loading ? '请等待'
        : (this.isEdit ? '编辑' : '发布')
    }
  },
  methods: {
    getSelectOptionName (id) {
      let { name, brief } = this.boardInfo[id]
      return `${name} — [${brief}]`
    },
    send: async function (e) {
      let ret
      let successText

      if (!this.topicInfo.board_id) {
        this.$message.error('没有选择发布的板块，如果没有板块，请先在管理界面创建。')
        return
      }

      let topicId
      if (this.loading) return
      this.loading = true

      let topicInfo = $.objDiff({
        'title': this.topicInfo.title,
        'board_id': this.topicInfo.board_id,
        'content': this.topicInfo.content,
        'returning': true
      }, this.save)

      if (this.isEdit) {
        if (Object.keys(topicInfo).length <= 1) {
          // 那个1是returning
          this.$message.success('编辑成功！但编辑者并未进行任何改动。')
          this.$router.push({ name: 'forum_topic', params: { id: this.topicInfo.id } })
          this.loading = false
          return
        }

        if (this.asAdmin) {
          ret = await this.$api.topic.set({ id: this.topicInfo.id }, topicInfo)
        } else {
          ret = await this.$api.topic.set({ id: this.topicInfo.id }, topicInfo, { role: 'user' })
        }
        successText = '编辑成功！已自动跳转至文章页面。'
        topicId = this.topicInfo.id
      } else {
        ret = await this.$api.topic.new(topicInfo, { role: 'user' })
        successText = '发表成功！已自动跳转至文章页面。'
        topicId = ret.data.id
      }

      if (ret.code === 0) {
        localStorage.setItem('topic-post-cache-clear', 1)
        this.$router.push({ name: 'forum_topic', params: { id: topicId } })
        this.$message.success(successText)
      } else if (ret.code === retcode.INVALID_ROLE) {
        this.$message.error('抱歉，您的账户为未激活账户，无法发表主题，请检查邮件。若未收到，请在设置界面重新发送激活邮件。')
        this.loading = false
      } else {
        if (ret.code === retcode.FAILED) {
          this.formErrors = ret.data
          this.$message.error('内容不符合要求，请根据输入框下方提示进行修改')
        } else {
          this.formErrors = {}
          this.$message.byCode(ret.code, ret.data)
        }
        // 注意：发布成功会跳转，故不做复位，失败则复位
        this.loading = false
      }
    },
    fetchData: async function () {
      this.pageLoading = true
      let params = this.$route.params
      this.asAdmin = this.$route.query.manage

      if (!this.$user.data) {
        this.$message.error('抱歉，无权访问此页面，请返回')
        return
      }

      let boardQueryParams = {}
      if (!this.$user.isForumAdmin) {
        boardQueryParams['can_post_rank.<'] = 100
      }
      let ret = await this.$api.board.list(boardQueryParams)
      if (ret.code) {
        this.$message.byCode(ret.code)
        return
      }
      let boardList = ret.data.items

      if (this.isEdit) {
        let ret = await this.$api.topic.get({
          id: params.id,
          loadfk: { user_id: null, board_id: null }
        })
        if (ret.code) {
          this.$message.error('抱歉，发生了错误')
          return
        }

        /* eslint-disable no-control-regex */
        ret.data.content = ret.data.content.replace(/\x01(.+?)\x01/g, '@$1')
        this.topicInfo = ret.data
        this.save = _.clone(ret.data)
        this.save.board_id = this.save.board_id.id
      }

      this.boardList = []
      for (let board of boardList) {
        this.boardInfo[board.id] = board
        this.boardList.push(board.id)
      }

      if (boardList.length) {
        if (!this.isEdit) {
          // 若是新建，给一个默认板块
          this.topicInfo.board_id = boardList[0].id
          // 若指定了板块id，那么按设置来
          if (params.board_id) {
            for (let i of boardList) {
              if (i.id === params.board_id) {
                this.topicInfo.board_id = i.id
                break
              }
            }
          }
        } else {
          // 若不是新建，那么按文章的板块来
          for (let i of boardList) {
            if (i.id === this.topicInfo.board_id.id) {
              this.topicInfo.board_id = i.id
              break
            }
          }
        }
      }

      this.pageLoading = false
    }
  },
  // beforeRouteEnter (to, from, next) {
  //     if (!store.state.user.userData) {
  //         store.commit('LOADING_SET', 0)
  //         // nprogress.done()
  //         this.$message.error('在登录后才能发帖。请登录账号，如果没有账号，先注册一个。')
  //         return next('/')
  //     }
  //     next()
  // },
  mounted: async function () {
    // if (localStorage.getItem('topic-post-cache-clear')) {
    //     // 我不知道为什么，在地址跳转前进行 storage 的清除工作，
    //     // 并不会实质上起效，因此这是一个替代手段，效果比较理想。
    //     localStorage.removeItem('topic-post-title')
    //     localStorage.removeItem('smde_topic-post-content')
    //     localStorage.removeItem('topic-post-cache-clear')
    // }

    if (!this.isEdit) {
      // this.title = localStorage.getItem('topic-post-title') || ''
    }
  },
  created: async function () {
    // 未登录跳转
    if (!this.$store.state.user.userData) {
      this.$store.commit('LOADING_SET', 0)
      // nprogress.done()
      this.$message.error('在登录后才能发帖。请登录账号，如果没有账号，先注册一个。')
      return this.$router.push('/')
    }

    let uploadBackend = this.$misc.BACKEND_CONFIG.UPLOAD_BACKEND

    await this.fetchData()
    let vm = this

    let func = async () => {
      let editor = this.$refs.editor
      if (editor) {
        let uploadImage = async function (editor, fileList) {
          let theFile = null

          if (fileList.length === 0) return
          for (let i of fileList) {
            if (i.type.indexOf('image') !== -1) {
              theFile = i
              break
            }
          }
          if (!theFile) return false

          let placeholder = `![Uploading ${theFile['name']} - ${(new Objectid()).toString()} ...]()`
          editor.replaceRange(placeholder, {
            line: editor.getCursor().line,
            ch: editor.getCursor().ch
          })

          if (uploadBackend === 'qiniu') {
            let token = await asyncGetUploadToken()
            let qiniu = require('qiniu-js')
            let ob = qiniu.upload(theFile, null, token, null)

            ob.subscribe({
              complete: (ret) => {
                // 注意，这里的res是本地那个callback的结果，七牛直接转发过来了
                // console.log('done', ret)
                if (ret.code === retcode.SUCCESS) {
                  // let url = `${config.qiniu.host}/${ret.data}` // -${config.qiniu.suffix}
                  let url = `${vm.$misc.BACKEND_CONFIG.UPLOAD_STATIC_HOST}/${ret.data}`
                  let suffix = vm.$misc.BACKEND_CONFIG.UPLOAD_QINIU_IMAGE_STYLE_TOPIC
                  if (suffix) url += `-${suffix}`
                  let newTxt = `![](${url})`
                  let offset = newTxt.length - placeholder.length
                  let cur = editor.getCursor()
                  editor.setValue(editor.getValue().replace(placeholder, newTxt + '\n'))
                  editor.setCursor(cur.line, cur.ch + offset)
                }
              }
            })
          } else {
            let ret = await vm.$api.upload.upload(theFile, 'user')
            console.log('file upload', ret)
          }
        }

        let cm = editor.simplemde.codemirror
        cm.on('drop', async (editor, e) => {
          await uploadImage(editor, e.dataTransfer.files)
        })
        cm.on('paste', async (editor, e) => {
          if (e.clipboardData.files.length > 0) {
            // fix for macos
            e.preventDefault()
          }
          await uploadImage(editor, e.clipboardData.files)
        })
      } else {
        setTimeout(func, 500)
      }
    }
    setTimeout(func, 500)
  },
  watch: {
    'topicInfo.title': _.debounce(function (val, oldVal) {
      localStorage.setItem('topic-post-title', val)
    }, 5000)
  },
  components: {
    Multiselect,
    markdownEditor
  }
}
</script>
