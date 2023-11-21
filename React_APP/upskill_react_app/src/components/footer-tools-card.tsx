const Footer_tools_card = ({ header, children }) => {
  return (
    <div className="">
      <h3 className="mb-3 text-success">{header}</h3>
      <div className="d-flex gap-3 flex-wrap">{children}</div>
    </div>
  );
};

export default Footer_tools_card;
