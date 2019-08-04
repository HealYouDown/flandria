const merge = require('webpack-merge');
const common = require('./webpack.common.js');
const CompressionPlugin = require('compression-webpack-plugin');
const path = require('path');
const fs = require('fs');

// Clears output folder from all previous things except folders
const outputDir = common.output.path;
fs.readdirSync(outputDir).forEach(filename => {
  const filenamePath = path.join(outputDir, filename)
  if (!fs.lstatSync(filenamePath).isDirectory()) {
    fs.unlinkSync(filenamePath);
  }
});

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