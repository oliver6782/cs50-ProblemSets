function get_cities() {
    var selected_province = document.getElementById("province").value;
    var cityDropdown = document.getElementById("city");

    fetch(`/get_cities/${selected_province}`)
        .then(response => response.json())
        .then(city_names => {
           
            cityDropdown.innerHTML = '';
            
            city_names.forEach(city => {
                var option = document.createElement('option');
                option.value = city;
                option.text = city;
                cityDropdown.add(option);
            });
        })
        .catch(error => console.error('Error:', error));
}



document.querySelector('form').addEventListener('submit', function(event) {
    
    var inputElement1 = document.getElementById('首年衰减');
    var inputElement2 = document.getElementById('线性衰减');
    var inputElement3 = document.getElementById('运维费用');
    var inputElement4 = document.getElementById('收益率');
    
    if (inputElement1.value === '') {
        inputElement1.value = '1.5'; 
    }
    if (inputElement2.value === '') {
        inputElement2.value = '0.4'; 
    }
    if (inputElement3.value === '') {
        inputElement3.value = '0.05'; 
    }
    if (inputElement4.value === '') {
        inputElement4.value = '8'; 
    }
});
