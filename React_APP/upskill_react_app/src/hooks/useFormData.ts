import React, { useState } from "react";
import { formStateType } from "../components/signup";

function useFormData(fields: formStateType): any {
  const [formData, setFormData] = useState<formStateType>(fields);
  const inputChange = (event: React.ChangeEvent<HTMLFormElement>) => {
    setFormData({ ...formData, [event.target.name]: event.target.value });
  };
  const submitData = (event: React.FormEvent) => {
    event.preventDefault();
    console.log(formData);
    // fields.setToken("Token");
    fields.setToken ? fields.setToken() : null;
  };

  return [formData, inputChange, submitData];
}

export default useFormData;
