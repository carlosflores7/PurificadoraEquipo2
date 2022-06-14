function validar(form){
    var cad=comparar(parseInt(form.cGarrafones.value), parseInt(form.garrafones_entregados.value));
    cad+=validarNegativo(parseInt(form.garrafones_entregados.value));
    var div=document.getElementById("notificaciones");
    if(cad!=''){
        div.innerHTML='<p>'+cad+'</p>';
        return false;
    }
    else{
        return true;
    }

}

function comparar(total,entregados){
	if(entregados>total){
		return '<br>La cantidad de garrafones entregados debe ser menor o igual al total';
	}else{
		return '';
	}
}

function validarNegativo(garrafones){
	if(garrafones<=0){
		return 'La cantidad de garrafones devueltos debe ser mayor a cero';
	}else{
		return '';
	}
}