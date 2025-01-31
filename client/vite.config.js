// const IS_PRODUCTION = process.env.NODE_ENV === 'production'

import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import ViteBabelPlugin from 'vite-plugin-babel';
import eslintPlugin from 'vite-plugin-eslint';
import Components from 'unplugin-vue-components/vite';
import {BootstrapVueNextResolver} from 'bootstrap-vue-next';
import { fileURLToPath, URL } from "url";

export default defineConfig({
  plugins: [
    vue(),
    ViteBabelPlugin({
      presets: ['@babel/preset-env'],
      plugins: [
        ['@babel/plugin-transform-runtime', {
          corejs: 3,
          helpers: true,
          regenerator: true,
          useESModules: true,
        }]
      ],
      babelHelpers: 'runtime'
    }),
    Components({
      resolvers: [BootstrapVueNextResolver()],
    }),
    // eslintPlugin({
    //  failOnError: false, // Not stop the server when there is an ESLint error
    //  failOnWarning: false,
    //  include: ['src/**/*.js', 'src/**/*.vue']
    // }),
  ],
  //base: '/',
  resolve: {
    alias: [
      //'@': '/src', // Alias for imports
      //'@': path.resolve(__dirname, './src')
      { find: '@', replacement: fileURLToPath(new URL('./src', import.meta.url)) },
      //{ find: '@assets', replacement: fileURLToPath(new URL('./src/shared/assets', import.meta.url)) },
      //{ find: '@cmp', replacement: fileURLToPath(new URL('./src/shared/cmp', import.meta.url)) },
      //{ find: '@stores', replacement: fileURLToPath(new URL('./src/shared/stores', import.meta.url)) },
      //{ find: '@use', replacement: fileURLToPath(new URL('./src/shared/use', import.meta.url)) },
    ],
  },
  optimizeDeps: {
    include: ['@babel/runtime/helpers/interopRequireDefault']
  },
  server: {
    port: 8091,
    proxy: {
      '/api': {
        target: 'http://localhost:8090',
        changeOrigin: true
      }
    }
  },
  build: {
    outDir: 'dist',
    assetsDir: 'static',
    rollupOptions: {
      output: {
        assetFileNames: 'static/[name]-[hash][extname]',
        chunkFileNames: 'js/[name]-[hash].js',
        entryFileNames: 'js/[name]-[hash].js'
      }
    }
  }
});

// module.exports = {
//   outputDir: 'dist',
//   assetsDir: 'static',
//   // baseUrl: IS_PRODUCTION
//   // ? 'http://cdn123.com'
//   // : '/',
//   // For Production, replace set baseUrl to CDN
//   // And set the CDN origin to `yourdomain.com/static`
//   // Whitenoise will serve once to CDN which will then cache
//   // and distribute
//   devServer: {
//     proxy: {
//       '/api*': {
//         // Forward frontend dev server request for /api to django dev server
//         target: 'http://localhost:8090/', // debug local
//         //target: "http://host.docker.internal:8090/" // debug docker
//       }
//     }
//   },
//   configureWebpack: {
//     devtool: 'source-map'
//   }
// }
