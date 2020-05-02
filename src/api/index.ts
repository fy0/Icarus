import { TokenStoreNuxt, newRequestClient, SlimSQLAPI } from 'slim-tools'
import config from '@/config'
import { UserAPI, NotifAPI, UploadAPI, SearchAPI, WikiAPI, MiscAPI } from './apis'
import { Context } from '@nuxt/types'
import { AxiosResponse } from 'axios'

let client = newRequestClient(config.remote.API_SERVER)

export interface APIInterface {
  // misc: MiscAPI,
  misc: any,
  tick: any,
  getDefaultRole: any,
  // misc: Promise<AxiosResponse<any>>,
  // tick: Promise<AxiosResponse<any>>,
  saveAccessToken: any, // function

  user: UserAPI,
  board: SlimSQLAPI,
  topic: SlimSQLAPI,
  stats: SlimSQLAPI,
  comment: SlimSQLAPI,
  notif: NotifAPI,
  upload: UploadAPI,
  logManage: SlimSQLAPI,
  wiki: WikiAPI,
  search: SearchAPI
}

export function createAPIRequester (ctx: Context): APIInterface {
  let ts = new TokenStoreNuxt(ctx)

  let getRole = () => {
    return data.getDefaultRole()
  }

  let data = {
    getDefaultRole: () => {},

    /** 获取综合信息 */
    misc: async function () {
      let token = ts.getAccessToken()
      let headers: any = {}
      if (token) headers['AccessToken'] = token
      return client.request({ url: '/api/misc/info', method: 'GET', headers })
    },

    /** 周期请求 */
    tick: async function (auid: string) {
      let token = ts.getAccessToken()
      let headers: any = {}
      if (token) headers['AccessToken'] = token
      return client.request({ url: '/api/misc/tick', method: 'GET', headers })
    },

    saveAccessToken (t: string) {
      ts.saveAccessToken(t)
    },

    // misc: new MiscAPI(client, ts, '/api/misc', getRole),
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
