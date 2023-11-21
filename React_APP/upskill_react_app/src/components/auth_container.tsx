import Signin from "./signin";
import Signup from "./signup";

const Auth_container = () => {
  return (
    <section className="container-fluid bg-white" style={{ height: "100vh" }}>
      <div className="row h-100 ">
        <div className="col-lg-6 bg-primary p-3 d-flex justify-content-center align-items-center">
          <p>
            Lorem ipsum dolor, sit amet consectetur adipisicing elit. Assumenda
            deserunt vel reprehenderit accusamus culpa velit modi nostrum! At
            quidem ex, libero quibusdam dolore id quo nobis eveniet, in sunt
            molestiae nulla cumque iusto? Hic velit, doloremque sequi aliquid
            amet error dignissimos et exercitationem nisi in repellat quisquam?
            Esse, pariatur facere!
          </p>
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
