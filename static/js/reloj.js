var hoy = new Date();
var horas = '';
var minutos = '';
if(hoy.getHours()<10){
	var horas = '0' + hoy.getHours();
}else{
	var horas = hoy.getHours();
}
if(hoy.getMinutes()<10){
	var minutos = '0' + hoy.getMinutes();
}else{
	var minutos = hoy.getMinutes();
}

switch(hoy.getMonth() + 1){
	case 1:
		mes = 'Enero'
		break;
	case 2:
		mes = 'Febrero'
		break;
	case 3:
		mes = 'Marzo'
		break;
	case 4:
		mes = 'Abril'
		break;
	case 5:
		mes = 'Mayo'
		break;
	case 6:
		mes = 'Junio'
		break;
	case 7:
		mes = 'Julio'
		break;
	case 8:
		mes = 'Agosto'
		break;
	case 9:
		mes = 'Septiembre'
		break;
	case 10:
		mes = 'Octubre'
		break;
	case 11:
		mes = 'Noviembre'
		break;
	case 12:
		mes = 'Diciembre'
		break;
}
var fecha = hoy.getDate() + '-' + mes + '-' + hoy.getFullYear();
function reloj() {
  var r=document.getElementById("reloj");
  r.innerHTML=fecha + ' / ' + horas + ':' + minutos;
}