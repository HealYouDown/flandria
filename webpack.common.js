const path = require("path");

const staticPath = __dirname + "/app/static"
const bundlePath = path.join(staticPath, "bundles")

module.exports = {
  entry: "./src/index.js",
  output: {
    path: bundlePath,
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      },
      {
        test: /\.css$/i,
        use: ['style-loader', 'css-loader'],
      }
    ]
  },
  resolve: {
    extensions: ['.js', '.jsx']
  },
}