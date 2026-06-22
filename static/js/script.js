function closeMenu() {
    document.getElementById('mobileMenu').style.setProperty('transform', 'translateX(100%)', 'important');
    document.getElementById('menuOverlay').classList.add('hidden');
}

function openLightbox(src) {
    const lightbox = document.getElementById('lightbox');
    document.getElementById('lightbox-img').src = src;
    lightbox.style.opacity = '1';
    lightbox.style.pointerEvents = 'auto';
}

function closeLightbox() {
    const lightbox = document.getElementById('lightbox');
    lightbox.style.opacity = '0';
    lightbox.style.pointerEvents = 'none';
}

function prevImage() {
    lightboxIndex = (lightboxIndex - 1 + lightboxImages.length) % lightboxImages.length;
    document.getElementById('lightbox-img').src = lightboxImages[lightboxIndex];
}

function nextImage() {
    lightboxIndex = (lightboxIndex + 1) % lightboxImages.length;
    document.getElementById('lightbox-img').src = lightboxImages[lightboxIndex];
}

function submitOrder() {
    const name = document.getElementById('checkout-name').value.trim();
    const phone = document.getElementById('checkout-phone').value.trim();
    const address = document.getElementById('checkout-address').value.trim();
    const notes = document.getElementById('checkout-notes').value.trim();
    const error = document.getElementById('checkout-error');

    if (!name || !phone || !address) {
        error.classList.remove('hidden');
        return;
    }

    error.classList.add('hidden');

    let message = `🌸 *New Order — Bloom*\n\n`;
    message += `*Name:* ${name}\n`;
    message += `*Phone:* ${phone}\n`;
    message += `*Address:* ${address}\n`;
    if (notes) message += `*Notes:* ${notes}\n`;
    message += `\n*Order:*\n`;

    cartItems.forEach(item => {
        message += `• ${item.name} × ${item.quantity} — EGP ${item.total}\n`;
    });

    message += `\n*Total: EGP ${grandTotal}*`;

    const whatsappNumber = '201228698505';
    const url = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(message)}`;
    window.open(url, '_blank');
}

let lightboxImages = [];
let lightboxIndex = 0;

document.addEventListener('DOMContentLoaded', () => {

    // Password toggle — login page
    const toggle = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('id_password');
    if (toggle && passwordInput) {
        toggle.addEventListener('click', () => {
            passwordInput.type = passwordInput.type === 'password' ? 'text' : 'password';
        });
    }

    // Password toggle — register page
    document.querySelectorAll('.toggle-password').forEach(toggle => {
        toggle.addEventListener('click', () => {
            const input = toggle.previousElementSibling;
            input.type = input.type === 'password' ? 'text' : 'password';
        });
    });

    // Mobile menu
    const menuToggle = document.getElementById('menuToggle');
    const menuClose = document.getElementById('menuClose');

    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            document.getElementById('mobileMenu').style.setProperty('transform', 'translateX(0)', 'important');
            document.getElementById('menuOverlay').classList.remove('hidden');
        });
    }

    if (menuClose) {
        menuClose.addEventListener('click', closeMenu);
    }

    // Lightbox images array
    const mainImg = document.getElementById('main-img');
    if (mainImg) {
        lightboxImages = [mainImg.src];
        document.querySelectorAll('.thumbnail-img').forEach(img => {
            lightboxImages.push(img.src);
        });
    }

    // 📸 Image preview — المطور والذكي لحل مشكلة التحديث ومزامنة الـ Preview لايف
    const fileInput = document.getElementById('id_image') || document.querySelector('input[type="file"]');
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    // بنحدث المعاينة في صندوق الصورة الحالية مباشرة أو صندوق الـ preview الجديد
                    const currentImg = document.getElementById('current-product-image');
                    const previewImg = document.getElementById('image-preview');
                    
                    if (currentImg) {
                        currentImg.src = e.target.result;
                    }
                    if (previewImg) {
                        previewImg.src = e.target.result;
                        previewImg.classList.remove('hidden');
                    }
                }
                reader.readAsDataURL(file);
            }
        });
    }

});
