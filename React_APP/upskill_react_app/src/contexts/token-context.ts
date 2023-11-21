import { createContext } from "react";

const tokenContext = createContext({ setToken: function () {} });

export { tokenContext };
