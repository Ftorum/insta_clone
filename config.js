const webpack = require("webpack")

module.exports = {
    entry: './src/js/index.js',
    mode: 'development',
    output: {
        filename: 'index.js',
        path: '/Users/anton/anagram/insta/to_git/config/static/js'
    },
    module: {
        rules:[
            {
                test:/\.(sass|less|css|scss)$/,
                use:['style-loader', 'css-loader', 'sass-loader',],
                
            }
        ]
    },
    plugins: [
        new webpack.ProvidePlugin({
          $: 'jquery',
          jQuery: 'jquery'
        }),
      ]
};
