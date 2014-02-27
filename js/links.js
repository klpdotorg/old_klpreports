function displayPane(dat,cons,typ)
{
  var the_list = dat[cons];
  for (key in the_list)
  if (cons=='schl_dist' || cons=='block' || cons=='cluster' || cons=='pre_dist' || cons=='project' || cons=='circle')
     cons='boundary';
  heading_str = "<h1>" + cons.toUpperCase() + " Reports - " + typ.toUpperCase() + "</h1>";
  content_str = heading_str + '<div class="div-table">';
  for (key in the_list)
  { 
    if((typ!='infrastructure' && typ!='finance') && the_list[key][1]==2)
        continue;
    content_str = content_str +  '<div class="div-table-row">';
    content_str = content_str +  '<div class="div-table-col">' + key + '</div>';
    //content_str = content_str +  '<div class="div-table-col2"><a target="_blank" href="/charts/' + cons + '/' + the_list[key] + '/kannada/' + typ + '"> Kannada</a></div>';
    content_str = content_str +  '<div class="div-table-col2"><a target="_blank" href="/charts/' + cons + '/' + the_list[key][0] + '/english/' + typ + '"> English</a></div>';
    content_str = content_str +  '</div>';
  }
  content_str = content_str +  '</div><br/>For older PDF reports <a href="http://www.klp.org.in/listFiles/1" target="_blank">click here</a>';
  document.getElementById('content_pane').innerHTML = content_str;
}
