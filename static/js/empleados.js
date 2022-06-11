function validar(form){
    var cad=validarNSS(form.nss.value);

    var div=document.getElementById("notificaciones");
    if(cad!=''){
        div.innerHTML='<p>'+cad+'</p>';
        return false;
    }
    else{
        return true;
    }

}

function validarNSS(cadena){
    var patron=/\d{11}/;
    if(patron.test(cadena)==true){
        return '';
    }
    else{
        return 'El NSS debe ser exactamente 11 dígitos<br>';
    }
}

