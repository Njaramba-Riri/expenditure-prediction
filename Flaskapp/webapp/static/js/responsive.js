$(document).ready(function() {
    $('input[name="tarr"]').on('', function() {
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

$(function () {
  $("#slider").responsiveSlides({
    maxwidth: 600,
    speed: 50
  });
});

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

const togglePassword = document.querySelector('#togglePassword');
const password = document.querySelector('#id_password');

togglePassword.addEventListener('click', function () {
    if (password.type === 'password') {
        password.type = 'text';
        togglePassword.className = 'far fa-eye';
    } else {
        password.type = 'password';
        togglePassword.className = 'far fa-eye-slash';
    }
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

const dropdownlink = document.querySelector("#dropdownMenulink")
const dropdownmenu = document.querySelector("#dropdownMenu")

dropdownlink.addEventListener('click', function(){
    dropdownmmenu.className === "show-dropdown"
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
