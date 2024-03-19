
        let dataTable;
        let dataTableIsInitialized = false;

        const initDataTable = async (dataTableOptions) => {
            if (dataTableIsInitialized) {
                dataTable.destroy();
            }
        
            await listUsers();
        
            dataTable = $("#datatable_users").DataTable(dataTableOptions);
        
            $.extend(true, $.fn.dataTable.defaults, {
                language: {
                    search: ""
                }
            });
        
          
        
            dataTableIsInitialized = true;
        
            $('[type=search]').each(function () {
                $(this).attr("placeholder", "Buscar");
                $(this).css("color", "#ffffff"); 
                
                
            });
        };
        





        const listUsers = async () => {
            try {
                const response = await fetch('./table/');
                const users = await response.json();
                let content2 = ``;
                let content = ``;
                
                for (i = 0; i < users.user.length; i++) {
                    var sexo = '';
                   
                    if (users.user[i].fields.genero == 'M') {
                        sexo = 'Masculino';
                    }
                    if (users.user[i].fields.genero == 'F') {
                        sexo = 'Femenino';
                    }

                    content2 = `
                        <th style="color: #5481C8" id="th_no" class="centered">No</th>
                        <th style="color: #5481C8;" id="th_id" class="centered">Id</th>
                        <th style="color: #5481C8;" id="th_nombre" class="centered">Nombre</th>
                        <th style="color: #5481C8;" id="th_apellido" class="centered">Apellido</th>
                        <th style="color: #5481C8;" id="th_cedula" class="centered">Cédula</th>
                        <th style="color: #5481C8;" id="th_edad" class="centered">Edad</th>
                        <th style="color: #5481C8;" id="th_circ" class="centered">Circ.</th>
                        <th style="color: #5481C8;" id="th_sector" class="centered">Sector</th>
                        <th style="color: #5481C8;" id="th_seccion" class="centered">Sección</th>
                        <th style="color: #5481C8;" id="th_direccion" class="centered">Dirección</th>
                        <th style="color: #5481C8;" id="th_genero" class="centered">Género</th>
                        <th style="color: #5481C8;" id="th_recinto" class="centered">Recinto E.</th>
                        <th style="color: #5481C8;" id="th_telefono" class="centered">Teléfono</th>
                        <th style="color: #5481C8;" id="th_ocupacion" class="centered">Ocupación</th>
                        <th style="color: #5481C8;" id="th_voto" class="centered">Voto</th>
                        <th style="color: #5481C8;" id="th_coordinador" class="centered">Coord.</th>
                        <th style="color: #5481C8;" id="th_edicion" class="centered">Edición</th>`;

                    content += `
                        <tr>
                            <td style="color: white;" id="no${i}">${i}</td>
                            <td style="color: white;" id="id${i}">${users.user[i].pk}</td>
                            <td style="color: white;" id="nombre${i}">${users.user[i].fields.nombre}</td>
                            <td style="color: white;" id="apellido${i}">${users.user[i].fields.apellido}</td>
                            <td style="color: white;" id="cedula${i}">${users.user[i].fields.cedula}</td>
                            <td style="color: white;" id="edad${i}">${users.user[i].fields.edad} años</td>
                            <td style="color: white;" id="circ${i}">C-${users.user[i].fields.circunscripcion}</td>
                            <td style="color: white;" id="sector${i}">${users.user[i].fields.sector_nombre}</td>
                            <td style="color: white;" id="seccion${i}">${users.user[i].fields.seccion_nombre}</td>
                            <td style="color: white;" id="direccion${i}">${users.user[i].fields.direccion}</td>
                            <td style="color: white;" id="genero${i}">${sexo}</td>
                            <td style="color: white;" id="recinto${i}">${users.user[i].fields.recinto}</td>
                            <td style="color: white;" id="telefono${i}">${users.user[i].fields.telefono}</td>
                            <td style="color: white;" id="ocupacion${i}">${users.user[i].fields.ocupacion_nombre}</td>
                            <td style="color: white;" id="voto${i}">${users.user[i].fields.voto}</td>
                            <td style="color: white;" id="coordinador${i}">@${users.user[i].fields.coord_username}</td>
                            <td id="edicion${i}">
                                <button style="opacity: 0.6; background: #009AEB; border:none;" class="btn btn-sm btn-primary" onclick="modificar('${users.user[i].pk}','${users.user[i].fields.nombre}','${users.user[i].fields.apellido}','${users.user[i].fields.cedula}','${users.user[i].fields.fecha_nacimiento}','${users.user[i].fields.circunscripcion}','${users.user[i].fields.circunscripcion_nombre}','${users.user[i].fields.sector}','${users.user[i].fields.sector_nombre}','${users.user[i].fields.seccion}','${users.user[i].fields.seccion_nombre}','${users.user[i].fields.direccion}','${users.user[i].fields.genero}','${users.user[i].fields.recinto}','${users.user[i].fields.telefono}','${users.user[i].fields.ocupacion}','${users.user[i].fields.ocupacion_nombre}','${users.user[i].fields.voto}')"><i class="fa-solid fa-pencil"></i></button>                    
                                <a style="opacity: 0.6;" href="#myModal" class="trigger-btn" data-toggle="modal"><button style="background: white;" onclick="captura('${users.user[i].pk}')" class="btn btn-sm"> <i style="color:#009AEB;" class="fa-solid fa-trash-can"></i></button></a>
                            </td>
                        </tr>`;
                }
             
                tableBody_users.innerHTML = content;
                table_tr.innerHTML = content2;

                var suma = 0;
                var recipiente = "";

                for (let x = 0; x < 17; x++) {
                    var rec_check = document.getElementById(`check${x}`);
                    if (rec_check.checked) {
                        suma = suma + 1;
                        recipiente = rec_check;
                    }
                }
                if (suma == 1) {
                    recipiente.disabled = true;
                } else {
                    for (let x = 0; x < 17; x++) {
                        var rec_check = document.getElementById(`check${x}`);
                        if (rec_check.checked) {
                            if (rec_check.disabled) {
                                rec_check.disabled = false;
                            }
                        }
                    }
                }

                for (let x = 0; x < 17; x++) {
                    try {
                        var rec_check = document.getElementById(`check${x}`);
                        if (rec_check.checked) {

                        } else {
                            if (rec_check.dataset.nombre == '0') {
                                for (let i = 0; i < users.user.length; i++) {
                                    document.getElementById(`no${i}`).remove();
                                }
                                document.getElementById("th_no").remove();
                            }
                            if (rec_check.dataset.nombre == '1') {
                                for (let i = 0; i < users.user.length; i++) {
                                    document.getElementById(`id${i}`).remove();
                                }
                                document.getElementById("th_id").remove();
                            }
                            if (rec_check.dataset.nombre == '2') {
                                for (let i = 0; i < users.user.length; i++) {
                                    document.getElementById(`nombre${i}`).remove();
                                }
                                document.getElementById("th_nombre").remove();
                            }
                            if (rec_check.dataset.nombre == '3') {
                                for (let i = 0; i < users.user.length; i++) {
                                    document.getElementById(`apellido${i}`).remove();
                                }
                                document.getElementById("th_apellido").remove();
                            }
                            if (rec_check.dataset.nombre == '4') {
                                for (let i = 0; i < users.user.length; i++) {
                                    document.getElementById(`cedula${i}`).remove();
                                }
                                document.getElementById("th_cedula").remove();
                            }
                            if (rec_check.dataset.nombre == '5') {
                                for (let i = 0; i < users.user.length; i++) {
                                    document.getElementById(`edad${i}`).remove();
                                }
                                document.getElementById("th_edad").remove();
                            }
                            if (rec_check.dataset.nombre == '6') {
                                for (let i = 0; i < users.user.length; i++) {
                                    document.getElementById(`circ${i}`).remove();
                                }
                                document.getElementById("th_circ").remove();
                            }
                            if (rec_check.dataset.nombre == '7') {
                                for (let i = 0; i < users.user.length; i++) {
                                    document.getElementById(`sector${i}`).remove();
                                }
                                document.getElementById("th_sector").remove();
                            }
                            if (rec_check.dataset.nombre == '8') {
                                for (let i = 0; i < users.user.length; i++) {
                                    document.getElementById(`seccion${i}`).remove();
                                }
                                document.getElementById("th_seccion").remove();
                            }
                            if (rec_check.dataset.nombre == '9') {
                                for (let i = 0; i < users.user.length; i++) {
                                    document.getElementById(`direccion${i}`).remove();
                                }
                                document.getElementById("th_direccion").remove();
                            }
                            if (rec_check.dataset.nombre == '10') {
                                for (let i = 0; i < users.user.length; i++) {
                                    document.getElementById(`genero${i}`).remove();
                                }
                                document.getElementById("th_genero").remove();
                            }
                            if (rec_check.dataset.nombre == '11') {
                                for (let i = 0; i < users.user.length; i++) {
                                    document.getElementById(`recinto${i}`).remove();
                                }
                                document.getElementById("th_recinto").remove();
                            }
                            if (rec_check.dataset.nombre == '12') {
                                for (let i = 0; i < users.user.length; i++) {
                                    document.getElementById(`telefono${i}`).remove();
                                }
                                document.getElementById("th_telefono").remove();
                            }
                            if (rec_check.dataset.nombre == '13') {
                                for (let i = 0; i < users.user.length; i++) {
                                    document.getElementById(`ocupacion${i}`).remove();
                                }
                                document.getElementById("th_ocupacion").remove();
                            }
                            if (rec_check.dataset.nombre == '14') {
                                for (let i = 0; i < users.user.length; i++) {
                                    document.getElementById(`voto${i}`).remove();
                                }
                                document.getElementById("th_voto").remove();
                            }
                            if (rec_check.dataset.nombre == '15') {
                                for (let i = 0; i < users.user.length; i++) {
                                    document.getElementById(`coordinador${i}`).remove();
                                }
                                document.getElementById("th_coordinador").remove();
                            }
                            if (rec_check.dataset.nombre == '16') {
                                for (let i = 0; i < users.user.length; i++) {
                                    document.getElementById(`edicion${i}`).remove();
                                }
                                document.getElementById("th_edicion").remove();
                            }
                        }
                    } catch (error) {}
                }
            } catch (ex) {
                content = ``;  
                content2 = ``;
            }
        };

        function modificar(id_votante, nombre, apellido, cedula, nacimiento, circunscripcion, circunscripcion_nombre, sector, sector_nombre, seccion, seccion_nombre, direccion, genero, recinto, telefono, ocupacion, ocupacion_nombre, voto) {
            var dia = nacimiento.slice(8, 10); 
            var mes = nacimiento.slice(5, 7); 
            var anual = nacimiento.slice(0, 4); 

            var estado = $(`#modificar`).hasClass("collapsed");
            if (estado == true) {
                document.getElementById("modificar").click();
            }

            document.getElementById("id_id_votante").value = id_votante;
            document.getElementById("id_nombre").value = nombre;
            document.getElementById("id_nombre").focus();
            document.getElementById("id_apellido").value = apellido;
            document.getElementById("id_apellido").focus();
            document.getElementById("id_cedula").value = cedula;
            document.getElementById("id_cedula").focus();
            document.getElementById("id_telefono").value = telefono;
            document.getElementById("id_telefono").focus();
            document.getElementById("id_fecha_nacimiento").value = "Día: " + dia + ",  Mes: " + mes + ",  Año: " + anual;
            document.getElementById("id_fecha_nacimiento").focus();

            document.getElementById('id_circunscripcion').value = circunscripcion;
            document.getElementById('select2-id_circunscripcion-container').innerHTML = circunscripcion_nombre;

            document.getElementById('id_sector').value = sector;
            document.getElementById('select2-id_sector-container').innerHTML = sector_nombre;
            document.getElementById("id_sector").disabled = false;

            document.getElementById('id_seccion').value = seccion;
            document.getElementById('select2-id_seccion-container').innerHTML = seccion_nombre;
            document.getElementById("id_seccion").disabled = false;

            document.getElementById("id_direccion").value = direccion;
            document.getElementById("id_direccion").focus();

            document.getElementById('id_genero').value = genero;
            if (genero == 'M') {
                var genero_nombre = 'Masculino';
            }
            if (genero == 'F') {
                var genero_nombre = 'Femenino';
            }
            document.getElementById('select2-id_genero-container').innerHTML = genero_nombre;

            document.getElementById('id_ocupacion').value = ocupacion;
            document.getElementById('select2-id_ocupacion-container').innerHTML = ocupacion_nombre;

            document.getElementById("id_nombre").focus();

            $('html, body').animate({
                scrollTop: $("#accordionFlushExample").offset().top
            }, 500);
        }

        function captura(id_miembro) {
            document.getElementById("delete_btn").setAttribute('onclick', `eliminar(${id_miembro})`);
        }

        const eliminar = async (id_votante) => {
            try {
                const response = await fetch('./eliminar/', {
                    method: 'POST',
                    body: JSON.stringify({'id_votante': id_votante})
                });

                const respuesta = await response.json();
                quitar_columna();
                coordinadores();
            } catch(error) {}
        }

        function quitar_columna() {
            ocultar = [];
            
            const dataTableOptions = {
              order: [[5, 'desc']],
              lengthMenu: [],
              columnDefs: [
                { className: "centered", targets: [] },
                { visible: false, targets: [] },
                { orderable: true, targets: [] }
              ],
              pageLength: 10,
              destroy: true,
              dom: 'Bfrtip',
              buttons: [
                {
                  extend: 'copy',
                  text: 'Copiar',
                  className: 'btn4',
                
                },
                {
                  extend: 'csv',
                  text: 'CSV',
                  className: 'btn_4',
           
                },
                {
                    extend: 'excelHtml5',
                    autoFilter: true,
                    className: 'btn4'
                   
                 
                },
                {
                  extend: 'pdf',
                  text: 'PDF',
                  className: 'btn_4',
   
                },
                {
                  extend: 'print',
                  text: 'Imprimir',
                  className: 'btn_4',
         
                }
              ],
              select: true,
              language: {
                lengthMenu: "Mostrar _MENU_ registros por página",
                zeroRecords: "Ningún miembro encontrado",
                info: "Mostrando de _START_ a _END_ de un total de _TOTAL_ registros",
                infoEmpty: "Ningún miembro encontrado",
                infoFiltered: "(filtrados desde _MAX_ registros totales)",
                search: "",
                loadingRecords: "Cargando...",
                paginate: {
                  first: "Primero",
                  last: "Último",
                  next: "Siguiente",
                  previous: "Anterior"
                }
              }
            };
            
            initDataTable(dataTableOptions);
          }
          
          
        

        window.onload = quitar_columna;
