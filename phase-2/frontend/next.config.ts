import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  experimental: {
    serverComponentsExternalPackages: ["better-auth"],
  },
  images: {
    domains: ["lh3.googleusercontent.com", "avatars.githubusercontent.com"], // For Better Auth avatar images
  },
  // typescript: {
  //   ignoreBuildErrors: true,
  // },
};

export default nextConfig;
