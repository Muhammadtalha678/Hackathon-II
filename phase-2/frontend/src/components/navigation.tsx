"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Button } from "@/components/ui/button";
import { authClient } from "@/lib/auth/auth-client";
import { toast } from "sonner";
import { useRouter } from "next/navigation";

export function Navigation() {
  const pathname = usePathname();
  const router = useRouter();



  // Don't show navigation on auth pages
  if (pathname === '/login' || pathname === '/register') {
    return null
  }

  const handleSignOut = async () => {
    try {
      await authClient.signOut({
        fetchOptions: {
          onSuccess: () => {
            router.push("/login"); // redirect to login page
          },
        }
      });
    } catch (error: any) {
      toast.error("Error signing out", {
        description: error.message || "An error occurred while signing out",
      });
    }
  };

  return (
    <header className="border-b">
      <div className="container flex h-16 items-center justify-between px-4">
        <div className="flex items-center gap-6">
          <Link href="/tasks" className="text-xl font-bold">
            Task Manager
          </Link>
          <nav className="flex gap-4 sm:gap-6">
            <Link
              href="/tasks"
              className={`text-sm font-medium transition-colors hover:underline ${pathname === '/tasks' ? 'text-foreground' : 'text-muted-foreground'}`}
            >
              Tasks
            </Link>
            <Link
              href="/profile"
              className={`text-sm font-medium transition-colors hover:underline ${pathname === '/profile' ? 'text-foreground' : 'text-muted-foreground'}`}
            >
              Profile
            </Link>
          </nav>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" onClick={handleSignOut}>
            Sign Out
          </Button>
        </div>
      </div>
    </header>
  );
}