import marked from 'marked'
import Prism from 'prismjs'
import 'prismjs/themes/prism-tomorrow.css'

import 'prismjs/components/prism-autohotkey.js'
import 'prismjs/components/prism-bash.js'
import 'prismjs/components/prism-batch.js'
import 'prismjs/components/prism-c.js'
import 'prismjs/components/prism-clike.js'
import 'prismjs/components/prism-cpp.js'
import 'prismjs/components/prism-csharp.js'
import 'prismjs/components/prism-css.js'
import 'prismjs/components/prism-css-extras.js'
import 'prismjs/components/prism-git.js'
import 'prismjs/components/prism-glsl.js'
import 'prismjs/components/prism-go.js'
import 'prismjs/components/prism-ini.js'
import 'prismjs/components/prism-java.js'
import 'prismjs/components/prism-javascript.js'
import 'prismjs/components/prism-json.js'
import 'prismjs/components/prism-lua.js'
import 'prismjs/components/prism-markdown.js'
import 'prismjs/components/prism-python.js'
import 'prismjs/components/prism-sql.js'
import 'prismjs/components/prism-nginx.js'

let renderer = new marked.Renderer()

renderer.code = function (code, lang, escaped) {
    if (this.options.highlight) {
        var out = this.options.highlight(code, lang)
        // 这里存在问题，对部分简单代码来说 out == code 是完全可能的
        // 但是 escape 之后代价就是例如空格转换成%20，用户看来是成了乱码
        // if (out != null && out !== code) {
        if (out != null) {
            escaped = true
            code = out
        }
    }

    if (!lang) {
        return `<pre class="${this.options.langPrefix}PLACEHOLDER"><code>` +
            // + (escaped ? code : escape(code, true))
            code + '\n</code></pre>'
    }

    let langText = this.options.langPrefix + escape(lang, true)
    return `<pre class="${langText}"><code class="${langText}">` +
        (escaped ? code : escape(code, true)) +
        '\n</code></pre>\n'
}

marked.setOptions({
    renderer: renderer,
    gfm: true,
    breaks: true,
    sanitize: true,
    langPrefix: 'language-',
    highlight: function (code, lang) {
        if (lang) {
            let stdlang = lang.toLowerCase()
            if (Prism.languages[stdlang]) {
                return Prism.highlight(code, Prism.languages[stdlang])
            }
        }
    }
})

let myMarked = function (text, options, callback) {
    let html = marked(text, options, callback)
    /* eslint-disable no-control-regex */
    return html.replace(/\x01(.+?)\x01/g, '<a href="javascript:userPage(\'$1\')">@$1</a>')
}

export default myMarked
