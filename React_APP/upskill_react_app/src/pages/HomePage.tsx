import { Link } from "react-router-dom";
import About from "./Sections/About";
import Contact from "./Sections/Contact";
import Testimonies from "./Sections/Testimonies";
import Footer_des_card from "../components/footer-des_card";
import Tech_tools_card from "../components/tech-tools_card";
import Footer_tools_card from "../components/footer-tools-card";

import image from "../assets/images/home-v-1.jpg";

const tools_name = [
  "html / css",
  "javascript",
  "python",
  "java",
  "c++",
  "c#",
  "c",
  "react.js / next.js",
  "node",
  "Django",
  "Flask",
  "Spring / Spring boot",
  "Tailwind css",
  "Bootstrap",
  "Material UI",
  "Figma",
  "Adobe XD",
  "Spring",
  "Vue",
  "Angular",
  "etc.",
];
const HomePage = () => {
  return (
    <>
      <header className="fixed-top border-bottom shadow">
        <nav className="navbar navbar-expand-lg navbar-light bg-white">
          <div className="container-fluid">
            <a className="navbar-brand fs-4 me-5" href="#">
              Upskill
            </a>
            <button
              className="navbar-toggler"
              type="button"
              data-bs-toggle="offcanvas"
              data-bs-target="#offcanvasNavbar"
              aria-controls="offcanvasNavbar"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div
              className="offcanvas offcanvas-start"
              id="offcanvasNavbar"
              aria-labelledby="offcanvasNavbarLabel"
            >
              <div className="offcanvas-header">
                <h5 className="offcanvas-title" id="offcanvasNavbarLabel">
                  Upskill
                </h5>
                <button
                  type="button"
                  className="btn-close text-reset"
                  data-bs-dismiss="offcanvas"
                  aria-label="Close"
                ></button>
              </div>
              <div className="offcanvas-body">
                <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                  <li className="nav-item">
                    <a
                      className="nav-link active fs-5"
                      aria-current="page"
                      href="#"
                    >
                      Home
                    </a>
                  </li>
                  <li className="nav-item">
                    <a className="nav-link fs-5" href="#about">
                      About
                    </a>
                  </li>
                  <li className="nav-item">
                    <a className="nav-link fs-5" href="#contact">
                      Contact
                    </a>
                  </li>
                  <li className="nav-item">
                    <a className="nav-link fs-5" href="#testimonies">
                      Testimonies
                    </a>
                  </li>
                </ul>
                <Link to="sign_up" className="btn btn-success fs-5">
                  Create account
                </Link>
              </div>
            </div>
          </div>
        </nav>
      </header>

      <main
        style={{
          marginTop: "100px",
          marginBottom: "40px",
        }}
        className="p-3 mx-2 mx-lg-5 bg-white rounded "
      >
        <section className="mt-4 " id="why-upskill">
          <div className="row fs-5">
            <div className="col-lg-6 d-flex align-items-center">
              <div className="">
                <h2 className="text-success mb-3">Why choose UpSkill?</h2>
                <p className="text-dark h1">
                  Empowering you to provide quality eLearning experiences
                </p>
                <div className="description mb-2">
                  <p>
                    At UpSkill, we are on a mission to empower employers to
                    improve our world with open source employee training
                    software. With hundreds of millions of users around the
                    globe and translated into 2 languages, UpSkill gives you the
                    freedom to create online teaching and training solutions
                    that best meet your learners' needs.
                  </p>
                </div>
              </div>
            </div>
            <div className="col-lg-6">
              <img
                src={image}
                alt=""
                className="img-fluid rounded mx-auto p-2"
              />
            </div>
          </div>
        </section>
        <About />
        <Testimonies />
        <Contact />
      </main>

      <footer className="bg-dark text-white py-4 fs-5">
        <div className="container">
          <div className="row g-3">
            <div className="col-lg-4">
              <Footer_des_card header="Tech Fields">
                <li>UI / UX </li>
                <li>Frontend Development</li>
                <li>Backend Development</li>
                <li>DevOps</li>
                <li>Cybersecurity</li>
              </Footer_des_card>
            </div>
            <div className="col-lg-8">
              <Footer_tools_card header="Tech Tools">
                {tools_name.map((ele, index) => {
                  return <Tech_tools_card name={ele} key={index} />;
                })}
              </Footer_tools_card>
            </div>
          </div>
          <div className="text-center mt-3">
            <p className="mb-2">Developed by </p>
            <div className="d-flex justify-content-center">
              <span>Jeffery</span>
              <div className="vr mx-2"></div>
              <span>Jeremiah</span>
              <div className="vr mx-2"></div>
              <span>James</span>
              <div className="vr mx-2"></div>
              <span>Umaxcode</span>
            </div>
            <p>with ❤ @ all right reserved </p>
          </div>
        </div>
      </footer>
    </>
  );
};

export default HomePage;
