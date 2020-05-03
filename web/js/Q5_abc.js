var single = '<div class="col-sm-6"><div class="card Q5_card" ><h3 class="Q5_card-title card-body">A</h3><p class="Q5_card-content">😅</p></div></div>'
var newContent = "";
for (i = 0; i < 10; i++) {
  	newContent += single;
}

$('#Q5-content').append(newContent);  