//---------------------------------
// Autor: Fédor Tikhomirov
//---------------------------------

// Método para obtener el último valor
// Envia peticion al endpoint /ultimo que le devuelve las mediciones, luego escriben en el HTML sus valores
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

// Así nos evitamos la modificacion de la URL y la recarga de la página
document.getElementById("sensorForm").addEventListener("submit", subirDato(e));
//Actualizamos los datos cada 5 segundos para una mejor UX
setInterval(obtenerUltimo, 5000);

// Permite enviar datos desde la web, lee los campos de CO2 y contador y los envia al endpoint "/datosSensor",
// que los guarda en la base de datos
async function subirDato(e) {
    e.preventDefault();

    const contador = document.getElementById("contador").value;
    const co2 = document.getElementById("co2").value;

    try {
        const response = await fetch("/datosSensor", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                Contador: parseInt(contador),
                CO2: parseFloat(co2) })
        });

        const data = await response.json();
        if (data.status === "ok") {
            document.getElementById("mensaje").innerText = "Datos enviados correctamente";
        } else {
            document.getElementById("mensaje").innerText = "Error al enviar los datos";
        }
    } catch (err) {
        document.getElementById("mensaje").innerText = "Error: " + err;
    }
};