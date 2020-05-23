import baseMarked from 'marked'
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
import 'prismjs/components/prism-ruby.js'
import 'prismjs/components/prism-sql.js'
import 'prismjs/components/prism-nginx.js'
import { atConvertUserPage } from '@/utils/misc'

const renderer = new baseMarked.Renderer()

renderer.code = function (code: string, lang: string, escaped: boolean) {
  if (lang === 'rb') lang = 'ruby'
  if (lang === 'py') lang = 'python'
  if (lang === 'js') lang = 'javascript'

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

  if (!escaped) {
    const langText = this.options.langPrefix + escape(lang)
    return `<pre class="${langText}"><code class="${langText}">` +
        code + '\n</code></pre>\n'
  }

  const langText = this.options.langPrefix + escape(lang)
  return `<pre class="${langText}"><code class="${langText}">` +
        (escaped ? code : escape(code)) +
        '\n</code></pre>\n'
}

// 这是为了在 renderer 中获取 parser 实例继而获得当前 token 所做的 hack
baseMarked.Parser.parse = function (src: any, options: any) {
  const parser = new baseMarked.Parser(options)
  let renderer: any = parser.renderer
  renderer.headingCount = undefined
  renderer._parser = parser
  return parser.parse(src)
}

renderer.heading = function (text: string, level: number, rawtext: string) {
  (this as any).headingCount = (this as any).headingCount ? (this as any).headingCount + 1 : 1

  if (this.options.headerIds) {
    const pf = this.options.headerPrefix
    return `<h${level} id="${pf}${(this as any).headingCount}">${text}</h${level}>\n`
  }

  // ignore IDs
  return '<h' + level + '>' + text + '</h' + level + '>\n'
}

const originIndependentUrl = /^$|^[a-z][a-z0-9+.-]*:|^[?#]/i;

// 为了图片居中以及其他
renderer.image = function (href: string, title: string, text: string) {
  if (this.options.baseUrl && !originIndependentUrl.test(href)) {
    href = (baseMarked as any).resolveUrl(this.options.baseUrl, href)
  }
  let out = '<img src="' + href + '" alt="' + text + '"'
  if (title) {
    out += ' title="' + title + '"'
  }
  out += this.options.xhtml ? '/>' : '>'
  return `<div class="img-center">${out}</div>`
}

const myOpt = {
  renderer: renderer,
  gfm: true,
  tables: true,
  breaks: true,
  sanitize: true,
  smartLists: true,
  smartypants: true,
  headerIds: true,
  headerPrefix: 'til-', // topic index link
  langPrefix: 'language-',
  highlight: function (code: string, lang: string) {
    if (lang) {
      const stdlang = lang.toLowerCase()
      if (Prism.languages[stdlang]) {
        return Prism.highlight(code, Prism.languages[stdlang], stdlang)
      }
    }
  }
}

export function marked (text: string, options: any, callback: any): string {
  // 文章编辑页面的simplemde会覆盖掉marked的设置
  baseMarked.setOptions(myOpt)
  const html: any = baseMarked(text, options, callback) // 这里很奇怪，根据types，这里返回的是void
  return atConvertUserPage(html)
}

export function mdGetIndex (text: string, options: any) {
  if (!text) return []
  const tokens = baseMarked.lexer(text, options)
  const headings = []
  for (const t of tokens) {
    if (t.type === 'heading') {
      headings.push(t)
    }
  }
  return headings
}
