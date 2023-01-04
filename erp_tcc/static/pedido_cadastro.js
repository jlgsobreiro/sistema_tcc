/*jshint esversion: 6 */
/*globals $:false */
let lista_produto = produtos();
let lista_clientes = clientes();
let produto_selecionado;
let campo_quantidade = $('#quantidade');
let campo_produto = $('#produto');
let campo_desconto = $('#desconto');
let campo_valor = $('#valor');
let campo_total = $('#total');
let campo_cliente = $('#cliente');
let campo_cliente_id = $('#cliente_id');
  $(document).ready(function(){
    "use strict";
    lista_produto = produtos();
    lista_clientes = clientes();
    console.log(lista_produto);
    console.log(lista_clientes);
    campo_cliente.autocomplete({data:lista_clientes});
    campo_produto.autocomplete({data:lista_produto});
  });
  campo_cliente.on('change', function () {
    "use strict";
    var instance = M.Autocomplete.getInstance(campo_cliente);
    console.log(instance.activeIndex);
    console.log(lista_clientes[campo_cliente.val()]);
    campo_cliente_id.val(lista_clientes[campo_cliente.val()]);
  });
  campo_produto.on('change', function () {
    "use strict";
    let id = lista_produto[$('#produto').val()];
    consulta_produto(id);
    $('#valor').val(produto_selecionado.valor);
    calcula_total();
  });
  campo_quantidade.on('change', function () {
    "use strict";
    calcula_total();
  });
  campo_desconto.on('change', function () {
    "use strict";
    calcula_total();
  });
  campo_valor.on('change', function () {
    "use strict";
    let valor_original = parseInt(produto_selecionado.valor);
    let valor_novo = parseInt(campo_valor.val());
    let desconto =  valor_original - valor_novo;
    campo_desconto.val(desconto);
    calcula_total();
  });
  function calcula_total(){
    "use strict";
    let quantidade = campo_quantidade.val();
    let valor = campo_valor.val() - campo_desconto.val();
    campo_total.val(quantidade*valor);
  }
function clientes() {
  "use strict";
  let key = {};
  $.post('/api/clientes', function (data) {
    data.forEach(function (r) {
      key[r.nome] = r._id.$oid;
    });
  });
  return key;
}
function consulta_produto(produto_id){
  "use strict";
  $.post('/api/produtos/'+produto_id, function (data) {
    produto_selecionado = data;
    console.log(data);
  });
}
function produtos() {
  "use strict";
  let key = {};
  $.post('/api/produtos', function (data) {
    data.forEach(function (r) {
      key[r.nome] = r._id.$oid;
    });
  });
  return key;
}
