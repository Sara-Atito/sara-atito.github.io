(() => {
  const controls = document.querySelector('.publication-controls');
  const input = document.querySelector('#publication-search');
  const buttons = [...document.querySelectorAll('[data-filter]')];
  const papers = [...document.querySelectorAll('.publication')];
  const counter = document.querySelector('#results-count');
  const empty = document.querySelector('.empty-state');
  let category = 'All';
  function filter() {
    const query = input.value.toLowerCase().trim();
    let count = 0;
    papers.forEach(paper => {
      const visible = (category === 'All' || paper.dataset.category === category) && paper.dataset.search.includes(query);
      paper.hidden = !visible;
      if (visible) count++;
    });
    buttons.forEach(button => {
      const active = button.dataset.filter === category;
      button.classList.toggle('active', active);
      button.setAttribute('aria-pressed', String(active));
    });
    counter.textContent = `${count} selected publication${count === 1 ? '' : 's'}`;
    empty.hidden = count !== 0;
  }
  controls.hidden = false;
  buttons.forEach(button => button.addEventListener('click', () => {category = button.dataset.filter; filter();}));
  input.addEventListener('input', filter);
  document.querySelector('#reset-filters').addEventListener('click', () => {category = 'All'; input.value = ''; filter(); input.focus();});
})();
