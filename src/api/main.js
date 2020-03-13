import { TokenStoreNuxt, newRequestClient, SlimSQLAPI } from 'slim-tools/build/main'
import config from '@/config'
import { retcode, retinfo } from './misc'
import { UserAPI, NotifAPI, UploadAPI, SearchAPI, WikiAPI } from './apis'

let client = newRequestClient(config.remote.API_SERVER)

export function createAPIRequester (ctx) {
    let ts = new TokenStoreNuxt(ctx)

    return {
        retcode,
        retinfo,
        accessToken: null, // 需在初始化时进行设置

        /** 获取综合信息 */
        misc: async function () {
            return client.request('/api/misc/info', 'GET')
        },

        /** 周期请求 */
        tick: async function (auid) {
            return client.request('/api/misc/tick', 'GET', { params: { auid } })
        },

        user: new UserAPI(client, ts, '/api/user'),
        board: new SlimSQLAPI(client, ts, '/api/board'),
        topic: new SlimSQLAPI(client, ts, '/api/topic'),
        stats: new SlimSQLAPI(client, ts, '/api/stats'),
        comment: new SlimSQLAPI(client, ts, '/api/comment'),
        notif: new NotifAPI(client, ts, '/api/notif'),
        upload: new UploadAPI(client, ts, '/api/upload'),
        logManage: new SlimSQLAPI(client, ts, '/api/log/manage'),
        wiki: new WikiAPI(client, ts, '/api/wiki'),
        search: new SearchAPI(client, ts, '/api/search')
    }
}
