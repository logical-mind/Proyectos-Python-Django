const postForm = document.querySelector("#formulario");


function handleSubmit(postForm) {
    
    postForm.addEventListener("submit", e => {

        
        var bloqueo = false
        const id_forms = ['form_nombre','form_apellido','form_cedula','form_telefono','form_fecha_nacimiento']
      
        for (i = 0; i < id_forms.length; i++) {
            var estado = $(`#${id_forms[i]}`).hasClass("formulario__grupo-incorrecto")
            if(estado==true){
                bloqueo = true
            }
          } 
      
        
       e.preventDefault();
       formData = new FormData(postForm);
       if(bloqueo==false){
        fetch('./post_create/', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {


                if(data.nombre != null){
        
                
                
                if(data.id_votante == null) {
                 
                document.querySelector("#notify").innerHTML = `<div class="alert alert-info alert-dismissible fade show" role="alert" id="success-alert">
                                                                  Has registrado a<strong> ${data.nombre} </strong>con éxito.
                                                                  <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                                                                </div> `}else{
                                                                    
                                                                    document.querySelector("#notify").innerHTML = `<div class="alert alert-info alert-dismissible fade show" role="alert" id="success-alert">
                                                                                                                      Has modificado a<strong> ${data.nombre} </strong>con éxito.
                                                                                                                      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                                                                                                                    </div> `}
                                                                

                


                resetear()  
                quitar_columna()
                coordinadores() 
            }

                else{ 
                    if(data.cedula != null){    
                    if(data.cedula[0] == "Votante with this Cedula already exists."){
                    document.querySelector("#notify").innerHTML = `<div class="alert alert-danger alert-dismissible fade show" role="alert">
                                                                  Este miembro ya se encuantra registrado.
                                                                  <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                                                                </div> `
                                                                resetear()
                                                                    
                                                                
                                                                    
                    }} else{
                            if(data.fecha_nacimiento != null){    
                            if(data.fecha_nacimiento[0] == "Enter a valid date."){
                            document.querySelector("#notify").innerHTML = `<div class="alert alert-danger alert-dismissible fade show" role="alert">
                                                                        La fecha de nacimiento es inválida.
                                                                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                                                                      </div> `
                            }} else{
                                document.querySelector("#notify").innerHTML = `<div class="alert alert-danger alert-dismissible fade show" role="alert">
                                 Error en datos del formulario, intente nueva vez.
                                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                              </div> ` 
                            }  
                    }
            }                                                                                  
            })
            .catch((error) => {
                console.log(error)
                console.error('Error:', error);
            });
        }else{

            document.querySelector("#notify").innerHTML = `<div class="alert alert-danger alert-dismissible fade show" role="alert">
            Campos incorrectos en el formulario.
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
          </div> `

        }
    })

   

}

handleSubmit(postForm)

function resetear(){
                const id_forms = ['form_nombre','form_apellido','form_cedula','form_telefono','form_fecha_nacimiento']
                postForm.reset();
                for (i = 0; i < id_forms.length; i++) {
		            document.getElementById(`${id_forms[i]}`).classList.remove('formulario__grupo-correcto');
		            document.querySelector(`#${id_forms[i]} i`).classList.remove('fa-check-circle');}
                
                $('[id="id_circunscripcion"]').val('0');
                $('#id_circunscripcion').trigger('change.select2');
                $('#id_genero').trigger('change.select2');
                $('#id_ocupacion').trigger('change.select2');
                //document.getElementById("id_sector").disabled = true;
                //document.getElementById("id_seccion").disabled = true; 
}