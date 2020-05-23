<template>
  <div>
    <wiki-base>
        <!-- <div v-title>全部文章 - 百科 - {{config.title}}</div> -->
        <div class="box ic-paper ic-z1">
            <template v-if="page.items.length === 0">尚无文章</template>
            <template v-else>
                <ul>
                    <li v-for="i in page.items" :key="i.id">
                        <nuxt-link :to="{ name: 'wiki_article_by_ref', params: {'ref': i.ref } }">{{i.title}}</nuxt-link>
                        <nuxt-link v-if="isWikiAdmin" :to="{ name: 'wiki_article_edit', params: {'id': i.id }, query: { manage: true } }" style="margin-left: 10px">[编辑]</nuxt-link>
                    </li>
                </ul>
            </template>
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
</style>

<script>
import { marked } from '@/utils/md.ts'
import WikiBase from './_base.vue'
import { mapState, mapGetters } from 'vuex'
import { BaseWrapper, createFetchWrapper } from '@/fetch-wrap'
import { retcode } from 'slim-tools'

class FetchCls extends BaseWrapper {
  async fetchData () {
    let wrong = false
    let params = this.$route.params
    let pageNumber = params.page || 1

    let ret = await this.$api.wiki.list({
      flag: null,
      order: 'title.asc'
    }, pageNumber, { role: this.basicRole })

    if (ret.code === retcode.SUCCESS) {
      this.page = ret.data
    } else if (ret.code === retcode.NOT_FOUND) {
      this.page.items = []
    } else {
      wrong = ret
    }

    if (wrong) {
      this.$message.byCode(wrong.code)
    }
  }
}

export default {
  data () {
    return {
      marked,
      page: {
        items: []
      }
    }
  },
  head () {
    return {
      title: '文章列表 - 百科',
      meta: [
        { hid: 'description', name: 'description', content: '百科文章列表' }
      ]
    }
  },
  computed: {
    ...mapState(['config']),
    ...mapGetters('user', [
      'basicRole',
      'isWikiAdmin'
    ])
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
