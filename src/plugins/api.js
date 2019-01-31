// import Vue from 'vue'
import { createAPIRequester } from '@/netapi'

export default (ctx, inject) => {
    let api = createAPIRequester(ctx)
    inject('api', api)
}
