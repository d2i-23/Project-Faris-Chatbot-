module.exports = {
    // ...other webpack configurations
  
    module: {
      rules: [
        {
          test: /\.tsx?$/,
          use: 'ts-loader',
          exclude: /node_modules/,
        },
      ],
    },
  
    resolve: {
      extensions: ['.tsx', '.ts', '.js'],
      fallback: {
        fs: false,
        path: require.resolve("path-browserify"),
      },
    },
  };