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

    app.use(createProxyMiddleware("/*/aims", {
        target: 'http://localhost:5000',
        changeOrigin: true
    }));

    app.use(createProxyMiddleware("/*/set_def_hum", {
        target: 'http://localhost:5000',
        changeOrigin: true
    }));

    app.use(createProxyMiddleware("/*/set_def_temp", {
        target: 'http://localhost:5000',
        changeOrigin: true
    }));

    app.use(createProxyMiddleware("/*/delete_temp_schedule", {
        target: 'http://localhost:5000',
        changeOrigin: true
    }));

    app.use(createProxyMiddleware("/*/delete_hum_schedule", {
        target: 'http://localhost:5000',
        changeOrigin: true
    }));

    app.use(createProxyMiddleware("/*/add_temp_schedule", {
        target: 'http://localhost:5000',
        changeOrigin: true
    }));

    app.use(createProxyMiddleware("/*/add_hum_schedule", {
        target: 'http://localhost:5000',
        changeOrigin: true
    }));
};