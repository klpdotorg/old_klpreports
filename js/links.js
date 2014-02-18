function displayPane(dat,cons,typ)
{
  document.getElementById('error_pane').style.visibility="hidden";
  var the_list = dat[cons];
  heading_str = "<p class='bordered_text'>" + cons.toUpperCase() + " Reports - " + typ.toTitleCase() + "</p>";
  content_str = heading_str + '<div class="div-table">';
  for (key in the_list)
  {
    content_str = content_str +  '<div class="div-table-row">';
    content_str = content_str +  '<div class="div-table-col">' + key + '</div>';
    content_str = content_str +  '<div class="div-table-col2"><a target="_blank" href="/charts/' + cons + '/' + the_list[key] + '/kannada/' + typ + '"> Kannada</a></div>';
    content_str = content_str +  '<div class="div-table-col2"><a target="_blank" href="/charts/' + cons + '/' + the_list[key] + '/english/' + typ + '"> English</a></div>';
    content_str = content_str +  '</div>';
  }
  content_str = content_str +  '</div><br/>For older PDF reports <a href="http://www.klp.org.in/listFiles/1" target="_blank">click here</a>';
  document.getElementById('content_pane').innerHTML = content_str;
}

function showErrorsIfAny(data)
{
  if (data["errormsg"] != undefined)
    document.getElementById('error_pane').style.visibility="visible";
    document.getElementById('error_pane').innerHTML = '<p class="bordered_text"><span style="color:red">' + data["errormsg"] + '</span></p>'; 
}
String.prototype.toTitleCase = function() {
    var aStr = this.split(' ');
    var aProp = [];
    for (str in aStr) {
        aProp.push(aStr[str].charAt(0).toUpperCase() + aStr[str].slice(1));
    }
    return aProp.join(' ');
};
