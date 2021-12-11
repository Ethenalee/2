const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = (app) => {
	app.use(
		['/v1/rushingrecords'],
		createProxyMiddleware({
			target: process.env.REACT_APP_PROXY_HOST,
			changeOrigin: true,
		}),
	);
};
