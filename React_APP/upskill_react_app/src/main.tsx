import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx"
import "./assets/scss/custom_bs_style.css"
import "../node_modules/bootstrap/dist/js/bootstrap.bundle.js"

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
