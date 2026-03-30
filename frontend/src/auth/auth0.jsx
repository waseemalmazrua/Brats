import { useAuth0 } from "@auth0/auth0-react";

export default function Auth() {
  const {
    isLoading,
    isAuthenticated,
    error,
    loginWithRedirect,
    logout,
    user,
  } = useAuth0();

  const handleLogin = () => loginWithRedirect();

  const handleSignup = () =>
    loginWithRedirect({ authorizationParams: { screen_hint: "signup" } });

  const handleLogout = () =>
    logout({ logoutParams: { returnTo: window.location.origin } });

  if (isLoading) return <p>جاري التحميل...</p>;

  return (
    <div>
      {isAuthenticated ? (
        <>
          <p>مرحباً {user.email}</p>
          <img src={user.picture} alt="profile" width={60} />
          <pre>{JSON.stringify(user, null, 2)}</pre>
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