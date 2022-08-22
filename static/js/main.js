let searchForm = document.getElementById("searchForm");
let pageLinks = document.getElementsByClassName("page-link");

if (searchForm) {
  for (const pageLink of pageLinks) {
    pageLink.addEventListener("click", function (e) {
      e.preventDefault();

      let page = this.dataset.page;

      searchForm.innerHTML += `<input type="hidden" name="page" value="${page}">`;

      searchForm.submit();
    });
  }
}

let baseUrl = 'dev-search-eg.herokuapp.com' || "http://127.0.0.1:3000";
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
let tags = document.getElementsByClassName("project-tag");
for (const tag of tags) {
    
  tag.addEventListener("click", (e) => {

    let tagId = e.target.dataset.tag;
    let projectId = e.target.dataset.project;

    fetch(`${baseUrl}/api/remove-tag/`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ project: projectId, tag: tagId }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        e.target.remove();
      });


    // fetch(`${baseUrl}/projects/remove-tag/`, {
    //   method: "DELETE",
    //   headers: {
    //     "Content-Type": "application/json",
    //     'X-CSRFToken': csrftoken
    //   },
    //   body: JSON.stringify({ project: projectId, tag: tagId }),
    // })
    //   .then((response) => response.json())
    //   .then((data) => {
    //     console.log(data);
    //     e.target.remove();
    //   });




  });
}
