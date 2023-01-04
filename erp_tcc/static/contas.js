/*jshint esversion: 6 */
/*globals $:false */
  $(document).ready(function(){
    "use strict";
    let a = empresas();
    console.log(a);
    $('#empresa').autocomplete({data:a});
  });
function empresas() {
  "use strict";
  let key = {};
  $.post('/api/fornecedores_lista', function (data) {
    data.forEach(function (r) {
      key[r] = r;
    });
  });
  return key;
}
