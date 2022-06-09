function prestados(){
	var select=document.getElementById("divprestados");
	var prestados=document.getElementById("gprestados");
	var prestadosP=document.getElementById("garrafonesP");
	var control=prestados.options[prestados.options.selectedIndex].value;
	if(control=='1'){
		select.style.display = 'block';
	}else{
		prestadosP.value="0";
		select.style.display = 'none';
	}
}

function validar(form){
    var cad=validarNegativo(parseInt(form.cGarrafones.value));
    cad+=validarNegativoPrestados(parseInt(form.cGarrafonesPrestados.value));
    cad+=comparar(parseInt(form.cGarrafones.value), parseInt(form.cGarrafonesPrestados.value));
    var div=document.getElementById("notificaciones");
    if(cad!=''){
        div.innerHTML='<p>'+cad+'</p>';
        return false;
    }
    else{
        return true;
    }

}

function validarNegativo(garrafones){
	if(garrafones<=0){
		return 'La cantidad de garrafones debe ser positiva';
	}else{
		return '';
	}
}

function validarNegativoPrestados(garrafones){
	if(garrafones<0){
		return '<br>La cantidad de garrafones prestados debe ser mayor o igual a cero';
	}else{
		return '';
	}
}

function comparar(total,prestados){
	if(prestados>total){
		return '<br>La cantidad de garrafones prestados debe ser menor o igual al total';
	}else{
		return '';
	}
}