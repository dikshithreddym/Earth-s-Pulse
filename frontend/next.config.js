/** @type {import('next').NextConfig} */
const path = require('path')
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
    
    // Ensure all imports resolve to the same three instance to avoid
    // multiple-three warnings and prototype mismatches when using
    // globe.gl / three-globe alongside three.
    config.resolve = config.resolve || {}
    config.resolve.alias = {
      ...(config.resolve.alias || {}),
      three: path.resolve('./node_modules/three'),
    }
    
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

