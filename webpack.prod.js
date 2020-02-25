const merge = require("webpack-merge");
const common = require("./webpack.common");
const CompressionPlugin = require("compression-webpack-plugin");
const RemovePlugin = require("remove-files-webpack-plugin");

module.exports = merge(common, {
  output: {
    filename: "[hash].bundle.js",
  },
  mode: "production",
  devtool: "(none)",
  plugins: [
    new CompressionPlugin({
      filename: "[path].gz",
      algorithm: "gzip",
      test: /\.js(\?.*)?$/i,
      threshold: 10240,
      minRatio: 0.8
    }),
    new RemovePlugin({
      before: {
        include: [common.output.path],
      }
    })
  ]
})
