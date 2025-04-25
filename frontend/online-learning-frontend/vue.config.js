module.exports = {
    devServer: {
      proxy: {
        // Proxy any request that starts with /api → Django on port 8000
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
          secure: false,
        }
      }
    }
  }