
const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const DashboardPlugin = require('webpack-dashboard/plugin');
const CompressionWebpackPlugin = require('compression-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

const extractCSS = new ExtractTextPlugin('style/[name].css');
const extractLESS = new ExtractTextPlugin('style/[name]-less.css');
const extractSASS = new ExtractTextPlugin('style/[name]-sass.css');


module.exports = {
	target: 'web',
	entry: {
		app: './src/main.js',
		// vendor: ['handsontable', 'jquery', 'highcharts', 'vue', 'bootstrap', 'lodash',
		// 	'vue-router', 'sockjs-client', 'socket.io-client', 'html-entities', 'buffer',
		// 	'json3'],
	},
	output: {
		path: path.resolve(__dirname, './dist/assets'),
		publicPath: '/assets/',
		filename: '[name].js' //[hash].[name]
	},
	module: {
		rules: [
			{
				test: /\.vue$/,
				loader: 'vue-loader',
				options: {
					// vue-loader options go here
				}
			},
			{
				test: /\.js$/,
				loader: 'babel-loader',
				exclude: /node_modules/
			},
			{
				test: /\.css$/,
				// use: ['style-loader', 'css-loader'],
				// use: extractCSS.extract(['css-loader', 'postcss-loader'])
				use: extractCSS.extract(['css-loader'])
			},
			{
				test: /\.less$/,
				// use: ['style-loader', 'css-loader', 'less-loader'],
				use: extractLESS.extract(['css-loader', 'less-loader'])
			},
			{
				test: /\.(sass|scss)$/,
				// use: ['style-loader', 'css-loader', 'sass-loader']
				use: extractSASS.extract(['css-loader', 'sass-loader'])
			},
			{
				test: /\.(woff|woff2|ttf|eot|svg)?(\?v=[0–9]\.[0–9]\.[0–9])?$/,
				loader: 'file-loader',
				options: {
					name: 'font/[name].[ext]?[hash]'
				}
			},
			{
				test: /\.(png|jpe?g|gif)?(\?v=[0–9]\.[0–9]\.[0–9])?$/,
				loader: 'file-loader',
				options: {
					name: 'img/[name].[ext]?[hash]'
				}
			},
			// {
			// 	// I want to uglify with mangling only app files, not thirdparty libs
			// 	// test: /.*\/app\/.*\.js$/,
			// 	test: /\.js$/,
			// 	// exclude: /.spec.js/, // excluding .spec files
			// 	loader: "uglify-loader"
			// },
		],
	},
	plugins: [
		extractCSS,
		extractLESS,
		extractSASS,
		new webpack.ProvidePlugin({
			// '$': 'jquery',
			// 'jquery': 'jquery',
			'jQuery': 'jquery',
		}),
		new HtmlWebpackPlugin({
			favicon: './src/img/favicon.ico'
		}),
		// new webpack.optimize.CommonsChunkPlugin({
		// 	names: ['vendor']
		// }),
	],
	resolve: {
		alias: {
			'vue$': 'vue/dist/vue'
		}
	},
	devServer: {
		historyApiFallback: true,
		noInfo: true
	},
	devtool: '#eval-source-map'
};

if (process.env.NODE_ENV === 'development') {
	module.exports.plugins = (module.exports.plugins || []).concat([
		new DashboardPlugin(),
	]);
}


if (process.env.NODE_ENV === 'production') {
	module.exports.devtool = '#source-map';
	// http://vue-loader.vuejs.org/en/workflow/production.html
	module.exports.plugins = (module.exports.plugins || []).concat([
		new webpack.DefinePlugin({
			'process.env': {
				NODE_ENV: '"production"'
			}
		}),
		new webpack.optimize.UglifyJsPlugin({
			compress: {
				warnings: false
			}
		}),
		new webpack.LoaderOptionsPlugin({
			minimize: true
		}),
		new CompressionWebpackPlugin({
			asset: '[path].gz[query]',
			algorithm: 'gzip',
			test: new RegExp(
				'\\.(' +
				['js', 'css'].join('|') +
				')$'
			),
			threshold: 10240,
			minRatio: 0.8
		}),
		// generate dist index.html with correct asset hash for caching.
		// you can customize output by editing /index.html
		// see https://github.com/ampedandwired/html-webpack-plugin
		new HtmlWebpackPlugin({
			filename: path.resolve(__dirname, './dist/index.html'),
			template: 'src/top.html',
			inject: true,
			minify: {
				removeComments: true,
				collapseWhitespace: true,
				removeAttributeQuotes: true
				// more options:
				// https://github.com/kangax/html-minifier#options-quick-reference
			},
			// necessary to consistently work with multiple chunks via CommonsChunkPlugin
			chunksSortMode: 'dependency'
		}),
	]);
}

