<template>
  <div>
    <wiki-base v-if="nothing">
        <div class="box ic-paper ic-z1" >
            <template v-if="nothing">无处可去</template>
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
import { retcode } from 'slim-tools'

export default {
  data () {
    return {
      marked,
      nothing: true
    }
  },
  head () {
    return {
      title: '随便看看 - 百科',
      meta: [
        { hid: 'description', name: 'description', content: '百科' }
      ]
    }
  },
  methods: {
    fetchData: async function () {
      let ret = await this.$api.wiki.random()
      if (ret.code === retcode.SUCCESS) {
        this.nothing = false
        this.$nextTick(() => {
          this.$router.replace({
            name: 'wiki_article_by_ref',
            params: { ref: ret.data.ref }
          })
        })
      }
    }
  },
  created: async function () {
    // this.$store.commit('LOADING_INC', 1)
    await this.fetchData()
    // this.$store.commit('LOADING_DEC', 1)
  },
  components: {
    WikiBase
  }
}
</script>
