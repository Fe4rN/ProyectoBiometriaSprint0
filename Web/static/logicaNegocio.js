//---------------------------------
// Autor: Fédor Tikhomirov
//---------------------------------

// Método para obtener el último valor
async function obtenerUltimo() {
    try {
        const respuesta = await fetch('/ultimo');
        const datos = await respuesta.json();

        if (datos.error) {
            document.getElementById("resultado").innerHTML = "No hay datos aún";
        } else {
            document.getElementById("resultado").innerHTML =
                "Fecha: " + datos.Fecha + "<br>" +
                "Contador: " + datos.Contador + "<br>" +
                "CO2: " + datos.CO2;
        }
    } catch (error) {
        alert("Error al obtener los datos: " + error);
    }
}

//Actualizamos los datos cada 5 segundos
setInterval(obtenerUltimo, 5000);

// Método para subir datos manualmente
async function enviarLectura(events) {
    event.preventDefault();

    const contador = document.getElementById("contador").value;
    const co2 = document.getElementById("co2").value;

    const datos = {Contador:parseInt(contador), CO2: parseInt(co2)};

    try{
        const respuesta = await fetch('/datosSensor', {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(datos)
        });

        const resultado = await respuesta.json();

        if(respuesta.ok){
            document.getElementById("mensaje").innerText = "Lectura enviada con éxito"
            obtenerUltimo();
        } else {
            document.getElementById("mensaje").innerText = `Error: ${result.error}`;
        }
    } catch (error) {
        document.getElementById('mensaje').innerText = `Error de conexión: ${error}`;
    }
}