var WebpackBeforeBuildPlugin = require('before-build-webpack');
const path = require('path');
const fs = require('fs')

module.exports = {
  entry: {
    app: "./src/index.js"
  },
  plugins: [
    new WebpackBeforeBuildPlugin(function(stats, callback) {
      // Clears output folder from all previous things except folders
      const outputDir = __dirname + "/app/static";
      fs.readdirSync(outputDir).forEach(filename => {
        const filenamePath = path.join(outputDir, filename)
        if (!fs.lstatSync(filenamePath).isDirectory()) {
          fs.unlinkSync(filenamePath);
        }
      });
      callback();
    }),
  ],
  output: {
    path: __dirname + "/app/static",
    filename: "[hash].bundle.js",
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: ['babel-loader']
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      }
    ]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx']
  },
}