// all gloabal variables are here
console.log("script is running")
let spanYear = document.getElementById('currYear');
console.log(spanYear)


const currentDate = new Date();
const currentYear = currentDate.getFullYear();
spanYear.innerText = currentYear

// Wait for the DOM to be ready
document.addEventListener("DOMContentLoaded", function () {
    // Get the button element
    var scrollToTopButton = document.getElementById("scrollToTopButton");

    // Add a click event listener to the button
    scrollToTopButton.addEventListener("click", function () {
        // Scroll to the top of the page smoothly
        window.scrollTo({
            top: 0,
            behavior: "smooth" // This provides a smooth scrolling effect
        });
    });
});
