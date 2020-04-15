// import { Plugin } from '@nuxt/types'
import { createAPIRequester } from '../api/main'

declare module 'vue/types/vue' {
    interface Vue {
        $api: any
    }
}

export default (ctx: any, inject: any) => {
    const api = createAPIRequester(ctx)
    inject('api', api)
}
