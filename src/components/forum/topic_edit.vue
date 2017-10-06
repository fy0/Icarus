<template>
<div class="ic-container">
    <div class="edit-page-title">
        <h3 class="" v-if="!is_edit">新建主题</h3>
        <h3 class="" v-else>编辑主题</h3>
        <button class="ic-btn click blue right-top-btn" type="primary" :loading="loading" @click="send">{{postButtonText}}</button>
    </div>

    <form class="ic-form" id="form_topic" method="POST" @submit.prevent="send">
        <div class="form-item">
            <input type="text" name="title" v-model="topicInfo.title" placeholder="这里填写标题，最长50个字">
        </div>
        <div class="form-item2">
            <multiselect v-model="topicInfo.board" :options="boardList" :custom-label="getSelectOptionName" placeholder="选择一个板块" label="name" style="z-index: 2" open-direction="bottom" track-by="name"></multiselect>
        </div>
        <div class="form-item">
            <markdown-editor :configs="mdeConfig" v-model="topicInfo.content" placeholder="这里填写内容 ..." rows="15" autofocus></markdown-editor>
        </div>
        <div class="form-item">
            <button class="ic-btn click blue" style="float: right" type="primary" :loading="loading" @click="send">{{postButtonText}}</button>
        </div>
    </form>
</div>
</template>


<style scoped>
#form_topic input[name='title'] {
    padding: 19px 12px;
    width: 100%;
    font-weight: bolder;
    border-radius: 5px;
    box-shadow: none;
    border: 1px solid #e8e8e8;
}

.edit-page-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.edit-page-title > h3 {
}

.right-top-btn {
}

.form-item {
    margin-bottom: 10px;
}

.form-item2 {
    /* 此举是为了避免 ic-form 对 input 的样式覆盖。
        不然select会出现外框套内框这样的事情 */
    margin-bottom: 10px;
}

.el-select > .el-input > input[readonly] {
    background-color: #fff;
    color: #1f2d3d;    
}
</style>

<script>
import _ from 'lodash'
import Prism from 'prismjs'
import Multiselect from 'vue-multiselect'
import 'vue-multiselect/dist/vue-multiselect.min.css'
import markdownEditor from 'vue-simplemde/src/markdown-editor'
import 'simplemde/dist/simplemde.min.css'
import api from '@/netapi.js'
import state from '@/state.js'

export default {
    data () {
        return {
            loading: false,
            boardList: [],

            topicInfo: {
                title: '',
                board: null,
                content: ''
            },

            mdeConfig: {
                spellChecker: false,
                autoDownloadFontAwesome: false,
                autosave: {
                    enabled: false,
                    uniqueId: 'topic-post-content'
                },
                renderingConfig: {
                    singleLineBreaks: false,
                    codeSyntaxHighlighting: false
                },
                previewRender: function (plainText, preview) { // Async method
                    setTimeout(function () {
                        preview.innerHTML = this.parent.markdown(plainText)
                        Prism.highlightAll()
                    }.bind(this), 1)
                    return 'Loading...'
                }
            },

            topicState: state.misc.TOPIC_STATE.NORMAL,
            editing_data: null
        }
    },
    computed: {
        topicStateOptions: function () {
            return Object.entries(state.misc.TOPIC_STATE_TXT)
        },
        is_edit () {
            return this.$route.name === 'topic_edit'
        },
        postButtonText: function () {
            return this.loading ? '请等待'
                : (this.is_edit ? '编辑' : '发布')
        }
    },
    methods: {
        getSelectOptionName ({ name, brief }) {
            return `${name} — [${brief}]`
        },
        send: async function (e) {
            let formdata = new FormData($('#form_topic')[0])
            let title = (formdata.get('title') || '').trim()
            let content = this.editor.value()
            let linkTo = this.link_to
            let topicState = this.topicState

            if (!title) {
                $.message_error('请输入一个标题！')
                return false
            }

            if (title.length < state.data.misc.TITLE_LENGTH_MIN) {
                $.message_error(`标题应不少于 ${state.data.misc.TITLE_LENGTH_MIN} 个字！`)
                return false
            }

            if (title.length > state.data.misc.TITLE_LENGTH_MAX) {
                $.message_error(`标题应不多于 {TITLE_LENGTH_MAX} 个字！`)
                return false
            }

            let postTime = parseInt(this.date.getTime() / 1000)

            // 允许页面内容为空
            // if (!content) return;

            let ret
            let successText
            let failedText

            this.loading = true
            if (this.is_edit) {
                ret = await api.topicEdit(this.$route.params.id, {title, content, time: postTime, linkTo, state: topicState})
                successText = '编辑成功！已自动跳转至文章页面。'
                failedText = ret.msg || '编辑失败！'
            } else {
                ret = await api.topicNew({title, content, time: postTime, linkTo, state: topicState})
                successText = '发表成功！已自动跳转至文章页面。'
                failedText = ret.msg || '编辑失败！'
            }

            if (ret.code === 0) {
                this.editor.toTextArea()
                this.editor = null
                localStorage.setItem('topic-post-cache-clear', 1)
                this.$router.push({name: 'topic', params: { id: ret.data.id }})
                $.message_success(successText)
            } else {
                $.message_error(failedText)
                // 注意：发布成功会跳转，故不做复位，失败则复位
                this.loading = false
            }
        }
    },
    mounted: async function () {
        if (localStorage.getItem('topic-post-cache-clear')) {
            // 我不知道为什么，在地址跳转前进行 storage 的清除工作，
            // 并不会实质上起效，因此这是一个替代手段，效果比较理想。
            localStorage.removeItem('topic-post-title')
            localStorage.removeItem('smde_topic-post-content')
            localStorage.removeItem('topic-post-cache-clear')
        }

        // this.editor = new SimpleMDE({
        //     element: document.getElementById('editor'),
        //     spellChecker: false,
        //     autoDownloadFontAwesome: false,
        //     autosave: {
        //         enabled: true,
        //         uniqueId: "topic-post-content"
        //     },
        //     renderingConfig: {
        //         singleLineBreaks: false,
        //         codeSyntaxHighlighting: false
        //     },
        //     previewRender: function (plainText, preview) { // Async method
        //         setTimeout(function () {
        //             preview.innerHTML = this.parent.markdown(plainText)
        //             Prism.highlightAll()
        //         }.bind(this), 1)
        //         return "Loading..."
        //     }
        // })

        if (this.is_edit) {
            this.editing_data = this.$route.params.editing_data

            let date = new Date()
            date.setTime(this.editing_data.time * 1000)
            this.title = this.editing_data.title
            this.date = date
            this.editor.value(this.editing_data.content)

            // 这么搞有点绕，我忘了当初是为什么，大概只是太菜写的不好
            // 懒得改了
            this.link_to = this.editing_data.link_to
            this.topicState = this.editing_data.state
        } else {
            this.title = localStorage.getItem('topic-post-title') || ''
        }
    },
    watch: {
        'topicInfo.title': _.debounce(function (val, oldVal) {
            localStorage.setItem('topic-post-title', val)
        }, 5000)
    },
    beforeRouteEnter: async (to, from, next) => {
        if (!state.user) {
            $.message_error('抱歉，无权访问此页面')
            return next('/')
        }

        let ret = await api.board.list()
        if (ret.code) {
            $.message_by_code(ret.code)
            return next('/')
        }
        let boardList = ret.data.items

        if (to.name === 'topic_edit') {
            let ret = await api.topicGet(to.params.id)
            if (ret.code) {
                $.message_error('抱歉，发生了错误')
                return next('/')
            }
            to.params.editing_data = ret.data
        }

        next(vm => {
            vm.boardList = boardList
        })
    },
    beforeRouteUpdate: async function (to, from, next) {
        if (!state.user) {
            $.message_error('抱歉，无权访问此页面')
            return next('/')
        }

        let ret = await api.board.list()
        if (ret.code) {
            $.message_by_code(ret.code)
            return next('/')
        }
        let boardList = ret.data.items

        if (to.name === 'topic_edit') {
            let ret = await api.topicGet(to.params.id)
            if (ret.code) {
                $.message_error('抱歉，发生了错误')
                return next('/')
            }
            to.params.editing_data = ret.data
        }

        next(vm => {
            vm.boardList = boardList
        })
    },
    components: {
        Multiselect,
        markdownEditor
    }
}
</script>
