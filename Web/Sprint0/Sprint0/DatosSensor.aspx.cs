using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace Sprint0
{
    public partial class DatosSensor : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (IsPostBack) return;

            Response.Write("En endpoint DatosSensor está listo");
        }

        public void RecibirDatos(int contador, int co2)
        {
            //Guardar en base de datos;
        }
    }
}