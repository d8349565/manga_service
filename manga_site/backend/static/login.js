document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const tokenDuration = document.getElementById('tokenDuration').value;
    
    try {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        formData.append('token_duration', tokenDuration);
        
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('token', data.access_token);
            window.location.href = '/static/comics.html';
        } else {
            const errorData = await response.json();
            alert(errorData.detail || '登录失败');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('登录失败，请重试');
    }
}); 