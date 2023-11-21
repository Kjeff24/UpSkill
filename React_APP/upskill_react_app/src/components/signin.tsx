import useFormData from "../hooks/useFormData";
import FormInput from "./FormInput";

const Signin = () => {
  const [formData, inputChange] = useFormData({
    username: "",
    email: "",
    password: "",
    personality: "learner",
  });

  const submitData = (event: React.FormEvent) => {
    event.preventDefault();

    console.log(formData); // process the form input
  };

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
