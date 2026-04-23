<script>
const preview = document.getElementById("preview");
const container = document.querySelector(".hero-right");

container.addEventListener("mousemove", (e) => {
    const rect = container.getBoundingClientRect();
    
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    const rotateX = ((y - centerY) / centerY) * -15;
    const rotateY = ((x - centerX) / centerX) * 15;

    preview.style.transition = "transform 0.1s ease";
    preview.style.transform = `
        rotateX(${rotateX}deg)
        rotateY(${rotateY}deg)
        translateZ(20px)
    `;
});

container.addEventListener("mouseleave", () => {
    preview.style.transition = "transform 0.5s ease";
    preview.style.transform = `
        rotateX(0deg)
        rotateY(0deg)
        translateZ(0px)
    `;
});
</script>
