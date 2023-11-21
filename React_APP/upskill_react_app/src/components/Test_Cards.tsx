type cardTypes = {
  img: string;
  description: string;
};

const Test_Cards = ({ img, description }: cardTypes) => {
  return (
    <div className="card m-2">
      <img src={img} className="card-img-top" alt="..." />
      <div className="card-body">
        <i className="bi bi-quote fs-3"></i>
        <span className="card-text">{description}</span>
      </div>
    </div>
  );
};

export default Test_Cards;
