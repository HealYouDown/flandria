const merge = require("webpack-merge");
const common = require("./webpack.common");

module.exports = merge(common, {
  output: {
    filename: "bundle.js"
  },
  mode: "development",
  optimization: {
    minimize: false,
  }
})