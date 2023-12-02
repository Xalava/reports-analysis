// Usage
// 1. Open the browser at the right URL (change year)
// 2. Open the console and paste the code below, then arrow up and enter
// 3. Move from downloads to the right folder. 


// Get all the elements with the specified class
myFunction = () => {console.log('My Function')}

const selector = '.imf-result-item__file-download--pdf'

const pdfElements = document.querySelectorAll(selector)

// Loop through each element and trigger the click event
pdfElements.forEach((element) => {
	// element.click();
	setTimeout(() => {
		// Code to be executed after the random time delay
		const link = element.getAttribute('href')
		window.open(link, '_blank')
	}, Math.floor(Math.random() * 301) + 200);
});

// Easier to copy and paste
document.querySelectorAll('.imf-result-item__file-download--pdf').forEach((element) => {
	setTimeout(() => {
		const link = element.getAttribute('href')
		window.open(link, '_blank')
	}, Math.floor(Math.random() * 701) + 200)
});
