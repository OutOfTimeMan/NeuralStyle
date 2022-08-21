

let select = document.querySelector('select');
select.addEventListener('change', (e) => {
  let image = document.querySelector('.style-image-display')
  console.log(image)
  switch (e.target.value){
  case '1':
    image.style.backgroundImage = "url('/static/styles_image/1.jpg')"
    console.log('case 1')
    break;
  case '2':
    image.style.backgroundImage = "url('/static/styles_image/2.jpg')"
    console.log('case 2')
    break;
  };
});