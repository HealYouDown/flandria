const merge = require('webpack-merge');
const common = require('./webpack.common.js');
const CompressionPlugin = require('compression-webpack-plugin');

module.exports = merge(common, {
  mode: "production",
  devtool: "(none)",
  plugins: [
    new CompressionPlugin({
      filename: '[path].gz',
      algorithm: "gzip",
      test: /\.js(\?.*)?$/i,
      threshold: 10240,
      minRatio: 0.8
    })
  ]
})