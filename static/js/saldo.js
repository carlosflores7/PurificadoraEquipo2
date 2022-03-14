function mostrarSaldo(){
    var ajax=new XMLHttpRequest();
    url='/tarjeta/saldo';
    ajax.open('get',url,true);
    ajax.onreadystatechange=function(){
        if(this.status==200 && this.readyState==4){
            var tarjeta=JSON.parse(this.responseText);
            llenarCamposTarjeta(tarjeta);
        }
    };
    ajax.send();   
}

function llenarCamposTarjeta(tarjeta){
    if(tarjeta.estatus!='error'){
        document.getElementById("saldoTarjeta").value=tarjeta.saldo;
    }
}

function hacerPago(){
    if(parseInt(document.getElementById("saldoTarjeta").value) >= parseInt(document.getElementById("totalAPagar").value)){
        alert('Procesando pago...');
        window.location = "/carrito/pagar"
    }else{
        alert('Asegúrate de tener un método de pago y que tenga suficiente saldo');
    }
}

function inicio(){
    mostrarSaldo();
}