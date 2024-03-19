const formulario = document.getElementById('formulario');
const inputs = document.querySelectorAll('#formulario input');


const expresiones = {
	usuario: /^[a-zA-Z0-9\_\-]{4,16}$/, // Letras, numeros, guion y guion_bajo
	nombre: /^[a-zA-ZÀ-ÿ\s]{1,100}$/, // Letras y espacios, pueden llevar acentos.
    apellido: /^[a-zA-ZÀ-ÿ\s]{1,100}$/, // Letras y espacios, pueden llevar acentos.
	password: /^.{4,12}$/, // 4 a 12 digitos.
	correo: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
	telefono: /^[0-9\ \)\(\-]{14}$/, // 7 a 14 numeros.
    cedula: /^[0-9\-]{13}$/, // 7 a 14 numeros.
	fecha_nacimiento: /^[a-zA-Z0-9\ \:\,\í\ñ]{29}$/ // Letras, numeros, guion y guion_bajo
}


const campos = {
	nombre: false,
	apellido: false,
	fecha_nacimiento: false,
	cedula: false,
	telefono: false
}

const validarFormulario = (e) => {
	
	switch (e.target.name) {
        
		case "nombre":
			if(e.target.value != ""){
            var oracion = e.target.value;
            var palabras = oracion.split(" ");
            var nombre = ""            
            for (let i = 0; i < palabras.length; i++) {
                palabras[i] = palabras[i][0].toUpperCase() + palabras[i].substr(1);
                if (nombre.length <= 0){ nombre = nombre + palabras[i]
                }else{nombre = nombre + " " + palabras[i] }}
            e.target.value = nombre

			validarCampo(expresiones.nombre, e.target, 'nombre');
			}
		break;

		case "apellido":
			if(e.target.value != ""){
            var oracion = e.target.value;
            var palabras = oracion.split(" ");
            var nombre = ""            
            for (let i = 0; i < palabras.length; i++) {
                palabras[i] = palabras[i][0].toUpperCase() + palabras[i].substr(1);
                if (nombre.length <= 0){ nombre = nombre + palabras[i]
                }else{nombre = nombre + " " + palabras[i] }}
            e.target.value = nombre
			validarCampo(expresiones.apellido, e.target, 'apellido');}
		break;

		case "direccion":
			if(e.target.value != ""){
			var oracion = e.target.value;
            var palabras = oracion.split(" ");
            var nombre = ""            
            for (let i = 0; i < palabras.length; i++) {
                palabras[i] = palabras[i][0].toUpperCase() + palabras[i].substr(1);
                if (nombre.length <= 0){ nombre = nombre + palabras[i]
                }else{nombre = nombre + " " + palabras[i] }}
			e.target.value = nombre}
		break;

		case "cedula":
			if(e.target.value != ""){
			validarCampo(expresiones.cedula, e.target, 'cedula');}
		break;

		case "telefono":
			if(e.target.value != ""){
			validarCampo(expresiones.telefono, e.target, 'telefono');}
		break;

		case "fecha_nacimiento":
			if(e.target.value != ""){
			validarCampo(expresiones.fecha_nacimiento, e.target, 'fecha_nacimiento');}
		break;
	}
}


const validarCampo = (expresion, input, campo) => {
	if(expresion.test(input.value)){
		document.getElementById(`form_${campo}`).classList.remove('formulario__grupo-incorrecto');
		document.getElementById(`form_${campo}`).classList.add('formulario__grupo-correcto');
		document.querySelector(`#form_${campo} i`).classList.add('fa-check-circle');
		document.querySelector(`#form_${campo} i`).classList.remove('fa-times-circle');
		campos[campo] = true;
	} else {
		document.getElementById(`form_${campo}`).classList.add('formulario__grupo-incorrecto');
		document.getElementById(`form_${campo}`).classList.remove('formulario__grupo-correcto');
		document.querySelector(`#form_${campo} i`).classList.add('fa-times-circle');
		document.querySelector(`#form_${campo} i`).classList.remove('fa-check-circle');
		campos[campo] = false;
	}
}

inputs.forEach((input) => {
	input.addEventListener('keyup', validarFormulario);
	input.addEventListener('blur', validarFormulario);
});
