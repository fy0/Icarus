<template>
  <div>
    <wiki-base v-if="item">
      <article class="box article ic-paper ic-z1">
        <div class="title">
          <span>
            <h1>{{item.title}}</h1>
          </span>
          <span style="font-size: 14px; float: right; text-align: right; flex-shrink: 0;">
            <span class="stat">
              <span class="item" title="阅读次数">
                <i class="icarus icon-eye-outline" />
                <template>{{item.s.click_count}}</template>
              </span>
              <span class="item" title="编辑次数">
                <i class="icarus icon-zidingyi" />
                <template>{{item.s.edit_count}}</template>
              </span>
              <span class="item" title="最后更新时间">
                <i class="icarus icon-time1" />
                <ic-time :timestamp="item.s.update_time" />
              </span>
            </span>
            <div>
              <nuxt-link
                v-if="isWikiAdmin"
                :to="{ name: 'wiki_article_edit', params: {id: item.id}, query: { manage: true } }"
              >[编辑]</nuxt-link>
              <nuxt-link
                :to="{ name: 'wiki_history', params: {id: item.id} }"
                style="margin-left: 5px"
              >[历史]</nuxt-link>
            </div>
          </span>
        </div>
        <div class="ic-hr" style="margin: 10px 0;"></div>
        <div class="content" v-html="marked(item.content || '')"></div>
      </article>
      <div style="margin-left: 10px; font-size: 14px; color: #777"></div>
    </wiki-base>
    <page-not-found v-else />
  </div>
</template>

<style lang="scss" scoped>
.sup {
  font-size: smaller;
  vertical-align: super;
}

.stat > .item {
  margin-left: 15px;

  > i {
    margin-right: 3px;
  }
}

article > .title {
  display: flex;
  position: relative;
  justify-content: space-between;
}

.box {
  background: $white;
  padding: 10px;
  height: 100%;
  height: 100%;
}

.ic-hr {
  margin: 10px 0;
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
    if (params.ref && !/%\w/.test(params.ref)) {
      params.ref = encodeURIComponent(params.ref)
    }

    let ret = await this.$api.wiki.get(
      Object.assign(
        {
          loadfk: { id: { as: 's' } }
        },
        params
      )
    )
    if (ret.code === retcode.SUCCESS) {
      this.item = ret.data
    } else if (ret.code === retcode.NOT_FOUND) {
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
      item: null
    }
  },
  head () {
    if (this.item) {
      return {
        title: `${this.item.title} - 百科`,
        meta: [
          { hid: 'description', name: 'description', content: '百科文章页面' }
        ]
      }
    }
  },
  computed: {
    ...mapState(['config']),
    ...mapGetters('user', ['isWikiAdmin'])
  },
  methods: {},
  created: async function () {},
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
