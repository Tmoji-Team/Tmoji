var single = '<div class="col-sm-6"><div class="card Q5_card" ><h3 class="Q5_card-title card-body">A</h3><p class="Q5_card-content">😅</p></div></div>'
var newContent = "";

var data = [['t', '😂'], ['s', '🙏'], ['d', '🗣'], ['p', '😍'], ['x', '👉'], ['a', '😉'], ['b', '👏'], ['i', '♀'], ['o', '💙'], ['k', '🙌'], ['c', '👍'], ['w', '💪']]

nextR = 3

for (i = 0; i < data.length; i++) {
	if(i%nextR==0){
		struc = '<div class="row"><div class="col-sm-4 "><div class="card Q5_card" style="max-width: 12rem;"><h3 class="Q5_card-title card-body">'
	}else{
		struc = '<div class="col-sm-4"><div class="card Q5_card" style="max-width: 12rem;"><h3 class="Q5_card-title card-body">'
	}
	temp = data[i]
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