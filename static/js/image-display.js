document.querySelector('#image_origin').addEventListener('input', (e) => {
document.querySelector('.image-hint').style.display = 'none';
document.querySelector('.image-display').style.backgroundImage = 'url("' + URL.createObjectURL(event.target.files[0]) + '")';
});
