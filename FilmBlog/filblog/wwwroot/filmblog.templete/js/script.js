



//-------------------------------------Profil Sayfasi-------------------------------------------------
function selectPhoto(photoPath) {
    //Profil fotoğrafı seçme
    var currentPhoto = document.querySelector('.current-photo img');
    currentPhoto.src = photoPath;
}
//-----------------------------------------Giriş Sayfasi----------------------------------------------
function togglePasswordVisibility() {
    //Şifre görünürlüğü Giriş Sayfası İçin
    var passwordInput = document.getElementById("password");
    var button = document.querySelector("button");

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        button.textContent = "Şifreyi Gizle";
    } else {
        passwordInput.type = "password";
        button.textContent = "Şifreyi Görünür Yap";
    }
}

function validateForm() {
    //Kimlik doğrulama Giriş Sayfası için
    var usernameInput = document.getElementById("username");
    var passwordInput = document.getElementById("password");
    var loginError = document.getElementById("loginError");

    if (usernameInput.value !== "kullanici" || passwordInput.value !== "sifre") {
        loginError.textContent = "Kullanıcı adı veya şifre hatalı.";
        return false;
    } else {
        loginError.textContent = "";
        return true;
    }
}
//-------------------------------------------Kayit Sayfasi----------------------------------------------------------
function togglePasswordVisibility() {
    //Şifre görünürlüğü Kayıt Sayfası için
    var passwordInput = document.getElementById("password");
    var button = document.querySelector("button");

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        button.textContent = "Şifreyi Gizle";
    } else {
        passwordInput.type = "password";
        button.textContent = "Şifreyi Görünür Yap";
    }
}

function validateForm() {
    //Şifre uygunluğu Kayıt Sayfası İçin
    var passwordInput = document.getElementById("password");
    var passwordError = document.getElementById("passwordError");

    if (passwordInput.value.length < 6) {
        passwordError.textContent = "Şifre en az 6 karakter olmalıdır.";
        return false;
    } else {
        passwordError.textContent = "";
        return true;
    }
}
//--------------------------------------------------Film Sayfaları Slayt--------------------------------------------------------
let slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
    showSlides(slideIndex += n);
}

function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    let dots = document.getElementsByClassName("dot");
    if (n > slides.length) { slideIndex = 1 }
    if (n < 1) { slideIndex = slides.length }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].className += " active";
}

//------------------------------------------------------Yorum Ekle---------------------------------------------------------------------
function addComment() {
    // Formdaki değerleri al
    var name = document.getElementById('name').value;
    var comment = document.getElementById('comment').value;

    // Minimum 3 karakter kontrolü
    if (name.length < 3 || comment.length < 3) {
        alert("Ad ve yorum en az 3 karakter olmalıdır.");
        return;
    }

    // Yeni bir list elemanı oluştur
    var listItem = document.createElement('li');
    
    // Yorumun uzunluğunu kontrol et ve 80 karaktere ulaştığında alt satıra geçir
    if (comment.length > 80) {
        comment = comment.replace(/(.{80})/g, '$1\n');
    }

    // List elemanına içerik ekle
    listItem.innerHTML = '<strong>' + name + ':</strong> ' + comment;

    // Yorum listesine ekle
    document.getElementById('commentList').appendChild(listItem);

    // Formu sıfırla
    document.getElementById('commentForm').reset();
}

