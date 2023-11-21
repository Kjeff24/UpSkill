import { createContext, useState, ReactNode, useContext } from "react";
const AuthContext = createContext({});

type AuthPropType = {
  children: ReactNode;
};

const AuthContextProvider = ({ children }: AuthPropType) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [token, setToken] = useState("");

  const login = () => {
    // logics to show a user is login
    // fetch("") // a fetch to the login endpoint
    //   .then((res) => res.json())
    //   .then((data) => setToken(data["token"]));

    setIsAuthenticated(true);
    setToken("Token");
  };

  const logout = () => {
    // logics to show a user is logout
    // fetch("");
    setIsAuthenticated(false);
    setToken("");
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, logout, token }}>
      {children}
    </AuthContext.Provider>
  );
};

const AuthContextConsumer = () => {
  return useContext(AuthContext);
};

export { AuthContextProvider, AuthContextConsumer };
