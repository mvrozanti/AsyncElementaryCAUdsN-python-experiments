var gen0 = [0,0,0,0,0,1,0,0,0,0,0];

var ruleNumb = '00011110';
var splitedRuleNumb = ruleNumb.split('').map(Number);

function generate(param) {
	return param.map(function(content, item, array) {
		if(array[item-1]===undefined) {
			array[item-1]=array[10];
			return array[item-1]===1 && content===1 && array[item+1]===1 ? content=splitedRuleNumb[0] : array[item-1]===1 && content===1 && array[item+1]===0 ? content=splitedRuleNumb[1] :
			array[item-1]===1 && content===0 && array[item+1]===1 ? content=splitedRuleNumb[2] : array[item-1]===1 && content===0 && array[item+1]===0 ? content=splitedRuleNumb[3] : 
			array[item-1]===0 && content===1 && array[item+1]===1 ? content=splitedRuleNumb[4] : array[item-1]===0 && content===1 && array[item+1]===0 ? content=splitedRuleNumb[5] :
			array[item-1]===0 && content===0 && array[item+1]===1 ? content=splitedRuleNumb[6] : array[item-1]===0 && content===0 && array[item+1]===0 ? content=splitedRuleNumb[7] : null;
		} else if (array[item+1]===undefined) {
			array[item+1]=array[0];
			return array[item-1]===1 && content===1 && array[item+1]===1 ? content=splitedRuleNumb[0] : array[item-1]===1 && content===1 && array[item+1]===0 ? content=splitedRuleNumb[1] :
			array[item-1]===1 && content===0 && array[item+1]===1 ? content=splitedRuleNumb[2] : array[item-1]===1 && content===0 && array[item+1]===0 ? content=splitedRuleNumb[3] : 
			array[item-1]===0 && content===1 && array[item+1]===1 ? content=splitedRuleNumb[4] : array[item-1]===0 && content===1 && array[item+1]===0 ? content=splitedRuleNumb[5] :
			array[item-1]===0 && content===0 && array[item+1]===1 ? content=splitedRuleNumb[6] : array[item-1]===0 && content===0 && array[item+1]===0 ? content=splitedRuleNumb[7] : null;
		} else {
			return array[item-1]===1 && content===1 && array[item+1]===1 ? content=splitedRuleNumb[0] : array[item-1]===1 && content===1 && array[item+1]===0 ? content=splitedRuleNumb[1] :
			array[item-1]===1 && content===0 && array[item+1]===1 ? content=splitedRuleNumb[2] : array[item-1]===1 && content===0 && array[item+1]===0 ? content=splitedRuleNumb[3] : 
			array[item-1]===0 && content===1 && array[item+1]===1 ? content=splitedRuleNumb[4] : array[item-1]===0 && content===1 && array[item+1]===0 ? content=splitedRuleNumb[5] :
			array[item-1]===0 && content===0 && array[item+1]===1 ? content=splitedRuleNumb[6] : array[item-1]===0 && content===0 && array[item+1]===0 ? content=splitedRuleNumb[7] : null;
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