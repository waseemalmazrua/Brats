import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";
import { Auth0Provider } from "@auth0/auth0-react";
import "./index.css";

const authParams = {
  redirect_uri: window.location.origin,
  audience: import.meta.env.VITE_AUTH0_AUDIENCE,
  scope: "openid profile email",
};

// يضيف audience بس إذا موجود في .env
if (import.meta.env.VITE_AUTH0_AUDIENCE) {
  authParams.audience = import.meta.env.VITE_AUTH0_AUDIENCE;
}

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <Auth0Provider
      domain={import.meta.env.VITE_AUTH0_DOMAIN}
      clientId={import.meta.env.VITE_AUTH0_CLIENT_ID}
      authorizationParams={authParams}
    >
      <App />
    </Auth0Provider>
  </StrictMode>
);