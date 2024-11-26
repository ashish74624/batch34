/** @type {import('next').NextConfig} */
const nextConfig = {
    env:{
        BACKEND: process.env.BACKEND,
        CLOUD_NAME:process.env.CLOUD_NAME
    },
    images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'res.cloudinary.com',
        port: '',
        pathname: '/deirqjd6e/**',
      },
    ],
  },
};

export default nextConfig;
