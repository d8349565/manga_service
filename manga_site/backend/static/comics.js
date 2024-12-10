document.addEventListener('DOMContentLoaded', () => {
    const favoriteButtons = document.querySelectorAll('.favorite-btn');

    favoriteButtons.forEach(button => {
        button.addEventListener('click', async (e) => {
            e.preventDefault();
            const comicId = button.getAttribute('data-id');
            const isFavorite = button.classList.contains('active');
            await toggleFavorite(comicId, button, isFavorite);
        });
    });
});

async function toggleFavorite(comicId, button, isFavorite) {
    const token = localStorage.getItem('token');
    const method = isFavorite ? 'DELETE' : 'POST';
    try {
        const response = await fetch(`/api/favorites/${comicId}`, {
            method: method,
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            button.classList.toggle('active');
        }
    } catch (error) {
        console.error('Error:', error);
    }
} 