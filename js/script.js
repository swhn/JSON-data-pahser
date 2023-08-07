let data = [];
let hasSearched = false;
// Load the data from JSON file
const loadData = async () => {
  try {
    const response = await fetch('https://docs.google.com/spreadsheets/d/e/2PACX-1vSdTQsJJI5gVKOjlrEwX7c6xjHItFTJ2rwbD9EbLtsOAXhtLYKIgE2HtJ0t8Nqwm0mpFSD_VuWgHV1q/pub?gid=0&single=true&output=csv');
    const csvData = await response.text();

    // Parse CSV data into objects
    data = Papa.parse(csvData, { header: true }).data;

    // Call the function to render the results
    // renderResults([]);
  } catch (error) {
    console.error('Error loading data:', error);
    const resultsContainer = document.getElementById('results-container');
    resultsContainer.innerHTML = '<p>Error loading data.</p>';
  }
};

// Function to format date as DD-MM-YYYY
const formatDate = (date) => {
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = date.getFullYear();
  return `${day}-${month}-${year}`;
};

// Function to check if the date is a future date
const isFutureDate = (date) => {
  const today = new Date();
  return date >= today;
};

const getGoogleMapsEmbedURL = (plusCode) => {
  return `https://www.google.com/maps/embed/v1/place?key=AIzaSyAdbuKgityGoTos4q1g9hvbhehVJ2pg00A&q=${encodeURIComponent(plusCode)}`;
};
// Function to filter and render the search results
const renderResults = () => {
  const searchInput = document.getElementById('search-input').value.toLowerCase();
  const searchOption = document.getElementById('search-option').value;

  if (!searchInput && !searchOption && hasSearched ) {
    // If either searchInput or searchOption is empty, show an alert and do nothing
    alert('Please enter serial number and choose an equiptment type.');
    return;
  }
 
  const filteredResults = data.filter((result) => {
    const titleMatch = result.sn.toLowerCase() === searchInput;
    const optionMatch = searchOption === '' || result.option === searchOption;
    return titleMatch && optionMatch;
  });

  const resultsContainer = document.getElementById('results-container');
  resultsContainer.innerHTML = '';

  if (filteredResults.length === 0) {
    const noResultsText = document.createElement('p');
    noResultsText.classList.add('no-results');
    noResultsText.innerHTML = 'No results found. If you think something is wrong, please contact <br> <a href="mailto:service@gma-myanmar.com">service@gma-myanmar.com</a>';
    resultsContainer.appendChild(noResultsText);
    return;
  }
  

  filteredResults.forEach((result) => {
    const resultDate = new Date(result.ewarrantyDate);
    const dateFormat = formatDate(resultDate);
    const eiDate = new Date(result.einstallDate);
    const eidFormat = formatDate(eiDate);
    const futureDate = isFutureDate(resultDate) ? 'Active' : 'Warranty Out';
    const mapsEmbedURL = getGoogleMapsEmbedURL(result.location); // Get the Google Maps embed URL from the plus code

    const template = `
      <div class="result-item">
        <img src="images/${result.image}" alt="${result.sn}">
        <img src="images/${result.ebrand}.png" alt="${result.ebrand}">
        <h3>SN: ${result.sn}</h3>
        <p>Type: ${result.etype}</p>
        <p>Brand: ${result.ebrand}</p>
        <p>Model: ${result.emodel}</p>
        <p>Installation Date: ${eidFormat}</p>
        <p>Warranty Date: ${dateFormat}</p>
        <p class="${isFutureDate(resultDate) ? 'future-date-yes' : 'future-date-no'}">Warranty Status: ${futureDate}</p>
        <p>Customer: ${result.customer}</p>
        <p>Location: ${result.location}</p>
        <iframe
        src="${mapsEmbedURL}"
        frameborder="0"
        style="border:0;"
        allowfullscreen=""
        aria-hidden="false"
        tabindex="0"
      ></iframe>

        <p class="anno">This device is a part of product of Golden Myanmar Alliance. For more information, please visit <a href="https://gma-myanmar.com"> our website </a></p>
      </div>
    `;

    resultsContainer.innerHTML += template;
  });
};

// Function to handle the search action (called by both click and enter key events)
const handleSearch = () => {
  const searchInput = document.getElementById('search-input').value.trim().toLowerCase();
  const searchOption = document.getElementById('search-option').value;

  if (!searchInput) {
    // If searchInput is empty, show an alert and do nothing
    alert('Please enter serial number.');
    return;
  }

  if (!searchOption) {
    // If searchOption is empty, show an alert and do nothing
    alert('Please choose an equipment type.');
    return;
  }

  hasSearched = true; // Set the flag to true after the first search

  renderResults();
};

// Call the function to load the data when the page loads
document.addEventListener('DOMContentLoaded', () => {
    loadData();

  const searchButton = document.getElementById('search-button');
  searchButton.addEventListener('click', handleSearch);

  // Listen for the Enter key press event on the search input
  const searchInput = document.getElementById('search-input');
  searchInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
      handleSearch();
    }
  });
  // hasSearched = false; // Set the flag to false initially
  
});

