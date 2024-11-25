document.addEventListener('DOMContentLoaded', function() {
    // Function to fetch data from the server
    function fetchData() {
        fetch('/get_data')
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error(data.error);
                } else {
                    // Update the HTML elements with the fetched data
                    document.getElementById('temperature-display').textContent = data.temperature + '°C';
                    document.getElementById('humidity-display').textContent = data.humidity + '%';
                    document.getElementById('light-display').textContent = data.light + ' lux';
                    document.getElementById('time-display').textContent = data.time;
                }
            })
            .catch(error => console.error('Error fetching data:', error));
    }

    // Fetch data when the page loads
    fetchData();

    // Optionally, set an interval to fetch data periodically
    setInterval(fetchData, 5000); // Fetch data every 5 seconds
});

// Initial data load
updateData();


function updateCharts(data) {
    // Cập nhật biểu đồ nhiệt độ
    const temperatureChartCtx = document.getElementById('temperatureChart').getContext('2d');
    new Chart(temperatureChartCtx, {
        type: 'line',
        data: {
            labels: [data.thoigian],
            datasets: [{
                label: 'Nhiệt độ',
                data: [data.temperature],
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        }
    });

    // Cập nhật biểu đồ ánh sáng
    const lightChartCtx = document.getElementById('lightChart').getContext('2d');
    new Chart(lightChartCtx, {
        type: 'line',
        data: {
            labels: [data.thoigian],
            datasets: [{
                label: 'Ánh sáng',
                data: [data.light],
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        }
    });

    // Cập nhật biểu đồ độ ẩm
    const humidityChartCtx = document.getElementById('humidityChart').getContext('2d');
    new Chart(humidityChartCtx, {
        type: 'line',
        data: {
            labels: [data.thoigian],
            datasets: [{
                label: 'Độ ẩm',
                data: [data.humidity],
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        }
    });
}
