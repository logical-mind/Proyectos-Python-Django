
////////////////////////////////CIRCUSNCRIPCIONES////////////////////////////////
function circ_grafico(c1, c2, c3) {
  new Chart(document.getElementById("doughnut-chart"), {
    type: 'doughnut',
    data: {
      labels: ["Circ. 1", "Circ. 2", "Circ. 3"],
      datasets: [
        {
          label: "Population (millions)",
          backgroundColor: ["#3e95cd", "#3cba9f", "#e8c3b9"],
          data: [c1, c2, c3]
        }
      ]
    },
    options: {
      maintainAspectRatio: true, // Mantener el aspecto en dispositivos pequeños
      title: {
        display: true,
        text: 'Miembros por circunscripciones'
      },
      legend: {
        display: true,
        position: 'right' // Cambiar la posición de la leyenda a la derecha
      }
    }
  });
}

///////////////////////////////////////GENEROS//////////////////////////////////

function edad_grafico(m_total,m_joven,m_adulto,m_mayor,f_total,f_joven,f_adulto,f_mayor){

new Chart(document.getElementById("bar-chart-grouped"), {
  type: 'bar',
  data: {
    labels: ["Total", "Jovenes", "Adultos", "Mayores"],
    datasets: [
      {
        label: "Hombres",
        backgroundColor: "#3e95cd",
        data: [m_total,m_joven,m_adulto,m_mayor]
      }, {
        label: "Mujeres",
        backgroundColor: "#e8c3b9",
        data: [f_total,f_joven,f_adulto,f_mayor]
      }
    ]
  },
  options: {
    title: {
      display: true,
      text: 'Miembros por edad y genero'
    },
  }
});
}

/////////////////////////////////////////////////////SECTORES////////////////////////////////////////////////
function sector_grafico(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,a20,a21,a22,a23){
new Chart(document.getElementById("line-chart"), {
  type: 'line',
  data: {

labels:
['Ozama',
'Alma Rosa',
'Mendoza',
'Villa Faro',
'Los Tres Ojos',
'Las Américas',
'Villa Duarte',
'Los Mameyes',
'La Isabelita',
'Los Trinitarios',
'Los Tres Brazos',
'Los Mina Norte',
'Los Mina Sur',
'Cancino',
'El Tamarindo',
'Hainamosa',
'El Almirante',
'Ciudad Satélite',
'Brisas del Este',
'San José de Mendoza',
'Brisa Oriental',
'Los Frailes',
'La Ureña'],
    datasets: [
       { 
        data: [a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,a20,a21,a22,a23],
        label: "Miembros Votantes",
        borderColor: "#8e5ea2",
        fill: false
      }
    ]
  },
  options: {
    responsive:true,
    title: {
      display: true,
      text: 'Miembros por sectores'
    },
  }
});
}

const xValues = [
'Ozama',
'Alma Rosa',
'Mendoza',
'Villa Faro',
'Los Tres Ojos',
'Las Américas',
'Villa Duarte',
'Los Mameyes',
'La Isabelita',
'Los Trinitarios',
'Los Tres Brazos',
'Los Mina Norte',
'Los Mina Sur',
'Cancino',
'El Tamarindo',
'Hainamosa',
'El Almirante',
'Ciudad Satélite',
'Brisas del Este',
'San José de Mendoza',
'Brisa Oriental',
'Los Frailes',
'La Ureña'];

const yValues = [a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,a20,a21,a22,a23];

new Chart(document.getElementById("line-chart2"), {
  type: "line",
  data: {
    labels: xValues,
    datasets: [{
      backgroundColor:"rgba(0,0,255,1.0)",
      borderColor: "rgba(0,0,255,0.1)",
      data: yValues
    }]
  },
  
});


