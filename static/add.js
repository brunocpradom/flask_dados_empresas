function changeDisplayByClass(className,state){
    var base = document.getElementsByClassName(className)
    for (i = 0; i < base.length; i++) {
        base[i].style.display = state;
    }
}

function desactivateElement(className){
    var tablinks = document.getElementsByClassName(className);
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace("mdc-tab--active", "");
    }
}

function changeTabContent(event,tab){
    changeDisplayByClass('base','flex')
    changeDisplayByClass('socios','none')
    changeDisplayByClass('cnae','none')
    changeDisplayByClass('grafico','none')
    changeDisplayByClass('tab-content','none')
    desactivateElement('mdc-tab')
    document.getElementById('datatable-results').innerHTML=''
    
    document.getElementById(tab).style.display='flex';
    event.currentTarget.className += " mdc-tab--active"
  }

function showCnaeOptions(){
    changeDisplayByClass('base','none')
    changeDisplayByClass('cnae','flex')
    
    var cnaeEspecifico = document.getElementById('cnae-especifico')
    cnaeEspecifico.className += " mdc-tab--active"
  }

  function changeCnae(event,tab){
    changeDisplayByClass('tab-content','none')
    desactivateElement('cnae')

    document.getElementById(tab).style.display='flex';
    event.currentTarget.className += " mdc-tab--active"
  }

  function showSociosOptions(){
    changeDisplayByClass('base','none')
    changeDisplayByClass('cnae','none')
    changeDisplayByClass('socios','flex')

    var sociosCNPJ = document.getElementById('socios-cnpj')
    sociosCNPJ.className += " mdc-tab--active"
  }

  function changeSocios(event,tab){
    changeDisplayByClass('tab-content','none')
    desactivateElement('socios')

    document.getElementById(tab).style.display='flex';
    event.currentTarget.className += " mdc-tab--active"
  }

  function showChartOptions(){
    changeDisplayByClass('base','none')
    changeDisplayByClass('cnae','none')
    changeDisplayByClass('socios','none')
    changeDisplayByClass('grafico','flex')

    var graficoSetor = document.getElementById('graficos-setor')
    graficoSetor.className += " mdc-tab--active"
  }

  function changeChart(event,tab){
    changeDisplayByClass('tab-content','none')
    desactivateElement('grafico')

    document.getElementById(tab).style.display='flex';
    event.currentTarget.className += " mdc-tab--active"
  }

function showResults(){
    changeDisplayByClass('tab-content','none')
    document.getElementById('datatable').style.display='flex';
}

function createDataTable(){
    var datatable = document.getElementById('datatable-results')

    var tr = document.createElement('tr')
    tr.setAttribute('id','results')
    datatable.appendChild(tr)
    
    var listResults = JSON.parse(request.responseText)
    var counter = 1
    for (list in listResults){
        var trTag = document.getElementById('datatable-results')
        var row = document.createElement('tr')
        row.setAttribute('id','results'+ counter)
        datatable.appendChild(row)

        var rowTag =document.getElementById('results' + counter)

        var th = document.createElement('th')
        th.setAttribute('scope', 'row')
        rowTag.appendChild(th)

        counter++
        for (data in listResults[list]){
            var td = document.createElement('td')
            td.innerHTML = listResults[list][data]
            rowTag.appendChild(td)
      }
    }

}


function createDataTableSocios(){
  var datatable = document.getElementById('socios-results')

  var tr = document.createElement('tr')
  tr.setAttribute('id','results')
  datatable.appendChild(tr)
  
  var listResults = JSON.parse(request.responseText)
  var counter = 1
  for (list in listResults){
      
      var row = document.createElement('tr')
      row.setAttribute('id','results-socios'+ counter)
      datatable.appendChild(row)

      var rowTag =document.getElementById('results-socios' + counter)

      var th = document.createElement('th')
      th.setAttribute('scope', 'row')
      rowTag.appendChild(th)

      counter++
      for (data in listResults[list]){
          var td = document.createElement('td')
          td.innerHTML = listResults[list][data]
          rowTag.appendChild(td)
    }
  }
}


function createDataTableAtivEcon(){
  var datatable = document.getElementById('atividade-economica-results')

  var tr = document.createElement('tr')
  tr.setAttribute('id','results')
  datatable.appendChild(tr)
  
  var listResults = JSON.parse(request.responseText)
  var counter = 1
  for (list in listResults){
      
      var row = document.createElement('tr')
      row.setAttribute('id','results-ativ-econ'+ counter)
      datatable.appendChild(row)

      var rowTag =document.getElementById('results-ativ-econ' + counter)

      var th = document.createElement('th')
      th.setAttribute('scope', 'row')
      rowTag.appendChild(th)

      counter++
      for (data in listResults[list]){
          var td = document.createElement('td')
          td.innerHTML = listResults[list][data]
          rowTag.appendChild(td)
    }
  }
}

function showSociosResults(){
  changeDisplayByClass('tab-content','none')
  document.getElementById('socios-results-datatable').style.display='flex';
}


function showAtivEconResults(){
  changeDisplayByClass('tab-content','none')
  document.getElementById('atividade-economica-table').style.display='flex';
}


function showChartResults(){
  changeDisplayByClass('tab-content','none')
  document.getElementById('chart-results').style.display='flex';
}


// Build the chart
function buildChart(municipio,lista){
  Highcharts.chart('container', {
  chart: {
      plotBackgroundColor: null,
      plotBorderWidth: null,
      plotShadow: false,
      type: 'pie'
  },
  title: {text: 'Empresas ativas por setor-'+municipio.toUpperCase()},
  tooltip: {pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'},
  accessibility: {point: {valueSuffix: '%'}},
  plotOptions: {
      pie: {
          allowPointSelect: true,
          cursor: 'pointer',
          dataLabels: {
              enabled: false
          },
          showInLegend: false
      }
  },
  series: [{
      name: 'Empresas ativas',
      colorByPoint: true,
      data: [
            {name: 'Agricultura,pecuária,prod.florestal,pesca',y: lista[0]}, 
            {name: 'Indústrias extrativas',y: lista[1]}, 
            {name: 'Indústrias de transformação',y: lista[2]}, 
            {name: 'Eletricidade e gás',y: lista[3]}, 
            {name: 'Água,esgoto,ativ.gest.resíduos',y: lista[4]}, 
            {name: 'Construção',y: lista[5]},
            {name: 'Comércio,reparação de veículos',y: lista[6]}, 
            {name: 'Transporte, armazenagem e correio',y: lista[7]}, 
            {name: 'Alojamento e alimentação',y: lista[8]}, 
            {name: 'Informação e comunicação',y: lista[9]}, 
            {name: 'Ativ.financeiras de seguros e serv.rel.',y: lista[10]}, 
            {name: 'Atividades imobiliárias',y: lista[11]},
            {name: 'At. profissionais tec. e científicas',y: lista[12]}, 
            {name: 'Ativ.administrativas e serv. complementares',y: lista[13]}, 
            {name: 'Admin.pública,defesa e seguridade social',y: lista[14]}, 
            {name: 'Saúde humana e serviços sociais',y: lista[15]}, 
            {name: 'Artes,cultura,esporte e recreação',y: lista[16]}, 
            {name: 'Outras ativ. de serviços',y: lista[17]},
            {name: 'Serviços domésticos',y: lista[18]},
            {name: 'Org.internacionais e outras inst.extraterritoriais',y: lista[19]}
          ]
  }]
  });
}


