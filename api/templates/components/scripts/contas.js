/*jshint esversion: 6 */
/*globals $:false */
window.onload(function() {
  "use strict";
  let fornecedores = [];
  let a = 'test';
  $.post('/api/fornecedores_lista').then((res) => fornecedores = res);
  $("#empresa").autocomplete({source: fornecedores['res']});
});
