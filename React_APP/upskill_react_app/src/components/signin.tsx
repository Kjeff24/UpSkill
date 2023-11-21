import useFormData from "../hooks/useFormData";
import FormInput from "./FormInput";

import { useContext } from "react";

import { tokenContext } from "../contexts/token-context";

const Signin = () => {
  const context = useContext(tokenContext);

  const [formData, inputChange, submitData] = useFormData({
    username: "",
    email: "",
    password: "",
    personality: "learner",
    setToken: context.setToken,
  });

  return (
    <form
      action=""
      method="post"
      className="p-1 fs-5"
      autoComplete="off"
      onSubmit={submitData}
    >
      <FormInput
        hasUsername
        hasEmail
        hasPassword
        hasSelection
        selete_text="Sign in as?"
        formData={formData}
        inputChange={inputChange}
      />
      <div className="mb-3">
        <p>
          Don't have an account
          <a
            href=""
            type="button"
            className="ms-2"
            data-bs-target="#carouselExampleControls"
            data-bs-slide="next"
          >
            sign up
          </a>
        </p>
      </div>
      <div className="d-grid">
        <button type="submit" className="btn btn-primary fs-5">
          Sign In
        </button>
      </div>
    </form>
  );
};

export default Signin;
