<template>
<loading v-if="pageLoading"/>
<div v-else class="ic-container">
    <div class="edit-page-title">
        <h3 class="" v-if="!is_edit">新建主题</h3>
        <h3 class="" v-else>编辑主题</h3>
        <button class="ic-btn click blue right-top-btn" type="primary" :loading="loading" @click="send">{{postButtonText}}</button>
    </div>

    <form class="ic-form" id="form_topic" method="POST" @submit.prevent="send">
        <check-row :results="formErrors.title" :multi="true">
            <input type="text" name="title" v-model="topicInfo.title" :placeholder="`这里填写标题，${state.misc.TOPIC_TITLE_LENGTH_MIN} - ${state.misc.TOPIC_TITLE_LENGTH_MAX} 字`">
        </check-row>
        <check-row :results="formErrors.board" :multi="true">
            <multiselect v-model="topicInfo.board" :allow-empty="false" :options="boardList" :custom-label="getSelectOptionName" placeholder="选择一个板块" label="name" style="z-index: 2" open-direction="bottom" track-by="name"></multiselect>
        </check-row>
        <check-row :multi="true">
            <markdown-editor :configs="mdeConfig" v-model="topicInfo.content" placeholder="这里填写内容 ..." rows="15" autofocus></markdown-editor>
        </check-row>
        <div class="ic-form-row">
            <button class="ic-btn click blue" style="float: right" type="primary" :loading="loading">{{postButtonText}}</button>
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
/* 这部分内容是动态生成的 因此写在scope中无效 */
.ic-form > .ic-form-row.error > div.markdown-editor > div.editor-toolbar {
    opacity: 1; /* 上下颜色一致 */
    border-color: #FF6060 !important;
}

.ic-form > .ic-form-row.error > .markdown-editor > .cm-s-paper {
    border-left-color: #FF6060 !important;
    border-right-color: #FF6060 !important;
    border-bottom-color: #FF6060 !important;
}

</style>

<script>
import Prism from 'prismjs'
import Multiselect from 'vue-multiselect'
import 'vue-multiselect/dist/vue-multiselect.min.css'
import markdownEditor from 'vue-simplemde/src/markdown-editor'
import 'simplemde/dist/simplemde.min.css'
import api from '@/netapi.js'
import state from '@/state.js'
import CheckRow from '../utils/checkrow.vue'

export default {
    data () {
        return {
            state,
            pageLoading: true,
            loading: false,
            boardList: [],

            topicInfo: {
                title: '',
                board: null,
                content: ''
            },

            formErrors: {
                title: []
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

            topicState: state.misc.TOPIC_STATE.NORMAL
        }
    },
    computed: {
        is_edit () {
            return this.$route.name === 'forum_topic_edit'
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
            let ret
            let successText
            let failedText

            this.loading = true
            this.topicInfo.board_id = this.topicInfo.board.id
            if (this.is_edit) {
                ret = await api.topic.set({id: this.topicInfo.id}, this.topicInfo, 'user')
                successText = '编辑成功！已自动跳转至文章页面。'
                failedText = ret.msg || '编辑失败！'
            } else {
                ret = await api.topic.new(this.topicInfo, 'user')
                successText = '发表成功！已自动跳转至文章页面。'
                failedText = ret.msg || '新建失败！'
            }

            if (ret.code === 0) {
                localStorage.setItem('topic-post-cache-clear', 1)
                this.$router.push({name: 'forum_topic', params: { id: this.topicInfo.id }})
                $.message_success(successText)
            } else {
                $.message_error(failedText)
                // 注意：发布成功会跳转，故不做复位，失败则复位
                this.loading = false
            }
        },
        fetchData: async function () {
            this.pageLoading = true
            let params = this.$route.params

            if (!state.user) {
                $.message_error('抱歉，无权访问此页面，请返回')
                return
            }

            let ret = await api.board.list()
            if (ret.code) {
                $.message_by_code(ret.code)
                return
            }
            let boardList = ret.data.items

            if (this.is_edit) {
                let ret = await api.topic.get({
                    id: params.id,
                    loadfk: {user_id: null, board_id: null}
                })
                if (ret.code) {
                    $.message_error('抱歉，发生了错误')
                    return
                }
                this.topicInfo = ret.data
            }

            this.boardList = boardList
            if (boardList.length) this.topicInfo.board = boardList[0]

            this.pageLoading = false
        }
    },
    mounted: async function () {
        // if (localStorage.getItem('topic-post-cache-clear')) {
        //     // 我不知道为什么，在地址跳转前进行 storage 的清除工作，
        //     // 并不会实质上起效，因此这是一个替代手段，效果比较理想。
        //     localStorage.removeItem('topic-post-title')
        //     localStorage.removeItem('smde_topic-post-content')
        //     localStorage.removeItem('topic-post-cache-clear')
        // }

        if (!this.is_edit) {
            // this.title = localStorage.getItem('topic-post-title') || ''
        }
    },
    created () {
        this.fetchData()
    },
    watch: {
        'topicInfo.title': _.debounce(function (val, oldVal) {
            localStorage.setItem('topic-post-title', val)
        }, 5000)
    },
    components: {
        CheckRow,
        Multiselect,
        markdownEditor
    }
}
</script>
