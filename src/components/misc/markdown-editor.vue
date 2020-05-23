<!--
based on vue-simplemde
license: https://github.com/F-loat/vue-simplemde/blob/master/LICENSE
-->

<template>
<div class="markdown-editor">
    <textarea></textarea>
</div>
</template>

<script>
import { marked } from '@/utils/md.ts'
import Prism from 'prismjs'
// import SimpleMDE from 'easymde/src/js/easymde.js'
import 'easymde/dist/easymde.min.css'

// SimpleMDE.prototype.markdown = function (text) {
//     return marked(text)
// }

export default {
  name: 'markdown-editor',
  props: {
    value: String,
    previewClass: String,
    autoinit: {
      type: Boolean,
      default: true
    },
    highlight: {
      type: Boolean,
      default: false
    },
    configs: {
      type: Object,
      default () {
        return {}
      }
    }
  },
  mounted () {
    if (this.autoinit) this.initialize()
  },
  activated () {
    const editor = this.simplemde
    if (!editor) return
    const isActive = editor.isSideBySideActive() || editor.isPreviewActive()
    if (isActive) editor.toggleFullScreen()
  },
  methods: {
    initialize () {
      let SimpleMDE = require('easymde/src/js/easymde.js')

      SimpleMDE.prototype.markdown = function (text) {
        return marked(text)
      }

      const configs = Object.assign({
        element: this.$el.firstElementChild,
        initialValue: this.value,
        renderingConfig: {}
      }, {
        spellChecker: false,
        autoDownloadFontAwesome: false,
        placeholder: '这里填写内容，支持 Markdown 格式。\n支持图片上传（GIF除外），可通过拖拽或粘贴进行上传，大小限制5MB。',
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
      })
      // 同步 value 和 initialValue 的值
      if (configs.initialValue) {
        this.$emit('input', configs.initialValue)
      }
      // 判断是否开启代码高亮
      if (this.highlight) {
        configs.renderingConfig.codeSyntaxHighlighting = true
      }
      // 设置是否渲染输入的html
      // marked.setOptions({ sanitize: this.sanitize })
      // 实例化编辑器
      this.simplemde = new SimpleMDE(configs)
      // 添加自定义 previewClass
      const className = this.previewClass || ''
      this.addPreviewClass(className)
      // 绑定事件
      this.bindingEvents()
    },
    bindingEvents () {
      this.simplemde.codemirror.on('change', () => {
        this.$emit('input', this.simplemde.value())
      })
    },
    addPreviewClass (className) {
      const wrapper = this.simplemde.codemirror.getWrapperElement()
      const preview = document.createElement('div')
      wrapper.nextSibling.className += ` ${className}`
      preview.className = `editor-preview ${className}`
      wrapper.appendChild(preview)
    }
  },
  destroyed () {
    this.simplemde = null
  },
  watch: {
    value (val) {
      if (val === this.simplemde.value()) return
      this.simplemde.value(val)
    }
  }
}
</script>

<style>
.markdown-editor .markdown-body {
    padding: 0.5em
}
.markdown-editor .editor-preview-active, .markdown-editor .editor-preview-active-side {
    display: block;
}
</style>
