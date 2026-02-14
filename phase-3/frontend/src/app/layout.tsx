import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Navigation } from "@/components/navigation";
import { Toaster } from "sonner";
import { ChatbotWrapper } from "@/components/ChatbotWrapper";
// import "@openai/chatkit-react/";
// import "@openai/chatkit-react/styles.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Task Manager",
  description: "A task management application with authentication",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <Navigation />
        <main>{children}</main>

        {/* This will render on all pages but hide itself on login/register/profile */}
        {/* <ChatbotWrapper />  */}
        <Toaster richColors position="top-center" />
      </body>
    </html>
  );
}
