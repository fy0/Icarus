<template>
  <div>
    <wiki-base>
        <div class="box ic-paper ic-z1">
            <div class="title">
                <h1>[历史记录]{{article.title}}</h1>
                <span style="font-size: 14px; float: right; text-align: right; flex-shrink: 0;">
                    <div v-if="article.ref">
                        <nuxt-link :to="{ name: 'wiki_article_by_ref', params: {ref: article.ref} }" style="margin-left: 5px">[返回原文]</nuxt-link>
                    </div>
                </span>
            </div>
            <div class="ic-hr" style="margin: 10px 0;"></div>
            <ul v-if="page.items && page.items.length">
                <li v-for="i in page.items" :key="i.id">
                    <span>
                        <user-link :user="i.user_id" /> 对此文章进行了<b>{{MANAGE_OPERATION_TXT[i.operation]}}</b>操作 - <ic-time :timestamp="i.time" />
                        <!-- <pre>{{i.value}}</pre> -->
                    </span>
                </li>
            </ul>
            <div v-else>尚无历史记录</div>
            <page-not-found v-if="notFound" />
        </div>
    </wiki-base>
  </div>
</template>

<style lang="scss" scoped>
.box {
  background: $white;
  padding: 10px;
  height: 100%;
}

.title {
  display: flex;
  position: relative;
  justify-content: space-between;
}
</style>

<script>
import { mapState, mapGetters } from 'vuex'
import { marked } from '@/utils/md.ts'
import WikiBase from './_base.vue'
import { BaseWrapper, createFetchWrapper } from '@/fetch-wrap'
import { retcode } from 'slim-tools'

class FetchCls extends BaseWrapper {
  async fetchData () {
    let wrong = false
    let params = this.$route.params
    let pageNumber = params.page || 1

    let getArticle = async () => {
      let ret = await this.$api.wiki.get({
        id: params.id,
        select: ['id', 'title', 'ref']
      }, { role: this.basicRole })
      if (ret.code === retcode.SUCCESS) {
        this.article = ret.data
      } else if (ret.code === retcode.NOT_FOUND) {
        this.notFound = true
      } else {
        wrong = ret
      }
    }

    let getHistory = async () => {
      let ret = await this.$api.logManage.list({
        related_id: params.id,
        order: 'time.desc',
        loadfk: { 'user_id': null }
      }, pageNumber, { role: this.basicRole })

      if (ret.code === retcode.SUCCESS) {
        this.page = ret.data
      } else if (ret.code === retcode.NOT_FOUND) {
        this.page.items = []
      } else {
        wrong = ret
      }
    }

    await Promise.all([getHistory(), getArticle()])
    if (wrong) {
      this.$message.byCode(wrong.code)
    }
  }
}

export default {
  data () {
    return {
      marked,
      notFound: false,
      article: {},
      page: {
        items: []
      }
    }
  },
  head () {
    return {
      title: `[历史记录]${this.article.title} - 百科`,
      meta: [
        { hid: 'description', name: 'description', content: '百科文章编辑历史' }
      ]
    }
  },
  computed: {
    ...mapState(['config']),
    ...mapGetters(['MANAGE_OPERATION_TXT']),
    ...mapGetters('user', ['basicRole'])
  },
  methods: {
  },
  created: async function () {
  },
  async asyncData (ctx) {
    let f = createFetchWrapper(FetchCls, ctx)
    await f.fetchData()
    return f._data
  },
  components: {
    WikiBase
  }
}
</script>
