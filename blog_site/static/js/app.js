// const createAuthor = () => {
//     const url = '/users/create_author/'; // Замените на фактический URL вашей API-конечной точки
  
//     const data = {
//       // Включите необходимые поля данных для создания автора
//       // Пример: имя, электронная почта и т.д.
//     };
  
//     fetch(url, {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//         // Включите любые дополнительные заголовки, если необходимо
//       },
//       body: JSON.stringify(data),
//     })
//       .then(response => response.json())
//       .then(result => {
//         // Обработка успешного ответа
//         console.log(result);
//       })
//       .catch(error => {
//         // Обработка ошибки
//         console.error(error);
//       });
//   };

const createAuthor = () => {
    const url = '/users/create_author/'; // Замените на фактический URL вашей API-конечной точки
    // const csrftoken = document.getElementById('token')
    // var form = document.getElementById('body');
    // var column = [];
    // for (var i = 0; i < form.rows.length; i++) {
    //   column.push(form.rows[i].cells[1].childNodes[0].value);
    // }
    // var form = document.getElementById('create-author-form');
    // var column = [];
    // for(var i = 0; i<form.rows.length; i++){
    //     column.push(form.rows[i].cells[1].childNodes[0].value);
    // }
    // var csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const csrf = document.getElementById('csrfmiddlewaretoken').value
    const firstNameInput = document.getElementById('first-name');
    const lastNameInput = document.getElementById('last-name');
    const usernameInput = document.getElementById('username');
   
    const passwordInput = document.getElementById('password');
  
    const data = {
      first_name: firstNameInput.value,
      last_name: lastNameInput.value,
      username: usernameInput.value,
      gender: 'm',
      password: passwordInput.value,
    };
  
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'utf-8',
        'X-CSRFToken':  `${csrf}`
        // Включите любые дополнительные заголовки, если необходимо
      },
      body: JSON.stringify(data),
    })
      .then(response => response.json())
  };
  
  const form = document.getElementById('create-author-form');
  form.addEventListener('submit', event => {
    event.preventDefault();
    createAuthor();
  });
  