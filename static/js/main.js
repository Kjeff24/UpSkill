const sideBarToolsBtn = document.querySelectorAll("a.tools-button");
  const sideBarBig = document.querySelector(".side-bar-big");
  const sideBarSmall = document.querySelector(".side-bar-small");
  sideBarToolsBtn.forEach(function (link) {
    link.addEventListener("click", function () {
      sideBarBig.classList.toggle("active");
      sideBarSmall.classList.toggle("active");
    });

  })

// Handle download increment
// Get all the download links
var downloadLinks = document.querySelectorAll(".download-link");


// Iterate over each download link
downloadLinks.forEach(function (link) {
    // Add click event listener
    link.addEventListener("click", function (event) {
        

        // Get the file ID from the link's href attribute
        var fileID = link.getAttribute("data-file-id");

        // Call the increaseDownload view using AJAX
        fetch("/resource/" + fileID + "/download/")
            .then(function (response) {
                if (response.ok) {
                    // Perform any additional actions after the download is incremented
                    // ...
                } else {
                    console.error("Error: " + response.status);
                }
            })
            .catch(function (error) {
                console.error("Error: " + error);
            });
    });
});

