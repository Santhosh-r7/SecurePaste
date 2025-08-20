document.addEventListener("DOMContentLoaded",() =>{
    const observer = new MutationObserver(() => {
        const textarea = document.querySelector("textarea");
        if (textarea && !textarea.hasAttribute("data-guarded")){
            textarea.setAttribute("data-guarded","true");
            
            textarea.addEventListener("paste",async(e) =>{
                const pastedtext = (e.clipboardData || window.clipboardData).getData('text');
                
                const response = await fetch("http://localhost:5000/scan",{
                    method : "POST",
                    headers:{
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({prompt:pastedtext})
                });
                const result = await response.json();
                if (result.block){
                    alert("Risky content detected! Paste blocked.");
                    e.preventDefault();
                }
            });
        }
    });
observer.observe(document.body, {childList:true, subtree:true})
});