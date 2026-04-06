import { useEffect, useState } from "react";
import { useAuth0 } from "@auth0/auth0-react";

export default function Auth() {
  const {
    isLoading,
    isAuthenticated,
    error,
    loginWithRedirect,
    logout,
    user,
    getAccessTokenSilently,
  } = useAuth0();

  const [backendUser, setBackendUser] = useState(null);

  const handleLogin = () => loginWithRedirect();

  const handleSignup = () =>
    loginWithRedirect({
      authorizationParams: { screen_hint: "signup" },
    });

  const handleLogout = () =>
    logout({
      logoutParams: {
        returnTo: window.location.origin,
      },
    });

  // 🔥 إرسال التوكن للـ backend (مرة وحدة فقط)
  useEffect(() => {
    const sendUserToBackend = async () => {
      try {
        const token = await getAccessTokenSilently();

        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/users/me`,
          {
            method: "GET", // ✅ مهم
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!response.ok) {
          throw new Error("Failed to fetch user from backend");
        }

        const data = await response.json();
        setBackendUser(data);

        console.log("✅ Backend user:", data);
      } catch (err) {
        console.error("❌ Error:", err);
      }
    };

    if (isAuthenticated) {
      sendUserToBackend();
    }
  }, [isAuthenticated, getAccessTokenSilently]);

  if (isLoading) return <p>جاري التحميل...</p>;

  return (
    <div>
      {isAuthenticated ? (
        <>
          <h3>Frontend User</h3>
          <p>{user?.email}</p>
          <img src={user?.picture} alt="profile" width={60} />

          <h3>Backend User</h3>
          <pre>{JSON.stringify(backendUser, null, 2)}</pre>

          <button onClick={handleLogout}>تسجيل الخروج</button>
        </>
      ) : (
        <>
          {error && <p>خطأ: {error.message}</p>}
          <button onClick={handleSignup}>إنشاء حساب</button>
          <button onClick={handleLogin}>تسجيل الدخول</button>
        </>
      )}
    </div>
  );
}