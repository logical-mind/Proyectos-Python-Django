$(document).ready(function() {
    $('.js-example-basic-multiple').select2({});
    $(".seccion").select2({
    placeholder: "Filtrar Barrio o Urb.",
     allowClear: true
       });

       $(".sector").select2({
    placeholder: "Filtrar Sector.",
     allowClear: true});

     $(".circunscripcion").select2({
    placeholder: "Filtrar Circunscripción.",
     allowClear: true
    });

    $(".genero").select2({
    placeholder: "Filtrar Género.",
     allowClear: true
    });

    $(".ocupacion").select2({
    placeholder: "Filtrar Ocupación.",
     allowClear: true
    });

    $(".edad").select2({
    placeholder: "Filtrar Edad.",
     allowClear: true
    });


    });

    

const seccion = async (info) => {
             
           try {
            var circunscripcion = $('#select_circunscripcion').val();

            var sector = $('#select_sector').val();

            var seccion = $('#select_seccion').val();

            var genero = $('#select_genero').val();

            var ocupacion = $('#select_ocupacion').val();

            var edad = $('#select_edad').val();
 
            
            var filtros = {
                "circunscripcion": circunscripcion,
                "sector": sector,
                "seccion": seccion,
                "genero": genero,
                "ocupacion": ocupacion,
                "edad"     : edad
                };
            
              const response = await fetch("./seccion/",{
              method: "POST",
              body: JSON.stringify(filtros)
              })

              const secciones = await response.json();
             
             if (info == "circunscripcion"){
                borrar_sector()
                borrar_seccion()
             }
             else{
            if (info != "sector" && info != "seccion" ){
             var select_circunscripcion = document.getElementById("select_circunscripcion")
             for (let y = 0; y < secciones.circunscripcion.length ; y++){
             select_circunscripcion.insertAdjacentHTML("beforeend", `<option value="${secciones.circunscripcion[y].nombre}"> ${secciones.circunscripcion[y].nombre} </option>`);}
            
            }}

             
            if (info == "sector"){borrar_seccion()}
            else{
             var select_seccion = document.getElementById("select_sector")
             for (let y = 0; y < secciones.sector.length ; y++){
             select_seccion.insertAdjacentHTML("beforeend", `<option value="${secciones.sector[y].nombre}"> ${secciones.sector[y].nombre} </option>`);}
            }

             var select_seccion = document.getElementById("select_seccion")
             for (let y = 0; y < secciones.seccion.length ; y++){
             select_seccion.insertAdjacentHTML("beforeend", `<option value="${secciones.seccion[y].nombre}"> ${secciones.seccion[y].nombre} </option>`);}
             
                
                
             }  
                 catch(error){alert(error)} 
             }

seccion()	

    
function borrar_sector(){
    var sector_borrar = document.getElementById('select_sector');
    if(sector_borrar !== null){
    while (sector_borrar.hasChildNodes()){
        sector_borrar.removeChild(sector_borrar.lastChild);
    }}}

function borrar_seccion(){
    var seccion_borrar = document.getElementById('select_seccion');
    if(seccion_borrar !== null){
    while (seccion_borrar.hasChildNodes()){
        seccion_borrar.removeChild(seccion_borrar.lastChild);
    }}}		


var select_edad = document.getElementById("select_edad")
              
             for (let y = 2020; y > 1899 ; y--){
             select_edad.insertAdjacentHTML("beforeend", `<option value="${y}"> ${y} </option>`);}

