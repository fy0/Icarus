import { TokenStoreNuxt, newRequestClient, SlimSQLAPI } from 'slim-tools'
import config from '@/config'
import { retcode, retinfo } from './misc'
import { UserAPI, NotifAPI, UploadAPI, SearchAPI, WikiAPI } from './apis'

let client = newRequestClient(config.remote.API_SERVER)

export function createAPIRequester (ctx) {
    let ts = new TokenStoreNuxt(ctx)

    let getRole = () => {
        return data.getDefaultRole()
    }

    let data = {
        retcode,
        retinfo,
        getDefaultRole: () => {},

        /** 获取综合信息 */
        misc: async function () {
            let token = ts.getAccessToken()
            let headers = {}
            if (token) headers['AccessToken'] = token
            return client.request({ url: '/api/misc/info', method: 'GET', headers })
        },

        /** 周期请求 */
        tick: async function (auid) {
            let token = ts.getAccessToken()
            let headers = {}
            if (token) headers['AccessToken'] = token
            return client.request({ url: '/api/misc/tick', method: 'GET', headers })
        },

        saveAccessToken (t) {
            ts.saveAccessToken(t)
        },

        user: new UserAPI(client, ts, '/api/user', getRole),
        board: new SlimSQLAPI(client, ts, '/api/board', getRole),
        topic: new SlimSQLAPI(client, ts, '/api/topic', getRole),
        stats: new SlimSQLAPI(client, ts, '/api/stats', getRole),
        comment: new SlimSQLAPI(client, ts, '/api/comment', getRole),
        notif: new NotifAPI(client, ts, '/api/notif', getRole),
        upload: new UploadAPI(client, ts, '/api/upload', getRole),
        logManage: new SlimSQLAPI(client, ts, '/api/log/manage', getRole),
        wiki: new WikiAPI(client, ts, '/api/wiki', getRole),
        search: new SearchAPI(client, ts, '/api/search', getRole)
    }

    return data
}
