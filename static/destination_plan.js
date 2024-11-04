// static/js/destination_plan.js
var map = L.map('mapContainer').setView([51.505, -0.09], 13); // 初始化地图，设置默认视角

// 添加地图瓦片图层，使用 OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
}).addTo(map);

// 搜索功能
document.getElementById('searchForm').addEventListener('submit', function(e) {
    e.preventDefault();
    var searchQuery = document.getElementById('searchInput').value;
    // 执行搜索并定位到搜索结果
    // 此处代码需要根据实际 API 调整
});

// 地图标记功能
function addMarker(lat, lng) {
    var marker = L.marker([lat, lng]).addTo(map);
    // 绑定点击事件或其他交互
}