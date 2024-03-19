


const coordinadores = async () => {
    try {
        const response = await fetch('./coordinadores/');
        const user = await response.json();
        console.log(user.me)
        me.innerHTML = `                
                <li style="list-style: none" id="me2" class="active">
                        
                <div style="text-align:center;"> <img style="border-radius:50px" src="https://bootdey.com/img/Content/avatar/avatar6.png" alt="" width="70px"></div>
                <div style="text-align:center; color:#97C1FF;font-size:20px;font-family: 'ABeeZee';font-style: italic;"line-height: 35px;>@${user.me[0].fields.username}&nbsp&nbsp&nbsp</div>
                <div class="d-flex justify-content-between">
								
								<div class="p-2"> ${user.me[0].fields.total_final}/${user.me[0].fields.meta}</div>
                <div class="p-2"> ${user.me[0].fields.porciento_final}%</div>
                <div class="p-2"> <a href="#me3" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle"></a> </div> 

								</div>

                <div class="progress">
								<div class="progress" role="progressbar" style="width: ${user.me[0].fields.porciento_final}%; border-radius: 10px;" aria-valuenow="${user.me[0].fields.porciento_final}" aria-valuemin="0" aria-valuemax="100"></div>   
                </div>
       
                </li>
                        
          `


if (user.coordinadores.length > 0){
    me2.innerHTML += `<ul id="me3" class="collapse list-unstyled"></ul>`;
    
for (let x = 0; x < user.coordinadores.length; x++){ 
    me3.innerHTML += `
    <li style="list-style: none; margin-left:0px;" id=me4${x}>
    <div class="row">
        <div class="col">
          <a style="color: red !important;"  href="#me5${x}" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">
            @${user.coordinadores[x].fields.username}&nbsp&nbsp&nbsp<span style="color:cyan;">${user.coordinadores[x].fields.total_final_n1}/${user.coordinadores[x].fields.meta}&nbsp&nbsp&nbsp${user.coordinadores[x].fields.total_porciento_n1}%</span>
            <div class="progress mt-1 mb-0" style="height: 7px;">
            <div class="progress-bar bg-primary" role="progressbar" style="width: ${user.coordinadores[x].fields.total_porciento_n1}%" aria-valuenow="${user.coordinadores[x].fields.total_porciento_n1}" aria-valuemin="0" aria-valuemax="100"></div>
            </div>
          </a>
        </div>
        <div style="margin-top:29px; margin-right:10px;" class="col-1"><i class="bi bi-eye"></i></div>
    </div>
    </li>
    `;
    
    if (user.coordinadores[x].fields.nivel2.length > 0){
        var id2 = document.getElementById(`me4${x}`);
        id2.innerHTML += `<ul id="me5${x}" class="collapse list-unstyled"></ul>`;
    
        for (let y = 0; y < user.coordinadores[x].fields.nivel2.length; y++){
            var id3 = document.getElementById(`me5${x}`);
            id3.innerHTML += `
            <li style="list-style: none;margin-left:10px;" id=me6${y}${x}>
            <div class="row">
                <div class="col">
                  <a href="#me7${y}${x}" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">
                    @${user.coordinadores[x].fields.nivel2[y].fields.username}&nbsp&nbsp&nbsp<span style="color:cyan;">${user.coordinadores[x].fields.nivel2[y].fields.total_final_n2}/${user.coordinadores[x].fields.nivel2[y].fields.meta}&nbsp&nbsp&nbsp${user.coordinadores[x].fields.nivel2[y].fields.total_porciento_n2}%</span>
                    <div class="progress mt-1 mb-0" style="height: 7px;">
                    <div class="progress-bar bg-danger" role="progressbar" style="width: ${user.coordinadores[x].fields.nivel2[y].fields.total_porciento_n2}%" aria-valuenow="${user.coordinadores[x].fields.nivel2[y].fields.total_porciento_n2}" aria-valuemin="0" aria-valuemax="100"></div>
                    </div>
                  </a>
                </div>
                <div style="margin-top:29px; margin-right:10px;" class="col-1"><i class="bi bi-eye"></i></div>
            </div>
            </li>
            `;  

            if (user.coordinadores[x].fields.nivel2[y].fields.nivel3.length > 0){
                var id5 = document.getElementById(`me6${y}${x}`);
                id5.innerHTML += `<ul id="me7${y}${x}" class="collapse list-unstyled"></ul>`;
                for (let i = 0; i < user.coordinadores[x].fields.nivel2[y].fields.nivel3.length; i++){
                    var id6 = document.getElementById(`me7${y}${x}`);
                    id6.innerHTML += `
                    <li style="list-style: none; margin-left:10px;">
                    <div class="row">
                        <div class="col">
                          <a href="" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">
                            @${user.coordinadores[x].fields.nivel2[y].fields.nivel3[i].fields.username}&nbsp&nbsp&nbsp<span style="color:cyan;">${user.coordinadores[x].fields.nivel2[y].fields.nivel3[i].fields.total}/${user.coordinadores[x].fields.nivel2[y].fields.nivel3[i].fields.meta}&nbsp&nbsp&nbsp${user.coordinadores[x].fields.nivel2[y].fields.nivel3[i].fields.porciento}%</span>
                            <div class="progress mt-1 mb-0" style="height: 7px;">
                            <div class="progress-bar bg-warning" role="progressbar" style="width: ${user.coordinadores[x].fields.nivel2[y].fields.nivel3[i].fields.porciento}%" aria-valuenow="${user.coordinadores[x].fields.nivel2[y].fields.nivel3[i].fields.porciento}" aria-valuemin="0" aria-valuemax="100"></div>
                            </div>
                          </a>
                        </div>
                        <div style="margin-top:29px; margin-right:10px;" class="col-1"><i class="bi bi-eye"></i></div>
                    </div>
                    </li>
                    `;  
                }            
            } 
        }            
    } 
}
}

var resta = parseInt(user.me[0].fields.meta) - parseInt(user.me[0].fields.total_final)
document.getElementById('total_votantes').innerHTML = 'Total: '+ user.me[0].fields.total_final
document.getElementById('restan_votantes').innerHTML = 'Restan: '+ resta
document.getElementById('barra_votantes').style.width = user.me[0].fields.porciento_final
console.log(user.me[0].fields.masculino)
document.getElementById('total_masculino').innerHTML = 'Total: '+ user.me[0].fields.masculino
document.getElementById('porciento_masculino').innerHTML = 'Hombres '+ user.me[0].fields.masculino_porciento+'%'
document.getElementById('barra_masculino').style.width = user.me[0].fields.masculino_porciento+'%'

document.getElementById('total_femenino').innerHTML = 'Total: '+ user.me[0].fields.femenino
document.getElementById('porciento_femenino').innerHTML = 'Mujeres '+ user.me[0].fields.femenino_porciento+'%'
document.getElementById('barra_femenino').style.width = user.me[0].fields.femenino_porciento+'%'

document.getElementById('total_jovenes').innerHTML = 'Total: '+ user.me[0].fields.jovenes
document.getElementById('porciento_jovenes').innerHTML = 'Jovenes '+ user.me[0].fields.jovenes_porciento+'%'
document.getElementById('barra_jovenes').style.width = user.me[0].fields.jovenes_porciento+'%'

document.getElementById('total_adultos').innerHTML = 'Total: '+ user.me[0].fields.adultos
document.getElementById('porciento_adultos').innerHTML = 'Adultos '+ user.me[0].fields.adultos_porciento+'%'
document.getElementById('barra_adultos').style.width = user.me[0].fields.adultos_porciento+'%'

document.getElementById('total_mayores').innerHTML = 'Total: '+ user.me[0].fields.mayores
document.getElementById('porciento_mayores').innerHTML = 'Mayores '+ user.me[0].fields.mayores_porciento+'%'
document.getElementById('barra_mayores').style.width = user.me[0].fields.mayores_porciento+'%'

circ_grafico(user.me[0].fields.c1,user.me[0].fields.c2,user.me[0].fields.c3)
edad_grafico(user.me[0].fields.masculino,user.me[0].fields.m_jovenes,user.me[0].fields.m_adultos,user.me[0].fields.m_mayores,user.me[0].fields.femenino,user.me[0].fields.f_jovenes,user.me[0].fields.f_adultos,user.me[0].fields.f_mayores)
sector_grafico(user.me[0].fields.a1,user.me[0].fields.a2,user.me[0].fields.a3,user.me[0].fields.a4,user.me[0].fields.a5,user.me[0].fields.a6,user.me[0].fields.a7,user.me[0].fields.a8,user.me[0].fields.a9,user.me[0].fields.a10,user.me[0].fields.a11,user.me[0].fields.a12,user.me[0].fields.a13,user.me[0].fields.a14,user.me[0].fields.a15,user.me[0].fields.a16,user.me[0].fields.a17,user.me[0].fields.a18,user.me[0].fields.a19,user.me[0].fields.a20,user.me[0].fields.a21,user.me[0].fields.a22,user.me[0].fields.a23)

}catch(error){} }

coordinadores();
