// To show the next element on click forward and backward, you can use JavaScript. 

let currentIndex = 0;
const elements = document.querySelectorAll('.bit_sized_element');

function showNextElement() {
  //elements[currentIndex].style.display = 'none';
  currentIndex = (currentIndex + 1) % elements.length;
  elements[currentIndex].style.display = 'block';
  
  elements[currentIndex].classList.remove("d-none")
  //document.body.classList.remove("spinner"),
  //elements.length >=3 ? elements[currentIndex].style.display = 'none' : ''

}

function showPreviousElement() {
  //elements[currentIndex].style.display = 'none';
  currentIndex = (currentIndex - 1 + elements.length) % elements.length;
  elements[currentIndex].style.display = 'block';
}

document.querySelector('.btn-next').addEventListener('click', showNextElement);
document.querySelector('.btn-prev').addEventListener('click', showPreviousElement); 


/* 
In this example, we first get all the elements with class name "element" and store them in an array. We also initialize a variable called `currentIndex` to keep track of which element is currently displayed.

We then define two functions: `showNextElement()` and `showPreviousElement()`. These functions hide the current element and show the next or previous element in the array, respectively.

Finally, we add event listeners to the "next" and "previous" buttons that call these functions when clicked.
 */