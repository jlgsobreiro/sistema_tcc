$(document).ready(() => {
  let fornecedores = [];
  $.post('/api/fornecedores_lista').then((res) => fornecedores = res);
  $("#empresa").autocomplete({source: fornecedores});
})
