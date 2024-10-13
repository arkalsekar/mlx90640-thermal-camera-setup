console.log("Hello World")
const temperature = document.getElementById("temperature")
const url = "http://192.168.115.195:5000/"
console.log(temperature)

setInterval(() => {
    fetch(url)
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            let authors = data;
            console.log(authors.data)
            temperature.innerHTML = authors.data;
        })
}, 1000);