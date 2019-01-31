const path = require('path')
const pkg = require('./package')
const webpack = require('webpack')
const mm = require('micromatch')

module.exports = {
    mode: 'universal',
    srcDir: 'src/',

    /*
    ** Headers of the page
    */
    head: {
        title: pkg.name,
        meta: [
            { charset: 'utf-8' },
            { name: 'viewport', content: 'width=device-width, initial-scale=1' },
            { hid: 'description', name: 'description', content: pkg.description }
        ],
        link: [
            { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
        ]
    },

    /*
    ** Customize the progress-bar color
    */
    loading: { color: '#fff' },

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
            handler: function (req, res, next) {
                let spaPaths = [
                    '/account/**',
                    'notifications',
                    '/admin/**'
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
        '@/plugins/_main',
        '@/plugins/helpers',
        '@/plugins/api'
    ],

    /*
    ** Nuxt.js modules
    */
    modules: [
        '@nuxtjs/router',
        'nuxt-sass-resources-loader',
        'nuxt-universal-storage'
    ],
    storage: {
    },
    sassResources: [
        '@/assets/css/variables.scss',
        '@/assets/css/input.scss'
    ],

    /*
    ** Build configuration
    */
    build: {
        /*
        ** You can extend webpack config here
        */
        postcss: {
            plugins: {
                autoprefixer: {}
            }
        },

        plugins: [
            new webpack.ProvidePlugin({
                '_': path.resolve(__dirname, './src/tools/lodash.js')
            }),
            new webpack.ProvidePlugin({
                '$': path.resolve(__dirname, './src/tools/_merge.js')
            })
        ],

        extend (config, ctx) {
            // Run ESLint on save
            if (ctx.isDev && ctx.isClient) {
                config.module.rules.push({
                    enforce: 'pre',
                    test: /\.(js|vue)$/,
                    loader: 'eslint-loader',
                    exclude: /(node_modules)/
                })
            }
        }
    }
}
