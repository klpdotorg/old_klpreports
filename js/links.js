function displayPane(dat,cons,typ)
{
  document.getElementById('error_pane').style.visibility="hidden";
  var the_list = dat[cons];
  disclaimer_str ='<div id="disclaimer"><b>Disclaimer:</b> These reports below are being furnished for your information. You may choose to reproduce or redistribute this information in part or in full to any other person with due acknowledgement of Karnataka Learning Partnership (KLP). You will ensure that no part of the information provided here may be quoted out of context or misrepresented. KLP makes every effort to use reliable and comprehensive information from the government and other independent sources, but KLP does not represent that the data or information are accurate or complete. KLP is an independent, not-for-profit group. The information provided herein has been provided without regard to the objectives or opinions of those who may receive it. Please also see the <a href="http://www.klp.org.in/text/disclaimer" target="_blank">KLP Data Disclaimer</a>.</div>'

  heading_str = "<p class='bordered_text'>" + cons.toUpperCase() + " Reports - " + typ.toTitleCase() + "</p>";
  content_str = disclaimer_str + heading_str + '<div class="div-table">';
  for (key in the_list)
  {
    content_str = content_str +  '<div class="div-table-row">';
    content_str = content_str +  '<div class="div-table-col">' + key + '</div>';
    content_str = content_str +  '<div class="div-table-col2"><a target="_blank" href="/charts/' + cons + '/' + the_list[key] + '/kannada/' + typ + '"> Kannada</a></div>';
    content_str = content_str +  '<div class="div-table-col2"><a target="_blank" href="/charts/' + cons + '/' + the_list[key] + '/english/' + typ + '"> English</a></div>';
    content_str = content_str +  '</div>';
  }
  content_str = content_str +  '</div><br/>For older PDF reports <a href="http://www.klp.org.in/listFiles/1" target="_blank">click here</a>.';
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
