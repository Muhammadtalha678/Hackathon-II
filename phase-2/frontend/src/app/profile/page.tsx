"use client";

import { useEffect, useState } from "react";
import { toast } from "sonner";
import { authClient } from "@/lib/auth/auth-client";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ProfileForm } from "@/components/auth/profile-form";
import { PasswordChangeForm } from "@/components/auth/password-change-form";
import { Separator } from "@/components/ui/separator";

export default function ProfilePage() {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const { data: session } = await authClient.getSession();
        if (session?.user) {
          setUser(session.user);
        } else {
          throw new Error("User not authenticated");
        }
      } catch (error: any) {
        toast.error("Error fetching user data", {
          description: error.message || "Failed to load user data",
        });
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  const handleProfileUpdate = () => {
    // Refresh user data after update
    const fetchUser = async () => {
      try {
        const { data: session } = await authClient.getSession();
        if (session?.user) {
          setUser(session.user);
        }
      } catch (error: any) {
        toast.error("Error fetching user data", {
          description: error.message || "Failed to load user data",
        });
      }
    };

    fetchUser();
    toast.success("Profile updated successfully!");
  };

  if (loading) {
    return (
      <div className="container mx-auto py-10">
        <p>Loading profile...</p>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="container mx-auto py-10">
        <p>User not found</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-10">
      <div className="max-w-2xl mx-auto space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Profile Information</CardTitle>
            <CardDescription>
              Update your profile information here.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ProfileForm
              initialData={{
                name: user.name || ""
              }}
              onProfileUpdate={handleProfileUpdate}
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Change Password</CardTitle>
            <CardDescription>
              Change your password here. Make sure to use a strong password.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <PasswordChangeForm
              onPasswordChange={() => {
                toast.success("Password changed successfully!");
              }}
            />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}