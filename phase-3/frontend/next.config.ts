import type { NextConfig } from "next";

const nextConfig: NextConfig = {

  serverExternalPackages: ["better-auth"],
  redirects() {
    return [
      {
        source: "/",
        destination: "/tasks",
        permanent: true
      }
    ]
  },
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'lh3.googleusercontent.com',
      },
      {
        protocol: 'https',
        hostname: 'avatars.githubusercontent.com',
      },
    ],
  },
  typescript: {
    ignoreBuildErrors: true,
  },
};

export default nextConfig;
