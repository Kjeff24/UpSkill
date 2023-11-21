const Footer_des_card = ({ children, header }) => {
  return (
    <div className="text-white fs-5">
      <h3 className="text-success">{header}</h3>
      <ul className="">{children}</ul>
    </div>
  );
};

export default Footer_des_card;
