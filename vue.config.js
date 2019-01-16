const path = require('path')
const webpack = require('webpack')

module.exports = {
    baseUrl: undefined,
    outputDir: undefined,
    assetsDir: undefined,
    runtimeCompiler: undefined,
    productionSourceMap: false,
    parallel: undefined,
    configureWebpack: {
        plugins: [
            new webpack.ProvidePlugin({
                '_': path.resolve(__dirname, './src/tools/lodash.js')
            }),
            new webpack.ProvidePlugin({
                '$': path.resolve(__dirname, './src/tools/_merge.js')
            })
        ]
    },
    css: {
        loaderOptions: {
            sass: {
                data: '@import "@/assets/css/variables.scss"; @import "@/assets/css/input.scss";'
            }
        }
    }
}
