import { formStateType } from "./signup";

type FormInputPropsType = {
  hasFirstname?: boolean;
  hasLastname?: boolean;
  hasUsername?: boolean;
  hasEmail?: boolean;
  hasPassword?: boolean;
  hasCon_password?: boolean;
  hasSelection?: boolean;
  selete_text?: string;
  formData?: formStateType;
  inputChange?: React.ChangeEventHandler;
};

const FormInput = ({
  hasFirstname,
  hasLastname,
  hasUsername,
  hasEmail,
  hasPassword,
  hasCon_password,
  hasSelection,
  selete_text,
  formData,
  inputChange,
}: FormInputPropsType) => {
  const form_firstName = hasFirstname ? (
    <div className="mb-3">
      <label htmlFor="firstname" className="form-label">
        First Name
      </label>
      <input
        type="text"
        name="firstname"
        id="firstname"
        className="form-control bg-light"
        required
        minLength={3}
        pattern="[A-Za-z]*"
        value={formData?.firstname}
        onChange={inputChange}
      />
    </div>
  ) : null;
  const form_lastName = hasLastname ? (
    <div className="mb-3">
      <label htmlFor="lastname" className="form-label">
        Last Name
      </label>
      <input
        type="text"
        name="lastname"
        id="lastname"
        className="form-control bg-light"
        required
        minLength={3}
        pattern="[A-Za-z]*"
        value={formData?.lastname}
        onChange={inputChange}
      />
    </div>
  ) : null;
  const form_username = hasUsername ? (
    <div className="mb-3">
      <label htmlFor="username" className="form-label">
        Username
      </label>
      <input
        type="text"
        name="username"
        id="username"
        className="form-control bg-light"
        required
        minLength={3}
        pattern="^[A-Za-z][A-Za-z0-9]*"
        value={formData?.username}
        onChange={inputChange}
      />
    </div>
  ) : null;
  const form_email = hasEmail ? (
    <div className="mb-3">
      <label htmlFor="email" className="form-label">
        Email
      </label>
      <input
        type="email"
        name="email"
        id="email"
        className="form-control bg-light"
        required
        value={formData?.email}
        onChange={inputChange}
      />
    </div>
  ) : null;
  const form_password = hasPassword ? (
    <div className="mb-3">
      <label htmlFor="password" className="form-label">
        Password
      </label>
      <input
        type="password"
        name="password"
        id="password"
        className="form-control bg-light"
        required
        value={formData?.password}
        onChange={inputChange}
      />
    </div>
  ) : null;
  const form_con_password = hasCon_password ? (
    <div className="mb-3">
      <label htmlFor="conpassword" className="form-label">
        Confirm Password
      </label>
      <input
        type="password"
        name="conpassword"
        id="conpassword"
        className="form-control bg-light"
        required
        value={formData?.conpassword}
        onChange={inputChange}
      />
    </div>
  ) : null;
  const form_selection = hasSelection ? (
    <div className="mb-3">
      <label htmlFor="sign-up-personality" className="form-label">
        {selete_text}
      </label>
      <select
        className="form-select bg-light"
        aria-label="Default select example"
        id="sign-up-personality"
        name="personality"
        value={formData?.personality}
        onChange={inputChange}
      >
        <option value="learner">Learner</option>
        <option value="tutor">Tutor</option>
      </select>
    </div>
  ) : null;
  return (
    <>
      {form_firstName}
      {form_lastName}
      {form_username}
      {form_email}
      {form_password}
      {form_con_password}
      {form_selection}
    </>
  );
};

export default FormInput;
