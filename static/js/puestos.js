function validar(form){
    var cad=validarSalario(parseInt(form.salario_max.value),parseInt(form.salario_min.value));
    cad+=validarNegativo(parseInt(form.salario_max.value),parseInt(form.salario_min.value));
    var div=document.getElementById("notificaciones");
    if(cad!=''){
        div.innerHTML='<p>'+cad+'</p>';
        return false;
    }
    else{
        return true;
    }

}

function validarSalario(max,min){
    if(max>min){
        return '';
    }
    else{
        return 'El salario máximo debe ser mayor al salario mínimo';
    }
}

function validarNegativo(max,min){
    var regreso = '';
    if(max<=0){
        regreso = '<br>El salario máximo debe ser mayor a cero';
    }

    if(min<=0){
        regreso += '<br>El salario mínimo debe ser mayor a cero';
    }

    return regreso;
}