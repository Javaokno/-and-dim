document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('weatherForm').addEventListener('submit', function(e) {
        e.preventDefault();
        var destination = document.getElementById('destination').value;
        if (destination) {
            fetchWeather(destination);
        }
    });

    function fetchWeather(destination) {
        fetch(`/get-weather?destination=${encodeURIComponent(destination)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => displayWeatherResults(data))
            .catch(error => {
                console.error('Fetch error:', error);
                displayError('无法获取天气数据，请检查目的地名称或网络连接。');
            });
    }

    function displayWeatherResults(data) {
        const weatherResultElement = document.getElementById('weatherResult');
        if (data.error) {
            displayError(data.error);
        } else {
            weatherResultElement.innerHTML = `
                <h2>${data.name}</h2>
                <p>温度: ${data.main.temp} °C</p>
                <p>天气状况: ${data.weather[0].description}</p>
            `;
        }
    }

    function displayError(message) {
        const weatherResultElement = document.getElementById('weatherResult');
        weatherResultElement.innerHTML = `<p>${message}</p>`;
    }
});