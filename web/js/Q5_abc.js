

var single = '<div class="col-sm-6"><div class="card Q5_card" ><h3 class="Q5_card-title card-body">A</h3><p class="Q5_card-content">😅</p></div></div>'
var newContent = "";

var data = [['a', '😉'], ['b', '👏'], ['c', '👍'], ['d', '🗣'], ['i', '♀'], ['k', '🙌'], ['o', '💙'], ['p', '😍'], ['s', '🙏'], ['t', '😂'], ['w', '💪'], ['x', '👉']]

nextR = 4

for (i = 0; i < data.length; i++) {
	if(i%nextR==0){
		struc = '<div class="row">'
	}else{
		struc = ''
	}
	temp = data[i]
	struc += '<div class="col-sm-3"><div class="card Q5_card""><h3 class="Q5_card-title card-body">'
  	struc += temp[0].toUpperCase()
  	struc += '</h3><p class="Q5_card-content">'
  	struc += temp[1]
  	struc += '</p></div></div>'
  	if(i%nextR==nextR-1){
		struc += '</div>'
	}
  	newContent+= struc
}
$('#Q5-content').append(newContent);  

