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
    desactivateElemente('grafico')

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

    // var trTag = document.getElementById('results')
    // var th = document.createElement('th')
    // th.setAttribute('scope', 'row')
    // trTag.appendChild(th)
    
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




