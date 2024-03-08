
// Add hover effect to cards
document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('mouseenter', function () {
        this.style.transform = 'scale(1.05)';
        this.style.transition = 'transform 0.2s';
    });
    card.addEventListener('mouseleave', function () {
        this.style.transform = 'scale(1)';
    });
});
