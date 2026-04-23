// Subtle floating animation for circles
document.querySelectorAll('.circle').forEach(circle => {
    circle.style.animation = 'float 20s infinite ease-in-out';
});

const style = document.createElement('style');
style.innerHTML = `
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-30px); }
    100% { transform: translateY(0px); }
}
`;
document.head.appendChild(style);