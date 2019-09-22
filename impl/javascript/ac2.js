var gen0 = [0,0,0,0,0,1,0,0,0,0,0];

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
console.log(JSON.stringify(gen0));

new Promise(function(resolve, reject) {
	resolve(generate(gen0));
	reject('Promise error');
}).then(function(gen1) {
	console.log(JSON.stringify(gen1));
	return generate(gen1);
}).then(function(gen2) {
	console.log(JSON.stringify(gen2));
	return generate(gen2);
}).then(function(gen3) {
	console.log(JSON.stringify(gen3));
	return generate(gen3);
}).then(function(gen4) {
	console.log(JSON.stringify(gen4));
	return generate(gen4);
}).then(function(gen5) {
	console.log(JSON.stringify(gen5));
});