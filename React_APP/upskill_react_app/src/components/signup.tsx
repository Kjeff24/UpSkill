import FormInput from "./FormInput";
import useFormData from "../hooks/useFormData";

export type formStateType = {
  firstname?: string;
  lastname?: string;
  username: string;
  email: string;
  password: string;
  conpassword?: string;
  personality: string;
  setToken?: () => void;
};

const Signup = () => {
  const [formData, inputChange, submitData] = useFormData({
    firstname: "",
    lastname: "",
    username: "",
    email: "",
    password: "",
    conpassword: "",
    personality: "learner",
  });

  return (
    <form
      method="post"
      action=""
      className="p-1 fs-5"
      autoComplete="off"
      onSubmit={submitData}
    >
      <FormInput
        hasFirstname
        hasLastname
        hasUsername
        hasEmail
        hasPassword
        hasCon_password
        hasSelection
        selete_text="Sign up as?"
        formData={formData}
        inputChange={inputChange}
      />
      <div className="mb-3">
        <p>
          Already have an account?
          <a
            href=""
            type="button"
            data-bs-target="#carouselExampleControls"
            data-bs-slide="prev"
            className="ms-2"
          >
            Login
          </a>
        </p>
      </div>
      <div className="d-grid">
        <button type="submit" className="btn btn-primary text-white fs-5">
          Sign Up
        </button>
      </div>
    </form>
  );
};

export default Signup;
