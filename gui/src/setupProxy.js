const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function (app) {
    app.use(createProxyMiddleware("/roomnames", {
        target: 'http://localhost:5000',
        changeOrigin: true,
    }));

    app.use(createProxyMiddleware("/*/current", {
        target: 'http://localhost:5000',
        changeOrigin: true
    }));

    app.use(createProxyMiddleware("/*/data", {
        target: 'http://localhost:5000',
        changeOrigin: true
    }))
};