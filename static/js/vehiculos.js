function consultarPlacas(){
    var ajax = new XMLHttpRequest();
    var placas = document.getElementById("placas").value;
    var url = '/vehiculos/placas/' + placas;
    var div = document.getElementById("notificaciones");
    ajax.open('Get',url, true);
    ajax.onreadystatechange = function (){
        if (this.readyState== 4 && this.status==200){
            var respuesta == JSON.parse(this.responseText);
            if (respuesta.status=='Ok'){
                document.getElementById("registrar").removeAttribute("disabled");
            }else{
                document.getElementById("registrar").setAttribute("disabled","true");
                div.innerHTML = respuesta.mensaje;
            }
        }
    }
}