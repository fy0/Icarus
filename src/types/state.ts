export interface StateConfig {
    remote: {
        API_SERVER: string
        WS_SERVER: string
    }
    ws: { enable: boolean }

    siteName: string
    title: string
    logoText: string
}

export interface RootState {
    misc: any
    loading: number
    msgs: Array<string>
    messageId: number
    online: number
    _initing: boolean

    config: StateConfig
}
