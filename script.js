const header = document.querySelector('[data-header]');
const nav = document.querySelector('[data-nav]');
const navToggle = document.querySelector('[data-nav-toggle]');
const form = document.querySelector('[data-form]');
const formStatus = document.querySelector('[data-form-status]');
const newsList = document.querySelector('[data-news-list]');

window.addEventListener('scroll', () => {
  header.classList.toggle('scrolled', window.scrollY > 24);
});

navToggle.addEventListener('click', () => {
  const isOpen = nav.classList.toggle('open');
  navToggle.setAttribute('aria-expanded', String(isOpen));
});

nav.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => {
    nav.classList.remove('open');
    navToggle.setAttribute('aria-expanded', 'false');
  });
});

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.14 });

document.querySelectorAll('.reveal').forEach((element) => observer.observe(element));

function renderNewsAccordion() {
  if (!newsList || !Array.isArray(window.newsData)) return;

  newsList.innerHTML = window.newsData.map((item) => {
    const paragraphs = item.content
      .map((paragraph) => `<p>${paragraph}</p>`)
      .join('');

    const linkMarkup = item.link
      ? `<a class="news-link" href="${item.link}" target="_blank" rel="noopener noreferrer">Источник</a>`
      : '';

    return `
      <details class="news-item" name="news-accordion">
        <summary class="news-summary">
          <div class="news-summary-main">
            <div class="news-meta">
              <span class="news-date">${item.date}</span>
              <span class="news-tag">${item.tag}</span>
            </div>
            <h3 class="news-title">${item.title}</h3>
            <p class="news-lead">${item.lead}</p>
          </div>
          <span class="news-toggle" aria-hidden="true">+</span>
        </summary>

        <div class="news-content">
          <div class="news-text">
            ${paragraphs}
          </div>
          ${linkMarkup}
        </div>
      </details>
    `;
  }).join('');

  const detailsList = newsList.querySelectorAll('.news-item');

  detailsList.forEach((details) => {
    details.addEventListener('toggle', () => {
      if (!details.open) return;

      detailsList.forEach((other) => {
        if (other !== details) {
          other.open = false;
        }
      });
    });
  });
}

renderNewsAccordion();

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const data = Object.fromEntries(new FormData(form));
  formStatus.textContent = 'Отправляем заявку...';

  try {
    const response = await fetch('/send.php', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });

    const result = await response.json();

    if (!response.ok || !result.ok) {
      throw new Error(result.message || 'Ошибка отправки заявки.');
    }

    formStatus.textContent = result.message;
    form.reset();
  } catch (error) {
    formStatus.textContent = 'Не удалось отправить заявку. Пожалуйста, позвоните нам напрямую.';
  }
});
