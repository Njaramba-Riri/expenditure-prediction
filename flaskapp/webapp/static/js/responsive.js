document.addEventListener('DOMContentLoaded', (event) => {
  var loader = document.querySelector('.loader-content');
  var content = document.querySelector('#page-contents');

  window.addEventListener('load', () => {
    if(content){
      loader.classList.add('hidden');
      content.classList.add('visible');
    }else{
      loader.classList.remove('hidden');
    }
  })
});

document.addEventListener('DOMContentLoaded', (event) => {
  var element = document.getElementById("messages");
  var timer;
  
  function startTimer(){
    timer = setTimeout(function(){
      if(element){
        element.classList.add('close');
      }
    }, 4000);
  }

  function stopTimer(){
    clearTimeout(timer);
  }

  if(element){
    element.addEventListener('mouseover', stopTimer);
    element.addEventListener('mouseout', startTimer);
    element.addEventListener('click', function(){
      stopTimer();
      element.classList.add('close');
    });

    startTimer();
  }
});

document.addEventListener('DOMContentLoaded', () => {
  let form = document.getElementById('auth')
  let btn = document.getElementById('submit-btn');

  if (form){
    form.addEventListener('submit', () => {
      if(btn.classList.contains('loading')){
        btn.classList.remove('loading');
      }else{
        btn.classList.add('loading');      
      }      
    })
  }
    // setTimeout(() => {
    //   btn.classList.remove('loading');
    //   btn.classList.add('success');
    //   text.innerHTML = 'Login Successful.';
    // }, 2000)
});

// document.addEventListener("DOMContentLoaded", ()=>{
//     var error = document.getElementById("toCenter");
//     var errorWidth = error.clientWidth;
//     var errorHeight = error.clientHeight;
//     var viewportWidth = window.innerWidth;
//     var viewportHeight = window.innerHeight;
//     var leftPosition = (viewportWidth - errorWidth) / 2;
//     var topPosition = (viewportHeight - errorHeight);

//     error.style.left = leftPosition + 'px';
//     error.style.top = topPosition + 'px';
//     error.style.position = 'absolute';
// });

// document.addEventListener('DOMContentLoaded', () => {
//     const center = document.getElementById("toCenter");

//     const centerWidth = center.clientWidth;
//     const centerHeight = center.clientHeight;

//     const viewportWidth = window.innerWidth ;
//     const viewportHeight = window.innerHeight;

//     const leftPosition = (viewportWidth - centerWidth) / 2;
//     const topPosition = (viewportHeight - centerHeight);

//     center.style.left = leftPosition + 'px';
//     center.style.top = topPosition + 'px';
//     center.style.position = 'absolute';
// });

document.addEventListener('DOMContentLoaded', (event) => {
    const passwordFields = document.querySelectorAll(".password-field");
    const togglePasswords = document.querySelectorAll(".toggle-password");
  
    passwordFields.forEach((passwordField, index) => {
      const togglePassword = togglePasswords[index];
  
      if (togglePassword) {
        togglePassword.addEventListener('click', function() {
          if (passwordField.type === 'password') {
            passwordField.type = 'text';
            togglePassword.className = 'far fa-eye';
          } else {
            passwordField.type = 'password';
            togglePassword.className = 'far fa-eye-slash';
          }
        });
      }
    });
});


/* Trigger flash modal */
$(document).ready(function () {
    var messages = "{{ get_flashed_messages() }}";

    if (typeof messages != 'undefined' && messages != '[]') {
        $("#myModal").modal();
    };
});

function hideFlashed() {
    var flashMessages = document.getElementById('flash-messages');
    flashMessages.style.display = 'block';
}

document.addEventListener('DOMContentLoaded', (event) => {
    const dropdownlink = document.querySelector("#dropdownMenulink");
    const dropdownmenu = document.querySelector("#dropdownMenu");
  
    if (dropdownlink && dropdownmenu) {
      dropdownlink.addEventListener('click', function(){
        dropdownmenu.className === "show-dropdown";
      });
    }
  });

document.addEventListener('DOMContentLoaded', (event) => {
  var details = document.getElementById("details");
  var features = document.getElementById("features");

  details.addEventListener('click', ()=>{
    if(features){
      if(features.classList.contains('show')){
        features.classList.remove('show');
      }else{
        features.classList.add('show');
      } 
    }
  });

  var feedback = document.getElementById("Disatisfied");
  var mawoni = document.getElementById("mawoni");
  
  feedback.addEventListener('click', () => {
      if(mawoni.classList.contains("active")){
          mawoni.classList.remove("active");
      }else{
          mawoni.classList.add("active");
      }
  });

  var icons = document.querySelectorAll("ion-icon");
  var modal = document.getElementById("feed-modal");
  var content = document.getElementById("feed-content");
  var close = document.getElementsByClassName("close")[0];

  icons.forEach(function(icon){
    icon.addEventListener('click', function(){
      icons.forEach(function(otherIcons){
          otherIcons.classList.remove('active');
        });

      this.classList.toggle('active');

      function showMessage(message){
        document.getElementById("modalText").innerText = message;
        modal.style.display = "block";
      }   
      showMessage;

      close.onclick = function(){
        modal.style.display = "none";
      }
      
      window.onclick = function(event){
        if (event.target == modal){
          modal.style.display = "none";
        }
      }
    });
  });
});

document.addEventListener('DOMContentLoaded', (event) => {
    const users = document.querySelector("#goers");
    const reports = document.getElementById("reports");
    const model = document.querySelector("#model");
    const sema = document.querySelector("#sema");
    const user = document.querySelector("#user");
  
   if (users) {
      users.addEventListener('click', function(){
        window.location.href = "{{ url_for('admin.users') }}";
      });
  }
  
    if (reports) {
      reports.addEventListener('click', function(){
        window.location.href = "{{ url_for('/letsgo/admin/dashboard/') }}";
      });
    }
  
    if (model) {
    model.addEventListener('click', function(){
      window.location.href = "{{ url_for('.reports') }}";
    });
  }
  
  if (sema) {
    sema.addEventListener('click', function(){
      window.location.href = "{{ url_for('.feedback') }}";
    });
  }
  
  if (user) {
    user.addEventListener('click', function(){
      window.location.href = "{{ url_for('.profile') }}";
    });
  }
});
  
//adding hovered class to selected list item
document.addEventListener('DOMContentLoaded', (event) => {
  let sidebar_list = document.querySelectorAll(".savigation li");

  function activeLink() {
      sidebar_list.forEach((items) => {
          items.classList.remove("hovered");

      });
      this.classList.add("hovered");

      localStorage.setItem("activeItem", this.className);
  }
  sidebar_list.forEach((item) =>  {
    item.addEventListener("click", activeLink)
  });

  let activeItemClass = localStorage.getItem("activeItem");

  if (activeItemClass){
    let activeItem = document.querySelector(`${activeItemClass}`);
    if (activeItem){
      activeItem.classList.add("hovered");
    }
  }

  let main =  document.querySelector(".main-dash");
  let sidebar = document.querySelector(".savigation");
  let toggle = document.querySelector(".toggle");

  if (toggle){
    toggle.onclick = function () {
      sidebar.classList.toggle("active");
      main.classList.toggle("active");
    };    
  }
});

// Scroll behaviour on the top bar
document.addEventListener("DOMContentLoaded", (e) => {
  var topbar = document.querySelector("#topbar");

  window.onscroll = function() {scrollFunction()};
  function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
      topbar.classList.add("scrolled"); 
    } else {
      topbar.classList.remove("scrolled");
    }
  };
});


// document.addEventListener('DOMContentLoaded', function() {
//   let items = document.querySelectorAll('.savigation ul li a'); // Corrected the class name from '.savigation' to '.navigation'

//   // Function to remove 'hovered' class from all items and add it to the clicked item
//   function activeLink(event) {
//     event.preventDefault();

//     // Remove 'active' and 'hovered' classes from all items
//     items.forEach((item) => {
//       item.classList.remove('active', 'hovered');
//     });

//     this.classList.add('active', 'hovered'); // Moved this line after the forEach loop to ensure the clicked item gets the 'active' and 'hovered' classes

//     // Save the active item to localStorage
//     localStorage.setItem('activeItem', '.' + this.className.replace(/ /g, '.'));

//     // Fetch the new page content
//     let content  = document.getElementById("dash-content");

//     fetch(this.href)
//       .then(response => response.text())
//       .then(data => {
//         // Insert the new content into the DOM
//         content.innerHTML = data;
//       })
//       .catch(error => console.error('Error:', error));
//   }

//   function handleClick(event) {
//     // Check if the clicked element is an anchor tag
//     if (event.target.tagName === 'A') {
//       event.preventDefault(); // Prevent the default action of the anchor tag

//       // Fetch the new page content
//       fetch(event.target.href)
//         .then(response => response.text())
//         .then(data => {
//           // Insert the new content into the #dash-content element
//           content.innerHTML = data;
//         })
//         .catch(error => console.error('Error:', error));
//     }
//   }

//   // Attach the handleClick function to the click event of the #dash-content element
//   let content = document.getElementById("dash-content"); // Moved this line outside the activeLink function
//   content.addEventListener('click', handleClick);

//   // Attach the activeLink function to the click event of each item
//   items.forEach((item) => {
//     item.addEventListener('click', activeLink);

//     // Add 'hovered' class when mouse enters
//     item.addEventListener('mouseover', function() {
//       this.classList.add('hovered');
//     });

//     // Remove 'hovered' class when mouse leaves
//     item.addEventListener('mouseout', function() {
//       if (!this.classList.contains('active')) {
//         this.classList.remove('hovered');
//       }
//     });
//   });

//   // On page load, get the class of the last clicked item from localStorage
//   let activeItemClass = localStorage.getItem('activeItem');

//   // If there is a class in localStorage, add the 'hovered' class to the corresponding item
//   if (activeItemClass) {
//     let activeItem = document.querySelector(activeItemClass);
//     if (activeItem) {
//       activeItem.classList.add('hovered');
//     }
//   }
// });




// Searching Users Table.

document.addEventListener('DOMContentLoaded', (event) => {
  search = document.getElementById('search');
  
  if (search) {
    search.addEventListener('keyup', function() {
      var input, filter, table, tr, td, i, j, txtValue;
      input = document.getElementById('search');
      filter = input.value.toUpperCase();
      table = document.getElementById('users');
      tr = table.getElementsByTagName('tr');
      
      for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName('td');
        for (j = 0; j < tr.length; j++){
          if (td[j]) {
            txtValue = td[j].textContent || td[j].innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1){
              td[j].innerHTML = txtValue.replace(new RegExp(filter, 'gi'), (match) =>{
                return `<span class='txt-high'>${match}</span>`;
              });
              tr[i].classList.remove('hide');
              break;
            }else {
              tr[i].classList.add('hide');
              tr[i].style.setProperty('--delay', i/25 + 's');
            }
          }
        }
      }

      if (filter == ''){
        const highlighted = document.querySelectorAll('.txt-high');
        highlighted.forEach((highlight)=>{
          highlight.outerHTML = highlight.innerHTML;
        });
      }
    });
  }
});

document.addEventListener("DOMContentLoaded", (event) => {
  const dropdown = document.getElementById("dropdown");
  const dropList = document.querySelector(".dropdown")

  function activeDropdown() {
    if (dropList.classList.contains('hover')) {
      dropList.classList.remove('hover');
    } else {
      dropList.classList.add('hover');
    }
  }
  
  if(dropdown){
    dropdown.addEventListener('mouseover', activeDropdown);
    dropList.addEventListener('mouseout', activeDropdown);

    setTimeout(function (){
      dropList.classList.remove('hover');
    }, 2000);
  }
});

document.addEventListener("DOMContentLoaded", (e) => {
  var bar = document.querySelector("#navigation");
  
  window.onscroll = function() {scrollPage()};
  function scrollPage() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
      bar.classList.add("scrolled"); 
    } else {
      bar.classList.remove("scrolled");
    }
  };
})
