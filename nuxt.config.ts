const path = require('path')
const pkg = require('./package')
const webpack = require('webpack')
const mm = require('micromatch')

export default {
  // mode: 'universal',
  srcDir: './src/',
  env: {},
  head: {
    title: pkg.name,
    meta: [
      { charset: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { hid: "description", name: "description", content: pkg.description }
    ],
    link: [
      { rel: "icon", type: "image/x-icon", href: "/favicon.ico" }
    ]
  },
  loading: { color: "#3397dc" },

  /*
  ** Global CSS
  */
  css: [
      // '@/assets/css/variables.scss',
      // '@/assets/css/input.scss'
  ],

  /** middleware */
  serverMiddleware: [
    {
      handler: function (req: any, res: any, next: any) {
        // 注：此处从简，因为例如/search*明显匹配了更多url，但并非关键
        const spaPaths = [
          '/account/**',
          '/notifications',
          '/notifications*',
          '/notifications/**',
          '/admin/**',
          '/wiki/new',
          '/wiki/new*',
          '/wiki/edit/**',
          '/setting/**',
          '/search*',
          '/search/**'
        ]
        if (mm.some(req._parsedUrl.pathname, spaPaths)) {
          res.spa = true
        }
        next()
      }
    }
  ],

  /** middleware */
  router: {
    middleware: ['router-guards']
  },

  /*
  ** Plugins to load before mounting the App
  */
  plugins: [
    '@/plugins/index',
    '@/plugins/helpers',
    '@/plugins/api',
    '@/plugins/message'
  ],

  /*
  ** Nuxt.js modules
  */
  modules: [
    '@nuxtjs/router',
    '@nuxtjs/style-resources',
    '@nuxtjs/universal-storage'
  ],
  buildModules: ["@nuxt/typescript-build"],
  storage: {
  },
  styleResources: {
    scss: [
      '@/assets/css/variables.scss',
      '@/assets/css/response.scss',
      '@/assets/css/input.scss'
    ]
  },

  build: {
    plugins: [
      new webpack.ProvidePlugin({
        _: path.resolve(__dirname, './src/utils/lodash.ts')
      }),
      new webpack.ProvidePlugin({
        $: path.resolve(__dirname, './src/tools/_merge.js')
      })
    ]
  },
  axios: {}
}
