// import Vue from 'vue'
import { createAPIRequester } from '@/netapi'

export default (ctx, inject) => {
    const api = createAPIRequester(ctx)
    inject('api', api)
}
