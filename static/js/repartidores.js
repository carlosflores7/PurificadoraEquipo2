function validar(form){
    var cad=validarFolio(form.folio.value);
    var div=document.getElementById("notificaciones");
    if(cad!=''){
        div.innerHTML='<p>'+cad+'</p>';
        return false;
    }
    else{
        return true;
    }

}

function validarFolio(cadena){
    var patron=/\d{7}/;
    if(patron.test(cadena)==true){
        return '';
    }
    else{
        return 'El folio de la licencia deben ser exactamente 7 dígitos';
    }
}
