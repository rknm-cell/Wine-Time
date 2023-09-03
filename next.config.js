module.exports = {
  async rewrites() {
    return [
      {
        source: '@server/:path*',
        destination: 'http://127.0.0.1:5555/:path*', // Proxy to Backend
      },
    ]
  },
}