import React, { useState } from "react";
import { formStateType } from "../components/signup";

function useFormData(fields: formStateType): any {
  const [formData, setFormData] = useState<formStateType>(fields);
  const inputChange = (event: React.ChangeEvent<HTMLFormElement>) => {
    setFormData({ ...formData, [event.target.name]: event.target.value });
  };

  return [formData, inputChange];
}

export default useFormData;
