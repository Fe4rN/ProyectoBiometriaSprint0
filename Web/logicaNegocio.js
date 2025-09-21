function obtenerUltimo() {
    fetch('/ultimo')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("resultado").innerHTML = "No hay datos aún";
            } else {
                document.getElementById("resultado").innerHTML =
                "Fecha: " + data.Fecha + "<br>" +
                "Contador: " + data.Contador + "<br>" +
                "CO2: " + data.CO2;
            }
        })
        .catch(err => {
            alert("Error al obtener datos: " + err);
        });
}
setInterval(obtenerUltimo, 5000);