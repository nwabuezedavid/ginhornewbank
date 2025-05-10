const paymentForm = document.querySelector('.paymentForm');
paymentForm.addEventListener('submit', (e)=> {
    
    e.preventDefault()
    let handler = PaystackPop.setup({
        key: '{{key}} ', // Replace with your public key
    email: "{{request.user.email}}",
    amount: document.getElementById("amount").value * 100,
    ref: 'ID'+Math.floor((Math.random() * 1000000000) + 1), // generates a pseudo-unique reference. Please replace with a reference you generated. Or remove the line entirely so our API will generate one for you
    // label: "Optional string that replaces customer email"
    onClose: function(){
   
        
        
    },
    callback: function(response){
let amountb = document.getElementById("amount").value
    localStorage.setItem('amount', amountb)
    localStorage.setItem('isverified', 'ref')
    location.href="{% url 'fundingf' user.uuid %}"
        
    }
  });

 
  handler.openIframe();
},false)