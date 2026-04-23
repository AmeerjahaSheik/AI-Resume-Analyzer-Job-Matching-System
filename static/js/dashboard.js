// Level Selection Highlight
const buttons = document.querySelectorAll(".level-btn");

buttons.forEach(btn=>{
    btn.addEventListener("click", ()=>{
        buttons.forEach(b=>b.classList.remove("active"));
        btn.classList.add("active");
    });
});
