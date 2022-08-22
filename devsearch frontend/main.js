let baseUrl = 'dev-search-eg.herokuapp.com' || "http://127.0.0.1:3000";

let loginBtn = document.getElementById('login-btn')
let logoutBtn = document.getElementById('logout-btn')
let token = localStorage.getItem('token')
if (token) {
    loginBtn.remove()
} else {
    logoutBtn.remove()
}

logoutBtn.addEventListener('click', (e) => {
    e.preventDefault()
    localStorage.removeItem('token')
    window.location = 'login.html'
})


let projectsUrl = `${baseUrl}/api/projects/`;

let getProjects = () => {
  fetch(projectsUrl)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log(data);
      buildProjects(data);
    });
};

let buildProjects = (projectsData) => {
  let projectsWrapper = document.getElementById("projects-wrapper");
  projectsWrapper.innerHTML = '';
  for (const projectData of projectsData) {
    let projectCard = `
        <div class="project--card">
            <img src="${baseUrl}${projectData.feature_image}" alt="">
            <div>
                <div class="card--header">
                    <h3>${projectData.title}</h3>
                    <strong class="vote--option" data-vote="up" data-project="${projectData.id}">&#43;</strong>
                    <strong class="vote--option" data-vote="down" data-project="${projectData.id}">&#8722;</strong>
                </div>
                <i>${projectData.vote_ratio}% Positive feedback</i>
                <p>${projectData.description.substring(0, 150)}</p>
            </div>
        </div>

        `;
    projectsWrapper.innerHTML += projectCard;
  }

  //Add an listener
  addVoteEvents();
};

let addVoteEvents = () => {
  let voteBtns = document.getElementsByClassName("vote--option");

  for (let i = 0; voteBtns.length > i; i++) {
    voteBtns[i].addEventListener("click", (e) => {
      let token = localStorage.getItem("token");
      console.log("TOKEN:", token);
      if (!token){
        window.location = 'login.html'
      }
      let vote = e.target.dataset.vote;
      let project = e.target.dataset.project;

      fetch(`${baseUrl}/api/projects/${project}/vote/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ value: vote }),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("Success:", data);
          getProjects();
        });
    });
  }
};

getProjects();
