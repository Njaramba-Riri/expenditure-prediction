$(document).ready(function() {
    $('input[name="tarr"]').on('change', function() {
        var selectedValue = $(this).val();
        if (selectedValue === 'Package Tour') {
            $('#pkg').show();
        } else if (selectedValue === 'Independent') {
            $('#pkg').hide();
        } else {
            $('#pkg').show();
        }
    });
});


function Package(){
    var selectedValue = document.getElementById('PKG');
    if (selectedValue === 'Package Tour') {
            $('#pkg').show();
        } else if (selectedValue === 'Independent') {
            $('#pkg').hide();
        } else {
            $('#pkg').show();
        }
}


function myFunction() {
  var x = document.getElementById("Nav");
  if (x.className === "navbar") {
    x.className += " responsive";
  } else {
    x.className = "navbar";
  }
}

$(document).ready(function(){
	$('#ProfileModall').click(function(){
  		$('#ProfileBackdrop').modal('show')
	});
});

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

function goToReset(){
    window.location.href = "{{ url_for('auth.forgotpass') }}"
}

function openPass() {
    popup.classList.add("pop-show")
}

function closePop() {
    popup.classList.remove("pop-show")
} 

$(document).ready(function () {
    var messages = "{{ get_flashed_messages() }}";

    if (typeof messages != 'undefined' && messages != '[]') {
        $("#myModal").modal();
    };
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
    flashMessages.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', (event) => {
    const dropdownlink = document.querySelector("#dropdownMenulink");
    const dropdownmenu = document.querySelector("#dropdownMenu");
  
    // Check if the elements exist
    if (dropdownlink && dropdownmenu) {
      dropdownlink.addEventListener('click', function(){
        dropdownmenu.className === "show-dropdown";
      });
    }
  });
  


function goBack(){
    window.history.back()
}

let popup = document.getElementById("pass");

function openPass() {
    popup.classList.add("pop-show")
    popup.classList.add("dark-back")
}

function closePop() {
    popup.classList.remove("pop-show")
}



function goToReset(){
    window.location.href = "{{ url_for('auth.forgotpass') }}"
}

document.addEventListener('DOMContentLoaded', (event) => {
    const users = document.querySelector("#users");
    const reports = document.getElementById("reports");
    const model = document.querySelector("#model");
    const sema = document.querySelector("#sema");
    const user = document.querySelector("#user");
  
    // Check if the elements exist
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
      sidebar_list.forEach((item) => {
          item.classList.remove("hovered");
      });
      this.classList.add("hovered");
  }

  sidebar_list.forEach((item) =>  item.addEventListener("mouseover", activeLink));

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


window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  var topbar = document.querySelector("#topbar");
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    topbar.classList.add("scrolled"); 
  } else {
    topbar.classList.remove("scrolled");
  }
}

$(document).ready(function() {
  // Get the active item from localStorage
  var activeItem = localStorage.getItem('activeItem');

  // If there's an active item saved, add the 'active' and 'hovered' classes to it
  if (activeItem) {
      $(activeItem).addClass('active hovered');
  }

  $("ul li a").not('.dash, .home, .dashapp, .users').click(function(e) {
      e.preventDefault(); // Prevent the default action of the anchor tag
      var page = $(this).attr('href'); // Get the href attribute of the clicked anchor tag

      // Remove 'active' and 'hovered' classes from all items
      $("ul li").removeClass('active hovered');

      // Add 'active' and 'hovered' classes to the clicked item
      $(this).addClass('active hovered');

      // Save the active item to localStorage
      localStorage.setItem('activeItem', '.' + $(this).attr('class').replace(/ /g, '.'));

      $("#dash-content").load(page); // Load the content of the page into the div with id 'content'
  }).hover(function() {
      $(this).addClass('hovered'); // Add 'hovered' class when mouse enters
  }, function() {
      // Only remove 'hovered' class if the item is not active
      if (!$(this).hasClass('active')) {
          $(this).removeClass('hovered'); // Remove 'hovered' class when mouse leaves
      }
  });
});


// Searching Users Table.
document.getElementById('search').addEventListener('keyup', function() {
  var input, filter, table, tr, td, i,j, txtValue;
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
          tr[i].style.display = '';
          break;
        }else {
          tr[i].style.display = 'none';
        }
      }
    }
  }
});

$('users').on('keyup', 'input', function() {
  var $row = $(this).closest('tr');
  $row.css('transition', 'opacity 0.5s ease-in-out');
  $row.css('opacity', '0');
  setTimeout(function() {
      $row.remove();
  }, 500); // delay in ms
});