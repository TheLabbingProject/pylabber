const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const VueLoaderPlugin = require('vue-loader/lib/plugin');

module.exports = {
    context: __dirname,
    entry: path.resolve('./static/js/index.js'),
    mode: 'development',
    output: {
        path: path.resolve('./static/bundles/'),
        filename: 'app.js'
    },

    plugins: [
        new BundleTracker({ filename: './webpack-stats.json' }),
        new VueLoaderPlugin(),
    ],

    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                loader: 'babel-loader',
            },
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
            {
                test: /\.styl$/,
                loader: ['style-loader', 'css-loader', 'stylus-loader']
            },
            {
                test: /\.(css|less)$/,
                use: [{
                    loader: "style-loader" // creates style nodes from JS strings
                }, {
                    loader: "css-loader" // translates CSS into CommonJS
                }, {
                    loader: "less-loader" // compiles Less to CSS
                }]
            }
        ],
    },
    resolve: {
        // alias: { vue: 'vue/dist/vue.js' }
        extensions: ['.js', '.vue', '.json'],
        alias: {
            vue: 'vue/dist/vue.js',
            'vue$': 'vue/dist/vue.esm.js',
            '@': path.resolve('src'),
            '__STATIC__': path.resolve('static'),
        }
    },
};
