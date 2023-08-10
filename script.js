let cities = []
fetch('./cities.json')
    .then((response) => response.json())
    .then(data => cities.push(...data))
console.log(cities)

let guest = 0
let latitude = -99
let longitude = -99
let properties = []

function datehandler() {
    
}

function showGuestsMenu() {
    document.getElementById('menu-guests').classList.remove('invisible')
}

function ApplyGuest() {
    document.getElementById('guestsInput').value = guest
    document.getElementById('numOfGuests').value = guest
    document.getElementById('menu-guests').classList.add('invisible')
}

function addGuest() {
    guest += 1
    document.getElementById('numOfGuests').innerHTML = guest
}

function reduceGuest() {
    if(guest>=1) guest -= 1
    document.getElementById('numOfGuests').innerHTML = guest
}

function showRangeMenu() {
    document.getElementById('menu-range').classList.remove('invisible')
}

function ApplyRange() {
    document.getElementById('rangeInput').value = document.getElementById('slider-1').value + ' - ' + document.getElementById('slider-2').value
    document.getElementById('menu-range').classList.add('invisible')
}

function selectLocation(value, lat, lng) {
    document.getElementById('searchInput').value = value
    document.getElementById('searchSuggestions').innerHTML = ''
    latitude = lat
    longitude = lng
    generateProperty()
}

async function search(keyword) {
    if(keyword.length >= 3) {
        const filteredCities = cities.filter(c => c.name.match(new RegExp(keyword, 'gi')))
        console.log(filteredCities)
        const html = filteredCities.slice(0, 5).map(location=> {return(`<li lat="${location.lat}" lng="${location.lng}" class="h-10 px-5 p-2 bg-gray-200 hover:bg-gray-300" onClick="selectLocation('${location.name}, ${location.country}', ${location.lat}, ${location.lng})">${location.name}, ${location.country}</li>`)}).join(' ')
        document.getElementById('searchSuggestions').innerHTML = html
    }
    else document.getElementById('searchSuggestions').innerHTML = ''
}


window.onload = function(){
    slideOne();
    slideTwo();
}

let sliderOne = document.getElementById("slider-1");
let sliderTwo = document.getElementById("slider-2");
let displayValOne = document.getElementById("range1");
let displayValTwo = document.getElementById("range2");
let minGap = 0;
let sliderTrack = document.querySelector(".slider-track");
let sliderMaxValue = document.getElementById("slider-1").max;

function slideOne(){
    if(parseInt(sliderTwo.value) - parseInt(sliderOne.value) <= minGap){
        sliderOne.value = parseInt(sliderTwo.value) - minGap;
    }
    displayValOne.textContent = sliderOne.value;
    fillColor();
}
function slideTwo(){
    if(parseInt(sliderTwo.value) - parseInt(sliderOne.value) <= minGap){
        sliderTwo.value = parseInt(sliderOne.value) + minGap;
    }
    displayValTwo.textContent = sliderTwo.value;
    fillColor();
}
function fillColor(){
    percent1 = (sliderOne.value / sliderMaxValue) * 100;
    percent2 = (sliderTwo.value / sliderMaxValue) * 100;
    sliderTrack.style.background = `linear-gradient(to right, #dadae5 ${percent1}% , #3264fe ${percent1}% , #3264fe ${percent2}%, #dadae5 ${percent2}%)`;
}


function ShowSearchAttributes() {
    alert(`Search: ${document.getElementById('searchInput').value}
Check-in: ${document.getElementById('input-checkin').value} 
Check-out: ${document.getElementById('input-checkout').value}  
Guests: ${guest}
Price range: ${document.getElementById('rangeInput').value}  
    `)
}

function ShowMap() {
    if(document.getElementById('searchInput').value.length >= 3 && latitude != -99 && longitude != -99) {
        map.setView([latitude, longitude], 13)
        properties.map(property => {
            if(property.price <= document.getElementById('slider-2').value && property.price >= document.getElementById('slider-1').value)
                L.tooltip().setLatLng([property.lat, property.lng]).setContent(property.name+'<br>Price:'+property.price).addTo(map);
        })
        document.getElementsByTagName('nav')[0].style.display = 'none'
        document.getElementById('map').classList.remove('invisible')
        document.getElementById('div-button').style.display = 'none'
    }
    else alert('Please select a location. If you have already typed a location yourself, please reselect it from the suggestions.')
}

function HideMap() { 
    document.getElementById('div-button').style.display = 'flex'
    document.getElementById('map').classList.add('invisible')
    document.getElementsByTagName('nav')[0].style.display = 'flex'
}


var map = L.map('map').setView([51.505, -0.09], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

L.marker([51.5, -0.09]).addTo(map)
    .bindPopup('A pretty CSS3 popup.<br> Easily customizable.')
    .openPopup();

var button = L.control({ position: 'topleft'})
button.onAdd = function() {
    const div = L.DomUtil.create('div')
    div.innerHTML = '<button id="showMapButton" class=" absolute h-8 px-5 py-2 mt-4 mr-4 bg-gray-800 text-white rounded-2xl z-10" onclick="HideMap()">ShowList</button>'
    return div
}
button.addTo(map)

function generateProperty() {
    properties = []
    maxProperty = 25
    minProperty = 10
    numOfProperty = Math.floor(Math.random() * (maxProperty - minProperty) ) + minProperty;
    for(let i=0; i<numOfProperty; i++) {
        let property = {
            lat: latitude+(Math.random() * (-0.01 - (-0.02)) + (-0.02)),
            lng: longitude+(Math.random() * (-0.01 - (-0.02)) + (-0.02)),
            name: 'Property ' + i,
            price: Math.floor(Math.random() * (9999 - 1000) ) + 1000,
        }
        properties.push(property)
    }
    console.log(properties)
}