import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import Auth_container from "./components/auth_container";
import { AuthProvider } from "./contexts/auth-context";
import { useState } from "react";
import { tokenContext } from "./contexts/token-context";

const App = () => {
  const [token, setToken] = useState(null);
  console.log(token);
  return (
    <AuthProvider value={{ auth: token }}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />}></Route>
          <Route path="sign_up" element={<Auth_container />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;
