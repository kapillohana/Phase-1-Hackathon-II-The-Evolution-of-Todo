/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export', // This enables static export for platforms like Netlify
  trailingSlash: true, // Optional: adds trailing slashes to URLs
  experimental: {
    esmExternals: 'loose',
  },
  images: {
    domains: ['localhost', 'api.todo-app.com', 'your-api-domain.com'],
  },
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
      };
    }
    return config;
  },
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: '*' },
          { key: 'Access-Control-Allow-Methods', value: 'GET, POST, PUT, DELETE, OPTIONS' },
          { key: 'Access-Control-Allow-Headers', value: 'Content-Type, Authorization' },
        ],
      },
    ];
  },
};

export default nextConfig;