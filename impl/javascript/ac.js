var gen0 = [0,0,0,0,0,1,0,0,0,0,0];

var ruleNumb1 = 0;
var ruleNumb2 = 0;
var ruleNumb3 = 0;
var ruleNumb4 = 1;
var ruleNumb5 = 1;
var ruleNumb6 = 1;
var ruleNumb7 = 1;
var ruleNumb8 = 0;

function generate(param) {
	return param.map(function(content, item, array) {
		if(array[item-1]===undefined) {
			array[item-1]=array[10];
			return array[item-1]===1 && content===1 && array[item+1]===1 ? content=ruleNumb1 : array[item-1]===1 && content===1 && array[item+1]===0 ? content=ruleNumb2 :
			array[item-1]===1 && content===0 && array[item+1]===1 ? content=ruleNumb3 : array[item-1]===1 && content===0 && array[item+1]===0 ? content=ruleNumb4 : 
			array[item-1]===0 && content===1 && array[item+1]===1 ? content=ruleNumb5 : array[item-1]===0 && content===1 && array[item+1]===0 ? content=ruleNumb6 :
			array[item-1]===0 && content===0 && array[item+1]===1 ? content=ruleNumb7 : array[item-1]===0 && content===0 && array[item+1]===0 ? content=ruleNumb8 : null;
		} else if (array[item+1]===undefined) {
			array[item+1]=array[0];
			return array[item-1]===1 && content===1 && array[item+1]===1 ? content=ruleNumb1 : array[item-1]===1 && content===1 && array[item+1]===0 ? content=ruleNumb2 :
			array[item-1]===1 && content===0 && array[item+1]===1 ? content=ruleNumb3 : array[item-1]===1 && content===0 && array[item+1]===0 ? content=ruleNumb4 : 
			array[item-1]===0 && content===1 && array[item+1]===1 ? content=ruleNumb5 : array[item-1]===0 && content===1 && array[item+1]===0 ? content=ruleNumb6 :
			array[item-1]===0 && content===0 && array[item+1]===1 ? content=ruleNumb7 : array[item-1]===0 && content===0 && array[item+1]===0 ? content=ruleNumb8 : null;
		} else {
			return array[item-1]===1 && content===1 && array[item+1]===1 ? content=ruleNumb1 : array[item-1]===1 && content===1 && array[item+1]===0 ? content=ruleNumb2 :
			array[item-1]===1 && content===0 && array[item+1]===1 ? content=ruleNumb3 : array[item-1]===1 && content===0 && array[item+1]===0 ? content=ruleNumb4 : 
			array[item-1]===0 && content===1 && array[item+1]===1 ? content=ruleNumb5 : array[item-1]===0 && content===1 && array[item+1]===0 ? content=ruleNumb6 :
			array[item-1]===0 && content===0 && array[item+1]===1 ? content=ruleNumb7 : array[item-1]===0 && content===0 && array[item+1]===0 ? content=ruleNumb8 : null;
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