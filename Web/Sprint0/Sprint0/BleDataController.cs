using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Http;

namespace Sprint0
{
    public class BleDataController : ApiController
    {
        public class SensorData
        {
            public string Fecha {  get; set; }
            public int Contador { get; set; }
            public int CO2 { get; set; }
        }

        [HttpPost]
        public IHttpActionResult Post([FromBody] SensorData data)
        {
            if (data == null) return BadRequest("No data received.");
            return Ok(new { message = "Data received!" });
        }
    }
}