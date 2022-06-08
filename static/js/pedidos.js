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