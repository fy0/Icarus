// import { Plugin } from '@nuxt/types'
import { createAPIRequester, APIInterface } from '../api'
import { Context } from '@nuxt/types'

let $api: APIInterface

declare module 'vue/types/vue' {
  interface Vue {
    $api: APIInterface
  }
}

declare module 'vuex/types/index' {
  interface Store<S> {
    $api: APIInterface
  }
}

export default (ctx: Context, inject: any) => {
  const api = createAPIRequester(ctx)
  $api = api
  inject('api', api)
}

export { $api }
