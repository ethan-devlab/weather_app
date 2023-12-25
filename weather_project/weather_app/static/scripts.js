const api = document.getElementById("api");
const value = api.value
const url = `https://api.openweathermap.org/data/2.5/weather?q=London&appid=${value}`;
const button = document.getElementById("auth");
button.addEventListener("click", makeRequest);

async function makeRequest() {
//    console.log(api.value);
    try {
      const response = await fetch(url);
//      console.log('response.status: ', response.status);
      const data = await response.json();
      console.log(data['cod']);
      if (response.status == 401){
        alert("無效API");
      }
    } 
    catch (err) {
       console.log(err);
    }
  }

function signUpSuccess(){
    alert("註冊成功！Sign Up Successfully!");
}