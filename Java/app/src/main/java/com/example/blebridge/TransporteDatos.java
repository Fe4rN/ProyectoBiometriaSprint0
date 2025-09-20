package com.example.blebridge;

//--------------------------------------
// Autor: Fédor Tikhomirov
//--------------------------------------

import android.util.Log;

//Esta clase procesa las tramas recibidas y envia los datos contenidos a la BBDD a traves de la API
public class TransporteDatos {
    static final String DIRECCIONAPI = "";

    //Clase para los datos procesados porque Java no tiene structs
    private static class DatosProcesados{
        int contador;
        int C02;
        public int getContador() { return contador; }
        public int getC02() { return C02; }
        public DatosProcesados(int contador, int C02){
            this.contador = contador;
            this.C02 = C02;
        }

    }

    private static int ProcesarCO2(int CO2_original){
        // TODO: Implementar procesado de datos una vez que haya datos a procesar
        return CO2_original;
    }

    public static DatosProcesados ProcesarTrama(TramaIBeacon trama) throws Exception {
        int major = Utilidades.bytesToIntOK(trama.getMajor()); //Pasamos el major de bytes a entero

        int idMedicion = major >> 8 & 0xFF; //Obtenemos los valores del byte alto

        int contador = major & 0xFF; //Obtenemos los valores del byte bajo
        if (idMedicion == 11) {
            int valorCO2 = Utilidades.bytesToIntOK(trama.getMinor());
            valorCO2 = ProcesarCO2(valorCO2);

            return new DatosProcesados(contador, valorCO2); //Devolvemos la clase con los datos del sensor
        } else {
            throw new Exception("Medicion leida no es de C02");
        }
    }

    public static void EnviarDatos(){
        //ToDo: Todavía tengo que crear la API
    }
}
