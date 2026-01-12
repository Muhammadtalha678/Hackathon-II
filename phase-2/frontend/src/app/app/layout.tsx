import { Navigation } from "@/components/navigation";
import { ProtectedLayout } from "@/components/protected-layout";

export default function AppLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ProtectedLayout>
      <Navigation />
      {children}
    </ProtectedLayout>
  );
}