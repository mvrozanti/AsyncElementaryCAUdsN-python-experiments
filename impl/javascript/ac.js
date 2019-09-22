var array = [0,0,0,0,0,1,0,0,0,0,0];

var r = 0;
var u = 0;
var l = 0;
var e = 1;
var n = 1;
var o = 1;
var m = 1;
var b = 0;

function generate(param) {
	return param.map(function(content, item, array) {
		if(array[item-1]===undefined) {
			array[item-1]=array[10];
			if(array[item-1]===1 && content===1 && array[item+1]===1 ) {
				return content= r
			}
			else if(array[item-1]===1 && content===1 && array[item+1]===0 ) {
				return content= u
			}
			else if(array[item-1]===1 && content===0 && array[item+1]===1 ) {
				return content= l
			}
			else if(array[item-1]===1 && content===0 && array[item+1]===0 ) {
				return content= e
			}
			else if(array[item-1]===0 && content===1 && array[item+1]===1 ) {
				return content= n
			}
			else if(array[item-1]===0 && content===1 && array[item+1]===0 ) {
				return content= o
			}
			else if(array[item-1]===0 && content===0 && array[item+1]===1 ) {
				return content= m
			}
			else if(array[item-1]===0 && content===0 && array[item+1]===0 ) {
				return content= b
			}
		} else if (array[item+1]===undefined) {
			array[item+1]=array[0];
			if(array[item-1]===1 && content===1 && array[item+1]===1 ) {
				return content= r
			}
			else if(array[item-1]===1 && content===1 && array[item+1]===0 ) {
				return content= u
			}
			else if(array[item-1]===1 && content===0 && array[item+1]===1 ) {
				return content= l
			}
			else if(array[item-1]===1 && content===0 && array[item+1]===0 ) {
				return content= e
			}
			else if(array[item-1]===0 && content===1 && array[item+1]===1 ) {
				return content= n
			}
			else if(array[item-1]===0 && content===1 && array[item+1]===0 ) {
				return content= o
			}
			else if(array[item-1]===0 && content===0 && array[item+1]===1 ) {
				return content= m
			}
			else if(array[item-1]===0 && content===0 && array[item+1]===0 ) {
				return content= b
			}
		} else {
			if(array[item-1]===1 && content===1 && array[item+1]===1 ) {
				return content= r
			}
			else if(array[item-1]===1 && content===1 && array[item+1]===0 ) {
				return content= u
			}
			else if(array[item-1]===1 && content===0 && array[item+1]===1 ) {
				return content= l
			}
			else if(array[item-1]===1 && content===0 && array[item+1]===0 ) {
				return content= e
			}
			else if(array[item-1]===0 && content===1 && array[item+1]===1 ) {
				return content= n
			}
			else if(array[item-1]===0 && content===1 && array[item+1]===0 ) {
				return content= o
			}
			else if(array[item-1]===0 && content===0 && array[item+1]===1 ) {
				return content= m
			}
			else if(array[item-1]===0 && content===0 && array[item+1]===0 ) {
				return content= b
			}
		}
	})
}
console.log(JSON.stringify(array));

var gen1 = generate(array)

console.log(JSON.stringify(gen1));

var gen2 = generate(gen1)

console.log(JSON.stringify(gen2));

var gen3 = generate(gen2)

console.log(JSON.stringify(gen3));

var gen4 = generate(gen3)

console.log(JSON.stringify(gen4));

var gen5 = generate(gen4)

console.log(JSON.stringify(gen5));