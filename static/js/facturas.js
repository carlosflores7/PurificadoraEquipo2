function obtenerID(){
    var combo=document.getElementById("clientes");
    var idCliente=combo.options[combo.options.selectedIndex].value;
    var ajax=new XMLHttpRequest();
    var url='/Facturas/json/'+idCliente;
    ajax.open('get',url,true);
    ajax.onreadystatechange=function(){
        if(this.readyState==4 && this.status==200){
           llenarTabla(this.responseText);
        }
    };
    ajax.send();
}
function imprimirMsg(){
    alert('Documento cargado');
}
function llenarTabla(datos){
    var opciones=document.getElementById("ventas");
    var datosFactura=JSON.parse(datos);
    eliminarTabla();
    opciones=document.getElementById("ventas");
    for(i=0;i<datosFactura.length;i++){
        var tr=document.createElement("tr");
        var fac=datosFactura[i];
        for (propiedad in fac){
            //alert(propiedad);
            //alert(fac[propiedad]);
            var option=document.createElement("option");
            //var texto=document.createTextNode(prod[propiedad]);
            var texto=document.createTextNode(fac[propiedad]);
            var combo=document.getElementById("clientes");
            var idCliente=combo.options[combo.options.selectedIndex].value;
            if(idCliente==0){
                texto=document.createTextNode("Selecciona primero un cliente");
                opciones.setAttribute("readonly", true);
            }
            option.setAttribute("value", fac[propiedad]);
            option.appendChild(texto);
            opciones.appendChild(option);
            opciones.setAttribute("name", "Ventas")
        }
    }
}
function eliminarTabla(){
    document.getElementById("ventas").remove();
    var select=document.createElement("select");
    select.setAttribute("class", "form-control");
    select.setAttribute("id", "ventas");
    var div=document.getElementById("ventasdiv");
    div.appendChild(select);
}