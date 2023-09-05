import React from "react";

const InputWithLabel = ({ type, id, name, label, required }) => {
  return (
    <div className="inputBox">
      <input type={type} id={id} name={name} required={required} />
      <span>{label}</span>
    </div>
  );
};

export default InputWithLabel;
