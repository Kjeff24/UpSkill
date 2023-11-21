type tool_type = {
  name: string;
};

const Tech_tools_card = ({ name }: tool_type) => {
  return (
    <div className="rounded-pill border border-secondary px-3">{name}</div>
  );
};

export default Tech_tools_card;
