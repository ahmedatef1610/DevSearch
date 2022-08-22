let baseUrl = 'dev-search-eg.herokuapp.com' || "http://127.0.0.1:3000";
let form = document.getElementById('login-form')

form.addEventListener('submit', (e) => {
    e.preventDefault()

    let formData = {
        'username': form.username.value,
        'password': form.password.value
    }

    fetch(`${baseUrl}/api/users/token/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
        .then(response => response.json())
        .then(data => {
            console.log('DATA:', data.access)
            if (data.access) {
                localStorage.setItem('token', data.access)
                window.location = 'projects-list.html'
            } else {
                alert('Username OR password did not work')
            }
        })
})

console.log(ENV);