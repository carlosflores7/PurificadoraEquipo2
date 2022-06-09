function obtenerID(){
    var combo=document.getElementById("empleados");
    var idEmpleado=combo.options[combo.options.selectedIndex].value;
    var ajax=new XMLHttpRequest();
    var url='/Tarjetas/json/'+idEmpleado;
    ajax.open('get',url,true);
    ajax.onreadystatechange=function(){
        if(this.readyState==4 && this.status==200){
           llenarTabla(this.responseText);
        }
    };
    ajax.send();
}

function llenarTabla(datos){
    var opciones=document.getElementById("tarjetas");
    var datosTarjeta=JSON.parse(datos);
    eliminarTabla();
    opciones=document.getElementById("tarjetas");
    var combo=document.getElementById("empleados");
    var idEmpleado=parseInt(combo.options[combo.options.selectedIndex].value);
    var option=document.createElement("option");
    if(idEmpleado==0){
        var texto=document.createTextNode("Selecciona primero un empleado");
        opciones.setAttribute("readonly", true);
        option.appendChild(texto);
        opciones.appendChild(option);
        opciones.setAttribute("name", "Tarjetas")
    }
    var nomina=document.getElementById("idNomina");
    nomina.setAttribute("value", "0");
    for(i=0;i<datosTarjeta.length;i++){
        var tar=datosTarjeta[i];
            //alert(propiedad);
            //alert(tar[propiedad]);
            var option=document.createElement("option");
            //var texto=document.createTextNode(prod[propiedad]);
            var texto=document.createTextNode(tar['Tarjeta']);
            combo=document.getElementById("empleados");
            idEmpleado=parseInt(combo.options[combo.options.selectedIndex].value);
            option.setAttribute("value", tar['idTarjeta']);
            option.appendChild(texto);
            opciones.appendChild(option);
            opciones.setAttribute("name", "Tarjetas")
            nomina.setAttribute("value", tar['idNomina']);
    }
}
function eliminarTabla(){
    document.getElementById("tarjetas").remove();
    var select=document.createElement("select");
    select.setAttribute("class", "form-control");
    select.setAttribute("id", "tarjetas");
    var div=document.getElementById("tarjetasdiv");
    div.appendChild(select);
}