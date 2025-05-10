const videoCon = document.querySelector('.fv')


let arrydlifr =['{% static "/assets/assets/main/ICON_VERSION5.mp4" %}',"/assets/assets/ICON_VERSION8.mp4"]
let ini = 0
let htmf = ""
function slide() {
    htmf = `
<video src= ${arrydlifr[ini]}  class="sliude"  ></video>
    
    `
    videoCon.innerHTML = htmf
const sliude = document.querySelector('.sliude')
sliude.play()

}

slide()

setInterval(() => {
    ini++ 
    console.log(ini);
    if( ini === arrydlifr.length ){

        ini=0 
    } 
slide()

}, 12000);





window.addEventListener('scroll',()=>{
    const navi = document.querySelector('.nav')
    navi.classList.toggle('bgd',window.scrollY > 0) 
})
const btn__bar = document.querySelector('.toggle_bar')
const product = document.querySelector('.carryo')
const child = document.querySelector('.carryo span')
const child2 = document.querySelector('.nav ul')
let kx = 0
                                                                                                                                       
btn__bar.addEventListener('click',()=>{
    child2.classList.toggle('dn')
    child2.style.display ="none"
    kx++
    if (kx == 2 ) {
        child2.style.display ="flex"
        kx = 0 
    }
    console.log(kx, 'skdkdk');
    
})
product.addEventListener('click',()=>{
    child.classList.toggle('df') 
    child.style.display ="flex"
    kx++
    if (kx == 2 ) {
        child.style.display ="none"
        kx = 0 
    }
    console.log(kx, 'skdkdk');
    
})
console.log(child );
console.log(window.innerWidth );

 function checkwidth() {
    
     if (window.innerWidth < 980) {
         btn__bar.style.display ="none"
     }
 }
setInterval(() => {
     checkwidth()
}, 3000);

