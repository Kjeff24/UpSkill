import FormInput from "../../components/FormInput";

const Contact = () => {
  return (
    <section
      style={{ paddingTop: "60px", paddingBottom: "30px" }}
      className="fs-5"
      id="contact"
    >
      <div
        className=""
        style={{ maxWidth: "700px", width: "100%", marginInline: "auto" }}
      >
        <h1 className="text-center text-success display-6 fw-bold">
          Send us a message
        </h1>
        <form action="" method="post">
          <FormInput hasUsername hasEmail />
          <div className="mb-3">
            <label htmlFor="exampleFormControlTextarea1" className="form-label">
              Message
            </label>
            <textarea
              className="form-control bg-light"
              id="exampleFormControlTextarea1"
              rows={3}
            ></textarea>
          </div>
          <div className="d-md-block d-grid">
            <input
              type="submit"
              value="Send message"
              className="btn btn-success fs-5"
            />
          </div>
        </form>
      </div>
    </section>
  );
};

export default Contact;
