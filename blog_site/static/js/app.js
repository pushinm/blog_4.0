const currentURL = window.location.pathname;
const createAuthor = () => {
    const url = '/users/api/create_author/'; 
    const firstNameInput = document.getElementById('first-name');
    const lastNameInput = document.getElementById('last-name');
    const usernameInput = document.getElementById('username');
    const gender = document.getElementById('gender');
    const passwordInput = document.getElementById('password');
  
    const data = {
      first_name: firstNameInput.value,
      last_name: lastNameInput.value,
      username: usernameInput.value,
      gender: gender.value,
      password: passwordInput.value,
    };
  
    fetch(url, {
      method: "POST",
      headers: {
      'Content-Type': 'application/json'
      },
      body: JSON.stringify(data),
    })
    .then(response => {
      if (response.status == 201) {
        alert('Регистрация прошла успешно!')
      }else if (response.status == 500){
        alert('Такое имя пользователя уже существует!')
      }
      return response.json();
    })
  };
  if (currentURL === '/users/create_author/') {
    console.log(currentURL)
    const form = document.getElementById('create-author-form');
  form.addEventListener('submit', event => {
    event.preventDefault();
    createAuthor();
  }); 
  }


  const fetchDataFromBackend = async (url) => {
    const parentDiv = document.querySelector('.mydiv');
    const paginationDiv = document.querySelector('.pagination ul');
    parentDiv.innerHTML = ''; // Clear existing content
    paginationDiv.innerHTML = ''; // Clear pagination
    
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error("HTTP error " + response.status);
      }
  
      const { count, previous, next, results } = await response.json();
  
      results.forEach(blog => {
        const colDiv = document.createElement('div');
        colDiv.classList.add('col-md-4');
  
        const cardDiv = document.createElement('div');
        cardDiv.classList.add('card', 'mb-4');
  
        const imgElement = document.createElement('img');
        imgElement.src = blog.photo;
        imgElement.alt = blog.title;
        imgElement.classList.add('card-img-top');
  
        const cardBodyDiv = document.createElement('div');
        cardBodyDiv.classList.add('card-body', 'text-center');
  
        const cardTitle = document.createElement('h5');
        const cardLink = document.createElement('a');
        cardLink.href = `/blog/detail/${blog.id}`;
        cardLink.style.textDecoration = 'none';
        cardLink.textContent = blog.title;
  
        cardTitle.appendChild(cardLink);
        cardBodyDiv.appendChild(cardTitle);
  
        cardDiv.appendChild(imgElement);
        cardDiv.appendChild(cardBodyDiv);
  
        colDiv.appendChild(cardDiv);
  
        parentDiv.appendChild(colDiv);
      });
  
      // Update pagination links
      updatePagination(previous, next);
  
      console.log('Total Blogs:', count);
    } catch (error) {
      console.error('Error:', error);
    }
  };
  
  function updatePagination(previousPage, nextPage) {
    const paginationDiv = document.querySelector('.pagination ul');
  
    if (previousPage) {
      const previousLink = createPaginationLink(previousPage, 'Previous');
      paginationDiv.appendChild(previousLink);
    }
  
    if (nextPage) {
      const nextLink = createPaginationLink(nextPage, 'Next');
      paginationDiv.appendChild(nextLink);
    }
  }
  
  function createPaginationLink(pageURL, label) {
    const link = document.createElement('a');
    link.classList.add('page-link');
    link.href = '#';
    link.textContent = label;
    link.addEventListener('click', event => {
      event.preventDefault();
      fetchDataFromBackend(pageURL);
    });
  
    const listItem = document.createElement('li');
    listItem.classList.add('page-item');
    listItem.appendChild(link);
  
    return listItem;
  }
  
  
  if (currentURL == '/') {
    const initialApiUrl = 'api/';
    fetchDataFromBackend(initialApiUrl);
    console.log(currentURL);
  }
 




  // Fetch function for AuthorApiLogin view
// const loginAuthor = async (username, password) => {
//     const response = await fetch('/api/login/', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify({ username, password }),
//     })
//     .then(response => {
//       if (response.status == 200) {
//         alert('Вход выполнен!')
//       }
//       return response.json();
//     })
//     if (!response.ok) {
//       throw new Error('Login failed');
//     }
// };
// const loginAuthor = async (username, password) => {
//   try {
//     const response = await fetch('/api/login/', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify({ username, password }),
//     });

//     if (!response.ok) {
//       throw new Error('Login failed');   
//     }

//     const responseData = await response.json();
//     console.log(responseData);
//     alert('Вход выполнен!');

//   } catch (error) {
//     console.error('Error:', error);
//     throw error;
//   }
// };


// const loginAuthor = async (username, password) => {
//   try {
//     const response = await fetch('/api/login/', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify({ username, password }),
//     });

//     if (!response.ok) {
//       throw new Error('Login failed');
//     }

//     const responseData = await response.json();
//     console.log(responseData);
//     alert('Вход выполнен!');

//   } catch (error) {
//     console.error('Error:', error);
//     throw error;
//   }
// };
var name
var last_name
var username
const loginAuthor = async (username, password) => {
  try {
    const response = await fetch('/api/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });

    const responseData = await response.json();
    console.log(responseData);
    alert('Вход выполнен!');

    // Fetch user data after successful login
    const authorResponse = await fetch('/users/authorview/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!authorResponse.ok) {
      throw new Error('Failed to fetch user data');
    }

    const authorData = await authorResponse.json();
    name = authorData.first_name;
    last_name = authorData.last_name;
    console.log(last_name);
    username = authorData.username;
    console.log(username);
    console.log(authorData);

    // ... do something with the author object ...

  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
};
if (currentURL === '/users/login/') {
  console.log(currentURL);
  document.getElementById('login-form').addEventListener('submit', (e) => {
    e.preventDefault()
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;
    loginAuthor(username, password);
    
    const userInfoContainer = document.getElementById('userInfo');
    userInfoContainer.innerHTML = `
    <p>Имя: ${name}</p>
    <p>Фамилия: ${last_name}</p>
    <p>Имя пользователя: ${username}</p>
    `;
  });
}


const logoutAuthor = async () => {
  try {
    const response = await fetch('/users/api/logout/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (response.ok) {
      alert('выход выполнен')
      console.log('Logout successful');
    } else {
      throw new Error('выход не выполнен');
    }
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
};

if (currentURL == '/users/logout/') {
console.log(currentURL);
  document.querySelector('#logout-btn').addEventListener('click', (e) => {
    e.preventDefault();
    logoutAuthor();
  })
};










// Fetch function for AuthorView view
// const getAuthor = async () => {
//   try {
//     const response = await fetch('/api/author/', {
//       method: 'GET',
//       headers: {
//         'Content-Type': 'application/json',
//         Authorization: `Bearer ${localStorage.getItem('jwt')}`, // Assuming you store the JWT in localStorage
//       },
//     });

//     if (!response.ok) {
//       throw new Error('Unauthorized');
//     }

//     const data = await response.json();
//     return data;
//   } catch (error) {
//     console.error('Error:', error);
//     throw error;
//   }
// };

// // Example HTML template for demonstration
// const loginForm = document.querySelector('#login-form');
// const authorData = document.querySelector('#author-data');

// loginForm.addEventListener('submit', async (event) => {
//   event.preventDefault();

//   const username = event.target.elements.username.value;
//   const password = event.target.elements.password.value;

//   try {
//     const token = await loginAuthor(username, password);
//     localStorage.setItem('jwt', token);
//     authorData.textContent = 'Fetching author data...';

//     const author = await getAuthor();
//     authorData.textContent = `Author ID: ${author.id}, Username: ${author.username}`;
//   } catch (error) {
//     console.error('Error:', error);
//     authorData.textContent = 'Failed to fetch author data';
//   }
// });
// if (currentURL == ' api/login/') {
  
// }

// function fetchDataFromBackend() {
//     const parentDiv = document.querySelector('.mydiv');
//     fetch('api')
//       .then(response => response.json())
//       .then(data => {
//         console.log(data);
//         data.forEach(obj => {
//           const colDiv = document.createElement('div');
//           colDiv.classList.add('col-md-4');

//           const cardDiv = document.createElement('div');
//           cardDiv.classList.add('card', 'mb-4');

//           const imgElement = document.createElement('img');
//           imgElement.src = obj.photo;
//           imgElement.alt = obj.title;
//           imgElement.classList.add('card-img-top');

//           const cardBodyDiv = document.createElement('div');
//           cardBodyDiv.classList.add('card-body', 'text-center');

//           const cardTitle = document.createElement('h5');
//           const cardLink = document.createElement('a');
//           cardLink.href = `/blog/detail/${obj.id}`;
//           cardLink.style.textDecoration = 'none';
//           cardLink.textContent = obj.title;
          
//           cardTitle.appendChild(cardLink);
//           cardBodyDiv.appendChild(cardTitle);

//           cardDiv.appendChild(imgElement);
//           cardDiv.appendChild(cardBodyDiv);

//           colDiv.appendChild(cardDiv);

//           parentDiv.appendChild(colDiv);
//         });

//         console.log(data); 
//       })
//       .catch(error => {
//         console.error('Error:', error);
//       });
//   }

// if (currentURL === '/') {
//   fetchDataFromBackend();
//   console.log(currentURL);
// }


// function fetchDataFromBackend(pageNumber = 1) {
//     const parentDiv = document.querySelector('.mydiv');
//     fetch(`api/?page=${pageNumber}`)
//         .then(response => response.json())
//         .then(data => {
//             parentDiv.innerHTML = ''; // Очистить существующий контент

//             data.results.forEach(obj => {
//                 const colDiv = document.createElement('div');
//                 colDiv.classList.add('col-md-4');

//                 const cardDiv = document.createElement('div');
//                 cardDiv.classList.add('card', 'mb-4');

//                 const imgElement = document.createElement('img');
//                 imgElement.src = obj.photo;
//                 imgElement.alt = obj.title;
//                 imgElement.classList.add('card-img-top');

//                 const cardBodyDiv = document.createElement('div');
//                 cardBodyDiv.classList.add('card-body', 'text-center');

//                 const cardTitle = document.createElement('h5');
//                 const cardLink = document.createElement('a');
//                 cardLink.href = `/blog/detail/${obj.id}`;
//                 cardLink.style.textDecoration = 'none';
//                 cardLink.textContent = obj.title;

//                 cardTitle.appendChild(cardLink);
//                 cardBodyDiv.appendChild(cardTitle);

//                 cardDiv.appendChild(imgElement);
//                 cardDiv.appendChild(cardBodyDiv);

//                 colDiv.appendChild(cardDiv);

//                 parentDiv.appendChild(colDiv);
//             });

//             // Обновить ссылки пагинации
//             updatePagination(data.previous, data.next);

//             console.log(data);
//         })
//         .catch(error => {
//             console.error('Ошибка:', error);
//         });
// }

// function updatePagination(previousPage, nextPage) {
//     const paginationDiv = document.querySelector('.pagination ul');
//     paginationDiv.innerHTML = '';

//     if (previousPage) {
//         const previousLink = createPaginationLink(previousPage, 'Предыдущий');
//         paginationDiv.appendChild(previousLink);
//     }

//     const currentPage = document.createElement('li');
//     currentPage.classList.add('page-item', 'active');
//     currentPage.innerHTML = `<span class="page-link">Страница 1</span>`;
//     paginationDiv.appendChild(currentPage);

//     if (nextPage) {
//         const nextLink = createPaginationLink(nextPage, 'Следующий');
//         paginationDiv.appendChild(nextLink);
//     }
// }

// function createPaginationLink(pageURL, label) {
//     const link = document.createElement('a');
//     link.classList.add('page-link');
//     link.href = `#${pageURL}`;
//     link.textContent = label;
//     link.addEventListener('click', event => {
//         event.preventDefault();
//         const pageNumber = new URLSearchParams(pageURL).get('page');
//         fetchDataFromBackend(pageNumber);
//     });

//     const listItem = document.createElement('li');
//     listItem.classList.add('page-item');
//     listItem.appendChild(link);

//     return listItem;
// }

// if (currentURL === '/') {
//     fetchDataFromBackend();
//     console.log(currentURL);
// }





//
//function fetchDataFromBackend(pageNumber = 1) {
//  const parentDiv = document.querySelector('.mydiv');
//  fetch(`api/?page=${pageNumber}`)
//    .then(response => response.json())
//    .then(data => {
//      parentDiv.innerHTML = ''; // Clear the existing content
//
//      data.results.forEach(obj => {
//        const colDiv = document.createElement('div');
//        colDiv.classList.add('col-md-4');
//
//        const cardDiv = document.createElement('div');
//        cardDiv.classList.add('card', 'mb-4');
//
//        const imgElement = document.createElement('img');
//        imgElement.src = obj.photo;
//        imgElement.alt = obj.title;
//        imgElement.classList.add('card-img-top');
//
//        const cardBodyDiv = document.createElement('div');
//        cardBodyDiv.classList.add('card-body', 'text-center');
//
//        const cardTitle = document.createElement('h5');
//        const cardLink = document.createElement('a');
//        cardLink.href = `/blog/detail/${obj.id}`;
//        cardLink.style.textDecoration = 'none';
//        cardLink.textContent = obj.title;
//
//        cardTitle.appendChild(cardLink);
//        cardBodyDiv.appendChild(cardTitle);
//
//        cardDiv.appendChild(imgElement);
//        cardDiv.appendChild(cardBodyDiv);
//
//        colDiv.appendChild(cardDiv);
//
//        parentDiv.appendChild(colDiv);
//      });
//
//      // Update pagination links
//      updatePagination(data.previous, data.next);
//
//      console.log(data);
//    })
//    .catch(error => {
//      console.error('Error:', error);
//    });
//}
//
//function updatePagination(previousPage, nextPage) {
//  const paginationDiv = document.querySelector('.pagination');
//  paginationDiv.innerHTML = '';
//
//  if (previousPage) {
//    const previousLink = createPaginationLink(previousPage, 'Предыдущий');
//    paginationDiv.appendChild(previousLink);
//  }
//
//  const currentPage = document.createElement('span');
//  currentPage.classList.add('page-link', 'active');
//  currentPage.textContent = 'Страница 1';
//  paginationDiv.appendChild(currentPage);
//
//  if (nextPage) {
//    const nextLink = createPaginationLink(nextPage, 'Следующий');
//    paginationDiv.appendChild(nextLink);
//  }
//}
//
//function createPaginationLink(pageURL, label) {
//  const link = document.createElement('a');
//  link.classList.add('page-link');
//  link.href = `#${pageURL}`;
//  link.textContent = label;
//  link.addEventListener('click', event => {
//    event.preventDefault();
//    const pageNumber = new URLSearchParams(pageURL).get('page');
//    fetchDataFromBackend(pageNumber);
//  });
//
//  const listItem = document.createElement('li');
//  listItem.classList.add('page-item');
//  listItem.appendChild(link);
//
//  return listItem;
//}
//
//if (currentURL === '/') {
//  fetchDataFromBackend();
//  console.log(currentURL);
//}


//
//  function fetchDataFromBackend() {
//    const parentDiv = document.querySelector('.mydiv');
//    fetch('api')
//      .then(response => response.json())
//      .then(data => {
//        data.forEach(obj => {
//          const colDiv = document.createElement('div');
//          colDiv.classList.add('col-md-4');
//
//          const cardDiv = document.createElement('div');
//          cardDiv.classList.add('card', 'mb-4');
//
//          const imgElement = document.createElement('img');
//          imgElement.src = obj.photo;
//          imgElement.alt = obj.title;
//          imgElement.classList.add('card-img-top');
//
//          const cardBodyDiv = document.createElement('div');
//          cardBodyDiv.classList.add('card-body', 'text-center');
//
//          const cardTitle = document.createElement('h5');
//          const cardLink = document.createElement('a');
//          cardLink.href = `/blog/detail/${obj.id}`;
//          cardLink.style.textDecoration = 'none';
//          cardLink.textContent = obj.title;
//
//          cardTitle.appendChild(cardLink);
//          cardBodyDiv.appendChild(cardTitle);
//
//          cardDiv.appendChild(imgElement);
//          cardDiv.appendChild(cardBodyDiv);
//
//          colDiv.appendChild(cardDiv);
//
//          parentDiv.appendChild(colDiv);
//        });
//
//        console.log(data);
//      })
//      .catch(error => {
//        console.error('Error:', error);
//      });
//  }
//
//  if (currentURL === '/') {
//    fetchDataFromBackend();
//    console.log(currentURL);
//  }
