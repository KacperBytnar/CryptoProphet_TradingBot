// script.js

var socket = io.connect('http://' + document.domain + ':' + location.port);

var headerElement = document.getElementById('trading-header');
var logoElement = document.getElementById('spin');

document.getElementById('start-trading-btn').addEventListener('click', function() {
    // Call the start trading route when the button is clicked
    axios.get('/start-trading')
        .then(function(response) {
            headerElement.textContent = "Currently trading BTC-USDT on 1m interval with baseline Short-Long Strategy";
            console.log(response.data);  // Log the response (optional)
            logoElement.style.animation="rotate 3s linear infinite";
            headerElement.style.color = 'black'; // Change the color to red
        })
        .catch(function(error) {
            console.error(error);
        });
});

document.getElementById('switch-trading-btn').addEventListener('click', function() {
    // Call the start trading route when the button is clicked
    axios.get('/start-trading')
        .then(function(response) {
            headerElement.innerHTML = "Currently trading BTC-USDT on 1m interval using AI Empowered Breakout Strategy";
            console.log(response.data);  // Log the response (optional)
            headerElement.style.color = 'blue'; // Change the color to red
        })
        .catch(function(error) {
            console.error(error);
        });
});

document.getElementById('stop-trading-btn').addEventListener('click', function() {
    // Call the stop trading route when the button is clicked
    axios.get('/stop-trading')
        .then(function(response) {
            headerElement.innerHTML = "Trading has been stopped";
            headerElement.style.color = 'red'; // Change the color to red
            logoElement.style.animation="rotate 30000000s linear infinite";
            console.log(response.data);  // Log the response (optional)
        })
        .catch(function(error) {
            console.error(error);
        });
});

var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('trade_report', function(data) {
    var tradeList = document.getElementById('trade-list');

    var cumProfitsElement = document.getElementById('cum-profits');
    cumProfitsElement.innerHTML = data.time + ' | CumProfits: ' + data.cum_profits;

    // Apply different colors based on CumProfits value
    if (data.cum_profits > 0) {
        cumProfitsElement.style.color = 'green';
    } else if (data.cum_profits === 0) {
        cumProfitsElement.style.color = 'blue';
    } else {
        cumProfitsElement.style.color = 'red';
    }

    // Create a Bootstrap card element
    var card = document.createElement('div');
    card.className = 'card m-3';

    // Create card header
    var cardHeader = document.createElement('div');
    cardHeader.className = 'card-header';
    cardHeader.textContent = data.time + ' | ' + data.going;
    card.appendChild(cardHeader);

    // Create card body
    var cardBody = document.createElement('div');
    cardBody.className = 'card-body';

    // Format the trade report data
    var reportText = data.time + ' \n Base_Units = ' + data.base_units +
        ' | \nQuote_Units = ' + data.quote_units + ' | \nPrice = ' + data.price + '<br>' +
        data.time + ' | Profit = ' + data.real_profit + ' | CumProfits = ' + data.cum_profits;

    // Create a paragraph element for the trade report
    var reportParagraph = document.createElement('p');
    reportParagraph.className = 'card-text';
    reportParagraph.innerHTML = reportText;
    cardBody.appendChild(reportParagraph);

    card.appendChild(cardBody);

    // Append the card to the trade list
    tradeList.appendChild(card);
});