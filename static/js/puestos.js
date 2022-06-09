function validar(form){
    var cad=validarNegativo(parseInt(form.salario.value));
    var div=document.getElementById("notificaciones");
    if(cad!=''){
        div.innerHTML='<p>'+cad+'</p>';
        return false;
    }
    else{
        return true;
    }

}

function validarNegativo(salario){
    var regreso = '';
    if(salario<=0){
        regreso = '<br>El salario debe ser mayor a cero';
    }
    return regreso;
}