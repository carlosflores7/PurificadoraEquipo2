function validarTarjetas(form){
    var cad=validarnumero(form.noTarjeta.value);
    cad+=validarsaldo(form.Saldo.value);
    var div=document.getElementById("notificaciones");
    if(cad!=''){
        div.innerHTML='<p>'+cad+'</p>';
        return false;
    }
    else{
        return true;
    }

}
function validarnumero(cadena){
    for(i=0;i<cadena.length;i++){
        }
        if(i==16){
            return '';
        }else{
            return 'Tu tarjeta necesita ser de 16 digitos para continuar,<br>'
        }
    }


function validarsaldo(cadena){
    if(cadena<1 ){
        return 'La tarjeta necesita mas saldo para continuar,<br>';
    }
    else{
        return '';
    }
}