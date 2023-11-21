import { createContext } from "react";

const authContext = createContext({ auth: null });

const AuthProvider = authContext.Provider;
const AuthConsumer = authContext.Consumer;

export { AuthProvider, AuthConsumer };
