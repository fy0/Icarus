import { SlimSQLAPI } from "slim-tools";

const sentinel = {}

export class SlimCrudAPI extends SlimSQLAPI {
  async list (params: any = {}, page = 1, { size = null, role = sentinel } = {}): Promise<any> {
    params.page = page;
    if (size !== null) {
      params.size = size
    }

    if (params && params.loadfk) {
      params.loadfk = JSON.stringify(params.loadfk)
    }

    let ex: any = { params }
    if (role !== sentinel) { ex.role = role }
    return this.request('/list', 'GET', ex)
  }
}
