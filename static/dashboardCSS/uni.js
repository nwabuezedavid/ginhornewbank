const btn__open = document.querySelector('.btn__open')
const btn = document.querySelector('.btn__d')
const container = document.querySelector('.nav')
btn.addEventListener('click',()=>{
    container.classList.toggle('open_nav')
})
btn__open.addEventListener('click',()=>{
    container.classList.toggle('open_nav')
})