import Carousel from "react-multi-carousel";
import "react-multi-carousel/lib/styles.css";
import Test_Cards from "../../components/Test_Cards";
import image from "../../assets/images/home-v-1.jpg";

const Testimonies = () => {
  const responsive = {
    superLargeDesktop: {
      // the naming can be any, depends on you.
      breakpoint: { max: 4000, min: 992 },
      items: 4,
    },
    desktop: {
      breakpoint: { max: 992, min: 768 },
      items: 3,
    },
    tablet: {
      breakpoint: { max: 768, min: 464 },
      items: 2,
    },
    mobile: {
      breakpoint: { max: 464, min: 0 },
      items: 1,
    },
  };

  const CustomLeftArrow = ({ onClick }) => (
    <button
      onClick={onClick}
      className="react-multiple-carousel__arrow react-multiple-carousel__arrow--left bg-success shadow"
    ></button>
  );

  // CustomRightArrow Component
  const CustomRightArrow = ({ onClick }) => (
    <button
      onClick={onClick}
      className="react-multiple-carousel__arrow react-multiple-carousel__arrow--right bg-success shadow"
    ></button>
  );

  return (
    <section
      style={{ paddingTop: "70px", paddingBottom: "30px" }}
      className=""
      id="testimonies"
    >
      <h3 className="text-success">Testimonies</h3>
      <div className="fs-5">
        <Carousel
          customLeftArrow={<CustomLeftArrow />}
          customRightArrow={<CustomRightArrow />}
          infinite={true}
          responsive={responsive}
        >
          <Test_Cards img={image} description="dDFF DFDFDF DFDDFDF DFDFDF" />
          <Test_Cards img={image} description="dDFF DFDFDF DFDDFDF DFDFDF" />
          <Test_Cards img={image} description="dDFF DFDFDF DFDDFDF DFDFDF" />
          <Test_Cards img={image} description="dDFF DFDFDF DFDDFDF DFDFDF" />
          <Test_Cards img={image} description="dDFF DFDFDF DFDDFDF DFDFDF" />
          <Test_Cards img={image} description="dDFF DFDFDF DFDDFDF DFDFDF" />
          <Test_Cards img={image} description="dDFF DFDFDF DFDDFDF DFDFDF" />
          <Test_Cards img={image} description="dDFF DFDFDF DFDDFDF DFDFDF" />
          <Test_Cards img={image} description="dDFF DFDFDF DFDDFDF DFDFDF" />
          <Test_Cards img={image} description="dDFF DFDFDF DFDDFDF DFDFDF" />
        </Carousel>
      </div>
    </section>
  );
};

export default Testimonies;
