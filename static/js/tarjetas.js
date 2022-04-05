function validar(form){
    var empleado = form.empleado.value;
    var banco = form.banco.value;
    var tarjeta = form.numero.value;

    var cadena = verificarEmpleado(empleado);
    cadena+=verificarBanco(banco);
    cadena+=validarTarjeta(tarjeta);

    var div=document.getElementById("notificaciones");

    if(cadena==''){
        div.innerHTML="";
        return true;
    }
    else{
        div.innerHTML=cadena;
        return false;
    }
}
function verificarEmpleado(empleado){
    var salida = "";
    if(empleado=="opcion"){
        salida = "Debes elegir un empleado válido <br>";
    }
    return salida;
}
function verificarBanco(banco){
    var salida = "";
    if(banco=="opcion"){
        salida = "Debes elegir un banco válido <br>";
    }
    return salida;
}

function validarTarjeta(cadena){
    var salida="";
    if(cadena.length<16){
        salida="Debes introducir una tarjeta de 16 números";
    }
    return salida;
}