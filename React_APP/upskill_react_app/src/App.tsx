import {
  Route,
  createBrowserRouter,
  createRoutesFromChildren,
  RouterProvider,
} from "react-router-dom";
import HomePage from "./pages/HomePage";
import Auth_container from "./components/auth_container";
import { AuthContextProvider } from "./contexts/auth-context";
import Home from "./pages/AuthPages/Home";

const App = () => {
  const router = createBrowserRouter(
    createRoutesFromChildren(
      <Route>
        <Route path="/" element={<HomePage />}></Route>
        <Route path="sign_up" element={<Auth_container />} />
        <Route path="home" element={<Home />} />
      </Route>
    )
  );
  return (
    <AuthContextProvider>
      <RouterProvider router={router} />
    </AuthContextProvider>
  );
};

export default App;
