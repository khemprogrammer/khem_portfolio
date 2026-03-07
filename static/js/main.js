// Khem Bahadur Lodh - Portfolio JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Animate elements on scroll
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.project-card, .skill-category-card, .framework-card, .focus-card');
        
        elements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementVisible = 150;
            
            if (elementTop < window.innerHeight - elementVisible) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    };
    
    // Initialize animation styles
    const animatedElements = document.querySelectorAll('.project-card, .skill-category-card, .framework-card, .focus-card');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    });
    
    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // Run once on load
    
    // Counter animation for stats
    const animateCounters = function() {
        const counters = document.querySelectorAll('.stat-value');
        
        counters.forEach(counter => {
            const target = parseInt(counter.textContent);
            if (target && !counter.classList.contains('counted')) {
                const duration = 2000;
                const step = target / (duration / 16);
                let current = 0;
                
                const updateCounter = function() {
                    current += step;
                    if (current < target) {
                        counter.childNodes[0].textContent = Math.floor(current);
                        requestAnimationFrame(updateCounter);
                    } else {
                        counter.childNodes[0].textContent = target;
                        counter.classList.add('counted');
                    }
                };
                
                // Check if element is in view
                const observer = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting && !counter.classList.contains('counted')) {
                            updateCounter();
                            observer.unobserve(counter);
                        }
                    });
                });
                
                observer.observe(counter);
            }
        });
    };
    
    animateCounters();
    
    // Contact form AJAX submission
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Sending...';
            submitBtn.disabled = true;
            
            // Form will submit normally, this is for visual feedback
            setTimeout(() => {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 2000);
        });
    }
    
    // Newsletter form AJAX
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(newsletterForm);
            
            fetch('/contact/newsletter/subscribe/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message);
                    newsletterForm.reset();
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            });
        });
    }
    
    // Project filtering (if exists)
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectItems = document.querySelectorAll('.project-item');
    
    filterButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const filter = this.dataset.filter;
            
            filterButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            projectItems.forEach(item => {
                if (filter === 'all' || item.dataset.category === filter) {
                    item.style.display = 'block';
                    setTimeout(() => {
                        item.style.opacity = '1';
                        item.style.transform = 'scale(1)';
                    }, 10);
                } else {
                    item.style.opacity = '0';
                    item.style.transform = 'scale(0.8)';
                    setTimeout(() => {
                        item.style.display = 'none';
                    }, 300);
                }
            });
        });
    });
    
    // Mobile menu close on link click
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    const bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse);
    
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth < 992 && navbarCollapse.classList.contains('show')) {
                bootstrap.Collapse.getInstance(navbarCollapse).hide();
            }
        });
    });
    
    // Typing effect for hero (optional enhancement)
    const typingElement = document.querySelector('.typing-effect');
    if (typingElement) {
        const text = typingElement.textContent;
        typingElement.textContent = '';
        let i = 0;
        
        const typeWriter = function() {
            if (i < text.length) {
                typingElement.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            }
        };
        
        typeWriter();
    }
    
    // Lazy loading images
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        lazyImages.forEach(img => imageObserver.observe(img));
    }
    
    // Back to top button
    const backToTop = document.createElement('button');
    backToTop.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTop.className = 'back-to-top';
    backToTop.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        background: var(--primary);
        color: white;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s;
        z-index: 1000;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
    `;
    document.body.appendChild(backToTop);
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 500) {
            backToTop.style.opacity = '1';
            backToTop.style.visibility = 'visible';
        } else {
            backToTop.style.opacity = '0';
            backToTop.style.visibility = 'hidden';
        }
    });
    
    backToTop.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});