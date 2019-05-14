// Added trying to follow this tutorial:
// https://medium.com/@michealjroberts/part-1-integrating-django-2-vue-js-and-hot-webpack-reload-setup-387a975166d3
module.exports = {
    dev: {
        assetsSubDirectory: 'static',
        assetsPublicPath: 'http://localhost:8080/',
        proxyTable: {},
    },
    build: {
        assetsRoot: path.resolve(__dirname, '../dist/'),
        assetsSubDirectory: '',
        assetsPublicPath: '/static/',
    },
}