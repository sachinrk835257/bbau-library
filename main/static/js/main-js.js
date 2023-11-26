
// Wait for the DOM to be ready
document.addEventListener("DOMContentLoaded", function () {
    // all gloabal variables are here
    console.log("script is running")
    let spanYear = document.getElementById('currYear')

    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    spanYear.innerText = currentYear

    let nestedDropdown1 = document.getElementById('nestedDropdown1');
    nestedDropdown1.addEventListener('mouseover',()=>{
      console.log("mouse over")
      nestedDropdown1.nextElementSibling.classList.add('show')

    })
    nestedDropdown1.addEventListener('mouseleave',()=>{
      console.log("mouseleave")
      nestedDropdown1.nextElementSibling.classList.remove('show')
    })
    let nestedDropdown2 = document.getElementById('nestedDropdown2');
    nestedDropdown2.addEventListener('mouseover',()=>{
      console.log("mouse over")
      nestedDropdown2.nextElementSibling.classList.add('show')

    })
    nestedDropdown2.addEventListener('mouseleave',()=>{
      console.log("mouseleave")
      nestedDropdown2.nextElementSibling.classList.remove('show')
    })

});
