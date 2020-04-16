
export interface ConfigInfo {
  remote: {
    API_SERVER: string,
    WS_SERVER: string
  },
  ws?: {
    enable: boolean
  },

  siteName?: string,
  title?: string,
  logoText?: string
}
