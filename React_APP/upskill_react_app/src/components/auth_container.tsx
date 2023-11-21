import Signin from "./signin";
import Signup from "./signup";
import loginImage from "../assets/images/Upskill.png";

const Auth_container = () => {
  return (
    <section className="container-fluid bg-white" style={{ height: "100vh" }}>
      <div className="row h-100 ">
        <div className="col-lg-6 bg-primary p-3 d-flex justify-content-center align-items-center  ">
          <img src={loginImage} alt="" width={"70%"} />
        </div>
        <div className="col-lg-6 d-flex justify-content-center align-items-center p-3">
          <div
            className="bg-white p-2 rounded"
            style={{ maxWidth: "600px", width: "100%" }}
          >
            <div id="carouselExampleControls" className="carousel slide">
              <div className="carousel-inner">
                <div className="carousel-item active">
                  <Signup />
                </div>
                <div className="carousel-item">
                  <Signin />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Auth_container;
