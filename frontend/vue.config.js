const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // 后端接口地址
        changeOrigin: true,
        pathRewrite: {
          '^/api': '' // 去掉请求路径中的 /api 前缀
        }
      }
    }
  }
})