"use client";

import { useState } from "react";
import { usePathname } from "next/navigation";
import { ChatKit, useChatKit } from "@openai/chatkit-react";
import { authClient } from "@/lib/auth/auth-client";

export function ChatbotWrapper() {
  const pathname = usePathname();
  const excludedRoutes = ["/login", "/register", "/profile"];
  const [open, setOpen] = useState(false);

  const chat = useChatKit({
    api: {
      url: process.env.NEXT_PUBLIC_BACKEND_URL!,
      domainKey:
        process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY!,

      fetch: async (input: RequestInfo | URL, init?: RequestInit) => {
        // Get auth token + session
        const [{ data: tokenData }, { data: session }] =
          await Promise.all([
            authClient.token(),
            authClient.getSession(),
          ]);

        const token = tokenData?.token;
        const userId = session?.user?.id;

        if (!token || !userId) {
          throw new Error("Authentication failed");
        }

        // Forward request to FastAPI
        return fetch(`http://localhost:8000/${userId}/chat`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: init?.body, // ChatKit message body
        });
      },
    },
  });

  if (excludedRoutes.includes(pathname)) return null;

  return (
    <>
      {/* Floating button */}
      {!open && (
        <button
          onClick={() => setOpen(true)}
          className="fixed bottom-6 right-6 z-50 bg-blue-600 text-white px-4 py-3 rounded-full shadow-lg"
        >
          💬
        </button>
      )}

      {/* Chat window */}
      {open && (
        <div className="fixed bottom-6 right-6 z-50 w-96 h-[550px] shadow-2xl rounded-2xl overflow-hidden border bg-white flex flex-col">
          
          {/* Header */}
          <div className="p-3 bg-blue-600 text-white font-medium flex justify-between items-center">
            <span>AI Assistant</span>
            <button onClick={() => setOpen(false)}>✕</button>
          </div>

          {/* Chat area */}
          <div className="flex-1 overflow-hidden">
            <ChatKit control={chat.control} className="h-full" />
          </div>
        </div>
      )}
    </>
  );
}
