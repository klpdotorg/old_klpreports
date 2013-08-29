function displayPane(dat,cons,typ)
{
  var the_list = dat[cons];
  content_str = '<div class="div-table">';
  for (key in the_list)
  {
    content_str = content_str +  '<div class="div-table-row">';
    content_str = content_str +  '<div class="div-table-col">' + key + '</div>';
    content_str = content_str +  '<div class="div-table-col2"><a target="_blank" href="/charts/' + cons + '/' + the_list[key] + '/kannada/' + typ + '"> Kannada</a></div>';
    content_str = content_str +  '<div class="div-table-col2"><a target="_blank" href="/charts/' + cons + '/' + the_list[key] + '/english/' + typ + '"> English</a></div>';
    content_str = content_str +  '</div>';
  }
  content_str = content_str +  '</div>';
  document.getElementById('content_pane').innerHTML = content_str;
}
