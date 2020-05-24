<template>
  <div>
    <wiki-base>
        <article class="box article ic-paper ic-z1">
            <div class="content" v-html="marked(mainpage.content || '')"></div>
        </article>
    </wiki-base>
  </div>
</template>

<style lang="scss" scoped>
.box {
  background: $white;
  height: 100%;
  padding: 10px;
}
</style>

<script>
import { mapState } from 'vuex'
import { marked } from '@/utils/md.ts'
import WikiBase from './_base.vue'
import { BaseWrapper, createFetchWrapper } from '@/fetch-wrap'
import { retcode } from 'slim-tools'

class FetchCls extends BaseWrapper {
  async fetchData () {
    let wrong = false

    let ret = await this.$api.wiki.get({
      flag: 2
    }, { role: this.$user.basicRole })

    if (ret.code === retcode.SUCCESS) {
      this.mainpage = ret.data
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
      mainpage: {}
    }
  },
  head () {
    return {
      title: '百科',
      meta: [
        { hid: 'description', name: 'description', content: '百科' }
      ]
    }
  },
  computed: {
    ...mapState(['config'])
  },
  methods: {
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
