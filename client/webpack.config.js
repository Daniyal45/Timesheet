const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const TerserPlugin = require('terser-webpack-plugin');

module.exports = {
  mode: 'development',  
  entry: './src/index.js',
  devtool: 'inline-source-map',
  plugins: [        
         new HtmlWebpackPlugin({
           title: 'Timesheet',
           filename: "main.html"
         })
       ],
  output: {    
    filename: 'timesheet.js',
    path: path.resolve(__dirname, './dist')
  },
  module: {
         rules: [
           {
             test: /\.css$/,
             use: [
               'style-loader',
               'css-loader'
             ]
           },
           //Load Images
           {
                     test: /\.(png|svg|jpg|gif)$/,
                     use: [
                       {
                        loader: 'file-loader',
                        options: {
                          outputPath: './react_assets',
                        },
                      }
                     ]
            },
           // Load Font
            {
                     test: /\.(woff|woff2|eot|ttf|otf)$/,
                     use: [
                       {
                        loader: 'file-loader',
                        options: {
                          outputPath: './react_assets',
                        },
                      }
                     ]
            },
            //load react jsx
            {
              test: /\.(js|jsx)$/,
              exclude: /node_modules/,
              use: {
                loader: "babel-loader"
              }
            }
         ]
       },
	optimization: {
		minimize: true,
		minimizer: [
		  new TerserPlugin({
			parallel: true,
			cache: true,
			terserOptions: {
			  output: {
				comments: false,
			  },
			},
		  }),
		],
	  },	
};
