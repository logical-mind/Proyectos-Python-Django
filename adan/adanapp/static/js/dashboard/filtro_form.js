
const seccion2 = async (info) => {
             
           try {
            var circunscripcion= $('#id_circunscripcion').val();
            var sector= $('#id_sector').val();
            var seccion= $('#id_seccion').val();
           
            var filtros = {
                "circunscripcion": circunscripcion,
                "sector": sector,
                "seccion": seccion
            };
        
              if (circunscripcion != null){
              document.getElementById("id_sector").disabled = false;}
             
        
              if (sector != null){
                document.getElementById("id_seccion").disabled = false;}
               

              const response = await fetch("./secciones_form/",{
              method: "POST",
              body: JSON.stringify(filtros)
              })

              const secciones = await response.json();
              
              
             if (info == "circunscripcion"){
                borrar_sector2()
                borrar_seccion2()
             }

             else{
            if (info != "sector" && info != "seccion" ){
             var id_circunscripcion = document.getElementById("id_circunscripcion")
             id_circunscripcion.insertAdjacentHTML("beforeend", `<option value="0" disabled selected>Circunscripciones</option>`);
             for (let y = 0; y < secciones.circunscripcion.length ; y++){
             id_circunscripcion.insertAdjacentHTML("beforeend", `<option value="${secciones.circunscripcionid[y].id}"> ${secciones.circunscripcion[y].nombre} </option>`);} 
            }}

             
            if (info == "sector"){borrar_seccion2()}
            else{
             var id_sector = document.getElementById("id_sector")
             id_sector.insertAdjacentHTML("beforeend", `<option value="" disabled selected>Sectores</option>`);
             for (let y = 0; y < secciones.sector.length ; y++){
                
             id_sector.insertAdjacentHTML("beforeend", `<option value="${secciones.sectorid[y].id}"> ${secciones.sector[y].nombre} </option>`);}
            }

             var id_seccion = document.getElementById("id_seccion")
             id_seccion.insertAdjacentHTML("beforeend", `<option value="" disabled selected>Secciones</option>`);
             for (let y = 0; y < secciones.seccion.length ; y++){
             id_seccion.insertAdjacentHTML("beforeend", `<option value="${secciones.seccionid[y].id}"> ${secciones.seccion[y].nombre} </option>`);}
             
                
                
             }  
                 catch(error){alert(error)} 
             }

seccion2()	

    
function borrar_sector2(){
    var sector_borrar = document.getElementById('id_sector');
    if(sector_borrar !== null){
    while (sector_borrar.hasChildNodes()){
        sector_borrar.removeChild(sector_borrar.lastChild);
    }}}

function borrar_seccion2(){
    var seccion_borrar = document.getElementById('id_seccion');
    if(seccion_borrar !== null){
    while (seccion_borrar.hasChildNodes()){
        seccion_borrar.removeChild(seccion_borrar.lastChild);
    }}}		



function editar(){
            var circunscripcion= $('#id_circunscripcion').val();
            var sector= $('#id_sector').val();
            var seccion= $('#id_seccion').val();
            var ocupacion= $('#id_ocupacion').val();
            
            var link1 = `/admin/adanapp/circunscripcion/${circunscripcion}/change/?_to_field=id&_popup=1`;
            var link2 = `/admin/adanapp/sector/${sector}/change/?_to_field=id&_popup=1`;
            var link3 = `/admin/adanapp/seccion/${seccion}/change/?_to_field=id&_popup=1`;
            var link4 = `/admin/adanapp/ocupacion/${ocupacion}/change/?_to_field=id&_popup=1`;

            if (circunscripcion != null){
                var change_id_circunscripcion = document.getElementById("change_id_circunscripcion");
                change_id_circunscripcion.setAttribute(`href`, link1);
            }

            if (sector != null){
                var change_id_sector = document.getElementById("change_id_sector");
                change_id_sector.setAttribute(`href`, link2);
            }

            if (seccion != null){
                var change_id_seccion = document.getElementById("change_id_seccion");
                change_id_seccion.setAttribute(`href`, link3);
            }

            if (ocupacion != null){
                var change_id_ocupacion = document.getElementById("change_id_ocupacion");
                change_id_ocupacion.setAttribute(`href`, link4);
            }
}