document.addEventListener('DOMContentLoaded', () => {
    const searchBar = document.getElementById('search-bar');
    const boxes = document.querySelectorAll('.box');
    const sections = document.querySelectorAll('.universe-section');
    const bg1 = document.getElementById('bg1');
    const bg2 = document.getElementById('bg2');

    // Smooth Parallax for the Background Nebulas
    window.addEventListener('mousemove', (e) => {
        const x = (e.clientX / window.innerWidth) - 0.5;
        const y = (e.clientY / window.innerHeight) - 0.5;

        bg1.style.transform = `translate(${x * 50}px, ${y * 50}px) scale(1.1)`;
        bg2.style.transform = `translate(${x * -30}px, ${y * -30}px) scale(1.1) rotate(5deg)`;
    });

    // Real-time Search Filtering
    searchBar.addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase();

        boxes.forEach(box => {
            const content = box.textContent.toLowerCase();
            if (content.includes(term)) {
                box.style.display = 'block';
                box.style.opacity = '1';
                box.style.transform = 'scale(1)';
            } else {
                box.style.display = 'none';
            }
        });

        // Hide empty sections during search
        sections.forEach(section => {
            const visibleBoxes = section.querySelectorAll('.box[style*="display: block"]');
            const totalBoxesInGrid = section.querySelectorAll('.box');

            if (term.length > 0) {
                if (visibleBoxes.length === 0) {
                    section.style.display = 'none';
                } else {
                    section.style.display = 'block';
                }
            } else {
                // If search is empty, show everything
                section.style.display = 'block';
                totalBoxesInGrid.forEach(b => {
                    b.style.display = 'block';
                    b.style.opacity = '1';
                });
            }
        });
    });

    // Add staggered entrance animations
    boxes.forEach((box, index) => {
        box.style.opacity = '0';
        box.style.transform = 'translateY(30px)';
        setTimeout(() => {
            box.style.transition = 'all 0.6s cubic-bezier(0.23, 1, 0.32, 1)';
            box.style.opacity = '1';
            box.style.transform = 'translateY(0)';
        }, 100 + (index * 20));
    });
});
