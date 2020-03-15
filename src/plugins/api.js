import { createAPIRequester } from '../api/main'

export default (ctx, inject) => {
    const api = createAPIRequester(ctx)
    inject('api', api)
}
