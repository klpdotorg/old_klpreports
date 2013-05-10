var info;
var translations;

// Load the Visualization API and the piechart package.
google.load('visualization', '1', {'packages':['corechart','table','imagechart']});
var table1;
var grades = ['O','L','W','S','P'];

String.prototype.toTitleCase = function () {
    return this.replace(/\w\S*/g, function(txt){
      if(txt.indexOf('/')>0)
        return txt;
      else
	return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
};

function logslider(position) {
  // position will be between 0 and 100
  var minp = 0;
  var maxp = 100;

  // The result should be between 1 an 200
  var minv = Math.log(3);
  var maxv = Math.log(300);

  // calculate adjustment factor
  var scale = (maxv-minv) / (maxp-minp);

  return Math.exp(minv + scale*(position-minp));
}

    
function initialise(data)
{
  info = data;
  translations = info['transdict'];
  now = new Date()
  document.getElementById("reportdate").innerHTML = now.toDateString();
  document.getElementById("rephead").innerHTML = "<img src=\'/images/KLP_logo2.png\' width='130px' vertical-align='top' border=0 />" + '<br/>' + translations['H56'];

  document.getElementById("constname").innerHTML = translations[info["const_type"]] + " <img src=\'/images/arrow.gif\' width='8px' vertical-align='center' border='0'/>" + "<br/><h1>"  
                                               + info['const_name'] + "</h1>";
  document.getElementById("constinfo").innerHTML =  "<dl class='header-def'><dt>" + translations['H8'] + "</dt><dd>"
                           + info["const_code"] + "</dd>"
                           + "<dt>" + translations['H9'] + "</dt><dd>" + info["const_rep"] + "</dd>"
                           + "<dt>" + translations['H10'] + "</dt><dd>" + info["const_party"] + "</dd>" 
			   + "</dl>";
  document.getElementById("hiddenip").innerHTML = '<input type="hidden" name="const_type" value="'+ info["constype"] + '" />' +
  '<input type="hidden" name="const_id" value="'+ info["const_id"] + '" />' +
  '<input type="hidden" name="forreport" value="'+ info["forreport"] + '" />' +
  '<input type="hidden" name="rep_lang" value="'+ info["rep_lang"] + '" />' ;
  document.getElementById('instcounts').innerHTML = '<dl class=\'header-def\'>' 
			   + '<dt style="font-size:9pt">' + translations['H11'] + '</dt>'
                           + '<dd>' + info["inst_counts"]["abs_schcount"] + '</dd>'
			   + '<dt style="font-size:9pt">' + translations['H12'] + '</dt>'
                           + '<dd>' + info["inst_counts"]["abs_preschcount"] + '</dd>'
                           + '</dl>'
  if(parseInt(info["lib_count"]) != 0){
  
    document.getElementById("learninghead").innerHTML = translations['H113'];
    document.getElementById('learningintro_txt').innerHTML = (info['learningintro_txt'] == 'undefined') ? translations['H60'] : info['learningintro_txt'];

    document.getElementById('schassess_txt').innerHTML = (info['schassess_txt'] == 'undefined') ? translations['H60'] : info['schassess_txt'];
    sch_assess_chart();

    document.getElementById("angassesshead").innerHTML = translations['H114'];
    document.getElementById('angassess_txt').innerHTML = (info['angassess_txt'] == 'undefined') ? translations['H60'] : info['angassess_txt'];
    document.getElementById('angexpln_txt').innerHTML = (info['angexpln_txt'] == 'undefined') ? translations['H60'] : info['angexpln_txt'];
    ang_assess_chart();

/*  if(Object.keys(info["ang_assess_neighbor"]).length > 0) {
    ang_neighbours_chart();
  }
    document.getElementById("angneighhead").innerHTML = translations['H119'];
    document.getElementById('angneighbours_txt').innerHTML = (info['angneighbours_txt'] == 'undefined') ? translations['H60'] : info['angneighbours_txt']; */


    document.getElementById('source_txt').innerHTML = (info['source_txt'] == 'undefined') ? translations['H60'] : info['source_txt'];
  }
}

function sch_assess_chart()
{
      var data = new google.visualization.DataTable();
      data.addColumn('string' , 'Class');
      for (var i in grades) {
          data.addColumn('number', grades[i].toTitleCase());
      }
      for (var key in info["sch_assess_class"]){
        row = ['Class ' + key]
        for (var i in grades) {
            score = info["sch_assess_class"][key][grades[i]] == undefined ? 0 : info["sch_assess_class"][key][grades[i]];
            row.push(score * 100/ info["sch_assess_class"][key]["total"]);
        }
        data.addRow(row);
      }
      data.sort([{column:0,desc:false}]);
      var chart1 = new google.visualization.BarChart(document.getElementById('schassessclass_gph'));
      chart1.draw(data, {width: 750, height: 250, chartArea:{width:'72%'},  title: translations['H115'],colors:['f40d13','fa9b0d','f7fc1d','a9df0d','46af2f'], isStacked:true});

      data = new google.visualization.DataTable();
      data.addColumn('string' , 'Gender');
      for (var i in grades) {
          data.addColumn('number', grades[i].toTitleCase());
      }
      for (var key in info["sch_assess_gender"]){
        row = [key.toUpperCase()+'S']
        for (var i in grades) {
            score = info["sch_assess_gender"][key][grades[i]] == undefined ? 0 : info["sch_assess_gender"][key][grades[i]];
            row.push(score * 100/ info["sch_assess_gender"][key]["total"]);
        }
        data.addRow(row);
      }
      data.sort([{column:0,desc:false}]);
      var chart1 = new google.visualization.BarChart(document.getElementById('schassessgend_gph'));
      chart1.draw(data, {width: 750, height: 150, bar:{groupWidth:'35%'},chartArea:{width:'72%'},  title: translations['H116'],colors:['f40d13','fa9b0d','f7fc1d','a9df0d','46af2f'], isStacked:true});

      data = new google.visualization.DataTable();
      data.addColumn('string' , 'Constituency');
      for (var i in grades) {
          data.addColumn('number', grades[i].toTitleCase());
      }
      row = ['Bangalore']
      for (var i in grades) {
          score = info["sch_assess_bang"][grades[i]] == undefined ? 0 : info["sch_assess_bang"][grades[i]];
          row.push(score * 100/ info["sch_assess_bang"]["total"]);
      }
      data.addRow(row);
      row = [info['const_name'].toTitleCase()]
      for (var i in grades) {
          score = info["sch_assess_const"][grades[i]] == undefined ? 0 : info["sch_assess_const"][grades[i]];
          row.push(score * 100/ info["sch_assess_const"]["total"]);
      }
      data.addRow(row);

      data.sort([{column:0,desc:false}]);
      var chart1 = new google.visualization.BarChart(document.getElementById('schassesscomp_gph'));
      chart1.draw(data, {width: 750, height: 150, bar:{groupWidth:'35%'},chartArea:{width:'72%'},  title: translations['H118'],colors:['f40d13','fa9b0d','f7fc1d','a9df0d','46af2f'], isStacked:true});
}


function ang_assess_chart()
{
     var svghtml= '<svg width="100%" height="280px" version="1.0" xmlns="http://www.w3.org/2000/svg">'
     var _cx = 200;
     var _cy = 100;
     var bang_r = info["ang_assess_bang"]
     svghtml = svghtml + drawCircle(_cx,_cy,bang_r,'Bangalore','orange');
     _cx = _cx + (bang_r * 2) + 20;
     var const_r = info["ang_assess_score"];
     svghtml = svghtml + drawCircle(_cx,_cy,const_r,info["const_name"].toTitleCase(),'green');
     _cx = _cx + (const_r * 2) + 80;
     var boy_r = info["ang_assess_gender"]["male"];
     svghtml = svghtml + drawCircle(_cx,_cy,boy_r,'Boys Score','blue');
     _cx = _cx + (boy_r * 2) + 20;
     var girl_r = info["ang_assess_gender"]["female"];
     svghtml = svghtml + drawCircle(_cx,_cy,girl_r,'Girls Score','pink');
     svghtml = svghtml + '</svg>';
     document.getElementById('angassess_gph').innerHTML = svghtml;
}

function drawCircle(_cx,_cy,_r,label,color) {
     var circle_txt = '<circle cx="' + _cx + '" cy="' + _cy + '" r="' + logslider(_r) + '" fill="' + color + '"/>';
     var label_txt = '<text x="' + _cx + '" y="' + _cy + '" font-family="sans-serif" font-size="15px" text-anchor="middle" fill="black">' + _r + '%</text>';
     var desc_txt = '<text x="' + _cx + '" y="' + (_cy + 100) + '" font-family="sans-serif" font-size="15px" text-anchor="middle" fill="black">' + label + '</text>';
     return circle_txt + label_txt + desc_txt;
}

function libneighbours_chart()
{

}


//UTILITY FUCTIONS----------------------------

function sortDict(unsortedObj)
{
  var sortable = [];
  for (var key in unsortedObj)
  sortable.push([key, unsortedObj[key]]);
  var sortedDict = sortable.sort(function(a, b) {return b[1] - a[1]});
  return sortedDict;
}

function roundNumber(rnum, rlength) { // Arguments: number to round, number of decimal places
  var newnumber = Math.round(rnum*Math.pow(10,rlength))/Math.pow(10,rlength);
  return parseFloat(newnumber); // Output the result to the form field (change for your purposes)
}


function isEmpty(ob){
  for(var i in ob){ return false;}
  return true;
}

function ConvertToIndian(inputString,colour_code) { 
      cc_str = '';
      if( inputString == undefined || inputString == null)
        inputString = '0'
      if(colour_code){
        val = parseFloat(inputString[0]);
        bm = parseFloat(inputString[1]);
        /*if (val >= bm) {*/
        if (val >= 70) {
          cc_str = '<span style="color:#666;font-size:12pt;font-weight:bold"><span style="color:#43AD2C;">' 
        }
        else {
          cc_str = '<span style="color:#666;font-size:12pt;font-weight:bold"><span style="color:#CD4306;">' 
        }
      }
      inputString = inputString.toString(); 
      var numberArray = inputString.split('.', 2); 
      var pref = parseInt(numberArray[0]); 
      var suf = numberArray[1]; 
      var outputString = ''; 
      if (isNaN(pref)) return ''; 
      var minus = ''; 
      if (pref < 0) minus = '-'; 
      pref = Math.abs(pref).toString(); 
      if (pref.length > 3) { 
      var lastThree = pref.substr(pref.length - 3, pref.length); 
      pref = pref.substr(0, pref.length - 3); 
      if (pref.length % 2 > 0) { 
      outputString += pref.substr(0, 1) + ','; 
      pref = pref.substr(1, pref.length - 1); 
      } 

      while (pref.length >= 2) { 
      outputString += pref.substr(0, 2) + ','; 
      pref = pref.substr(2, pref.length); 
      } 

      outputString += lastThree; 
      } else { 

      outputString = minus + pref; 
      } 

      if (!isNaN(suf)) outputString += '.' + suf; 
      if(colour_code) {
        outputString = cc_str + outputString + '</span>%' 
        outputString = outputString + '<span style="font-size:8pt">&nbsp;&nbsp;&nbsp;' + translations['Bangalore Avg'] + ': ' + bm + '%</span></span>';
        return outputString; 
      } else {
        return outputString; 
      }
}

function ColourIcon(value,key) { 

      val = parseFloat(value[0]);
      /*bm = parseFloat(value[1]);
      if (val >= bm) {*/
      if (val >= 70) {
        return key;
      }
      else {
        return key.replace('.png','n.png');
      }
}
