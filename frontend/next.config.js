/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  output: 'standalone', // For Docker deployment
  transpilePackages: ['globe.gl', 'three-globe', 'three'],
  webpack: (config, { isServer, webpack }) => {
    // Fix for Three.js and globe.gl compatibility
    config.resolve.fallback = {
      ...config.resolve.fallback,
      fs: false,
    };
    
    // Note: We're using patch-package to fix three.js and three-globe
    // The patches add the missing exports directly to node_modules
    // No webpack aliases needed - let Next.js use the patched files
    
    // Handle .mjs files properly
    config.module = {
      ...config.module,
      rules: [
        ...config.module.rules,
        {
          test: /\.mjs$/,
          include: /node_modules/,
          type: 'javascript/auto',
          resolve: {
            fullySpecified: false,
          },
        },
      ],
    };
    
    return config;
  },
}

module.exports = nextConfig

